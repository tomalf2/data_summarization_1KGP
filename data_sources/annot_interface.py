from typing import List, Callable
from sqlalchemy.engine import Connection
from sqlalchemy.sql.expression import FromClause
from data_sources.io_parameters import *


def do_not_notify(type: SourceMessage.Type, msg: str) -> None:
    return


class AnnotInterface:

    # MAP ATTRIBUTE NAMES TO TABLE COLUMN NAMES
    col_map: dict = {}

    def __init__(self, logger_instance, notify_message: Callable[[SourceMessage.Type, str], None] = do_not_notify):
        self.logger = logger_instance
        self.notify_message = notify_message

    def annotate(self, connection: Connection, genomic_interval: GenomicInterval,
                 attrs: Optional[List[Vocabulary]], assembly: str) -> FromClause:
        raise NotImplementedError('Any subclass of AnnotInterface must implement the abstract method "annotate"')

    def find_gene_region(self, connection: Connection, gene: Gene, output_attrs: List[Vocabulary], assembly: str) -> FromClause:
        raise NotImplementedError('Any subclass of AnnotInterface must implement the abstract method "find_gene_region"')

    def values_of_attribute(self, connection, attribute: Vocabulary) -> (str, List):
        raise NotImplementedError('Any subclass of AnnotInterface must implement the abstract method "values_of_attribute".')

    @classmethod
    def get_available_annotation_types(cls):
        if len(cls.col_map) == 0:
            raise NotImplementedError('Source concrete implementations need to override class '
                                      'dictionary "col_map"')
        return cls.col_map.keys()
