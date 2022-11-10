from .test.test import test
from .menu.menu import menu
from .reg_stage1.reg_stage1 import reg_stage1
from .reg_stage2.reg_stage2 import reg_stage2
from .reg_stage3.reg_stage3 import reg_stage3
from .inventory.inventory import inventory, detail



link  = {
    'menu'          : menu,
    'reg_stage1'    : reg_stage1,
    'reg_stage2'    : reg_stage2,
    'reg_stage3'    : reg_stage3,
    'test'          : test,
    'inventory'     : inventory,
    'detail'        : detail,
}


