import pyparsing as pp
import networkx as nx
import itertools
from . import DataJointError


class Dependencies(nx.DiGraph):
    """
    The graph of dependencies (foreign keys) between loaded tables.
    """
    __primary_key_parser = (pp.CaselessLiteral('PRIMARY KEY') +
                            pp.QuotedString('(', endQuoteChar=')').setResultsName('primary_key'))

    def __init__(self, connection):
        self._conn = connection
        self.loaded_tables = set()
        self._node_alias_count = itertools.count()
        super().__init__(self)

    @staticmethod
    def __foreign_key_parser(database):
        def paste_database(unused1, unused2, toc):
            return ['`{database}`.`{table}`'.format(database=database, table=toc[0])]

        return (pp.CaselessLiteral('CONSTRAINT').suppress() +
                pp.QuotedString('`').suppress() +
                pp.CaselessLiteral('FOREIGN KEY').suppress() +
                pp.QuotedString('(', endQuoteChar=')').setResultsName('attributes') +
                pp.CaselessLiteral('REFERENCES') +
                pp.Or([
                    pp.QuotedString('`').setParseAction(paste_database),
                    pp.Combine(pp.QuotedString('`', unquoteResults=False) + '.' +
                               pp.QuotedString('`', unquoteResults=False))]).setResultsName('referenced_table') +
                pp.QuotedString('(', endQuoteChar=')').setResultsName('referenced_attributes'))

    def add_table(self, table_name):
        """
        Adds table to the dependency graph
        :param table_name: in format `schema`.`table`
        """
        if table_name in self.loaded_tables:
            return
        fk_parser = self.__foreign_key_parser(table_name.split('.')[0].strip('`'))
        self.loaded_tables.add(table_name)
        self.add_node(table_name)
        create_statement = self._conn.query('SHOW CREATE TABLE %s' % table_name).fetchone()[1].split('\n')
        primary_key = None
        for line in create_statement:
            if primary_key is None:
                try:
                    result = self.__primary_key_parser.parseString(line)
                except pp.ParseException:
                    pass
                else:
                    primary_key = [s.strip(' `') for s in result.primary_key.split(',')]
            try:
                result = fk_parser.parseString(line)
            except pp.ParseException:
                pass
            else:
                if '`.`~' not in result.referenced_table:  # omit external tables
                    referencing_attributes = [r.strip('` ') for r in result.attributes.split(',')]
                    referenced_attributes = [r.strip('` ') for r in result.referenced_attributes.split(',')]
                    props = dict(
                        primary=all(a in primary_key for a in referencing_attributes),
                        referencing_attributes=referencing_attributes,
                        referenced_attributes=referenced_attributes,
                        aliased=not all(a == b for a, b in zip(referencing_attributes, referenced_attributes)),
                        multi=not all(a in referencing_attributes for a in primary_key))
                    if not props['aliased']:
                        self.add_edge(result.referenced_table, table_name, **props)
                    else:
                        # for aliased dependencies, add an extra node in the format '1', '2', etc
                        alias_node = '%d' % next(self._node_alias_count)
                        self.add_node(alias_node)
                        self.add_edge(result.referenced_table, alias_node, **props)
                        self.add_edge(alias_node, table_name, **props)

    def load(self, target=None):
        """
        Load dependencies for all loaded schemas.
        This method gets called before any operation that requires dependencies: delete, drop, populate, progress.
        """
        if target is not None and '.' in target:  # `database`.`table`
            self.add_table(target)
        else:
            databases = self._conn.schemas if target is None else [target]
            for database in databases:
                for row in self._conn.query('SHOW TABLES FROM `{database}`'.format(database=database)):
                    table = row[0]
                    if not table.startswith('~'):  # exclude service tables
                        self.add_table('`{db}`.`{tab}`'.format(db=database, tab=table))
        if not nx.is_directed_acyclic_graph(self):  # pragma: no cover
            raise DataJointError('DataJoint can only work with acyclic dependencies')

    def parents(self, table_name, primary=None):
        """
        :param table_name: `schema`.`table`
        :param primary: if None, then all parents are returned. If True, then only foreign keys composed of
            primary key attributes are considered.  If False, the only foreign keys including at least one non-primary
            attribute are considered.
        :return: dict of tables referenced by the foreign keys of table
        """
        return dict(p[::2] for p in self.in_edges(table_name, data=True)
                    if primary is None or p[2]['primary'] == primary)

    def children(self, table_name, primary=None):
        """
        :param table_name: `schema`.`table`
        :param primary: if None, then all children are returned. If True, then only foreign keys composed of
            primary key attributes are considered.  If False, the only foreign keys including at least one non-primary
            attribute are considered.
        :return: dict of tables referencing the table through foreign keys
        """
        return dict(p[1:3] for p in self.out_edges(table_name, data=True)
                    if primary is None or p[2]['primary'] == primary)

    def descendants(self, full_table_name):
        """
        :param full_table_name:  In form `schema`.`table_name`
        :return: all dependent tables sorted in topological order.  Self is included.
        """
        nodes = nx.algorithms.dag.descendants(self, full_table_name)
        return [full_table_name] + nx.algorithms.dag.topological_sort(self, nodes)
