from core.node.mininode import MiniNode


class DeepLearningNode(MiniNode):
    pkg_name = 'pytorch deep learning'
    op_name = ''

    def __init__(self, parent=None):
        super(DeepLearningNode, self).__init__(parent=parent)
