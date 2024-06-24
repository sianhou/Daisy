import inspect
import os
import sys
from collections import defaultdict

from core.node.dln import DLN


class OpList:
    _op_list = []

    @staticmethod
    def registerNode(node):
        if isinstance(node, list):
            OpList._op_list.extend(node)
        else:
            OpList._op_list.append(node)

        # 去除重复节点
        OpList._op_list = list(set(OpList._op_list))


class OpListHandle:

    @staticmethod
    def scan():
        op_list = []
        # inspect只能查看Live Modules, 也就是必须是import过的
        # 如果想自动扫描路径下的所有node，自动注册，只用inspect是不行的
        sub_modules = []
        path_folder = os.path.dirname(__file__) + './'
        for module in os.listdir(path_folder):
            if not module.endswith('.py') or module == '__init__.py' or module == 'optable.py':
                continue
            __import__(f'dlpkg.{module[:-3]}')
            sub_modules.append(f'dlpkg.{module[:-3]}')

        for moudule_name in sub_modules:
            for cls_name, cls in inspect.getmembers(sys.modules[moudule_name], inspect.isclass):
                if cls_name != 'DLN' and issubclass(cls, DLN):
                    op_list.append(cls)

        OpList.registerNode(op_list)

    @staticmethod
    def getRegisteredOps():
        return OpList._op_list

    @staticmethod
    def getRegisteredOpsJson():
        data = defaultdict(dict)
        for cls in OpListHandle.getRegisteredOps():
            pkg_name = cls.pkg_name
            op_title = cls.model_name
            data[pkg_name][op_title] = cls
        return data


if __name__ == '__main__':
    OpListHandle.scan()
    print(OpListHandle.getRegisteredOps())
    print(OpListHandle.getRegisteredOpsJson())
