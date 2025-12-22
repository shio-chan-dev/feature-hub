
from abc import ABC


class BaseDecisionTable(ABC):
    pass

class FakeDecisionTable(BaseDecisionTable):
    pass


dec_table: BaseDecisionTable = FakeDecisionTable()

