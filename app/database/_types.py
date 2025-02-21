from enum import Enum

class DBEnum(Enum):

    def __str__(self):
        return self.value

class State(DBEnum):
    draft = 'draft'
    sent = 'sent'
    posted = 'posted'
    cancel = 'cancel'

class BusinessModel(DBEnum):
    piso = 'piso'
    ce = 'ce'

class ModuleOrigin(DBEnum):
    sale = 'sale'
    pos = 'pos'
    account = 'account'

class WarehouseCode(DBEnum):
    a1 = 'a1'
    a2 = 'a2'
