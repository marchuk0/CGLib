from models import BinTree, Node


class LinkedQueue:
    def __init__(self, points):
        self.p = sorted(points)
        node_ls = self.build_ls(points)
        self.root = node_ls[(len(node_ls) - 1) // 2]
        self.build_tree(self.root, node_ls)

    @staticmethod
    def build_ls(points):
        node_ls = []
        for i in range(len(points)):
            node_ls.append(Node([points[i]]))
        for i in range(len(node_ls)):
            node_ls[i].data.append(node_ls[i - 1])
            node_ls[i].data.append(node_ls[(i + 1) % len(node_ls)])
        return node_ls

    @staticmethod
    def build_tree(node, node_ls):
        mid = (len(node_ls) - 1) // 2
        l_ls, r_ls = node_ls[:mid], node_ls[mid + 1:]
        if l_ls:
            node.left = l_ls[(len(l_ls) - 1) // 2]
            LinkedQueue.build_tree(node.left, l_ls)
        if r_ls:
            node.right = r_ls[(len(l_ls) - 1) // 2]
            LinkedQueue.build_tree(node.right, r_ls)

    def search_left(self, point):
        pass

    def search_right(self, point):
        pass

    def insert(self, p, l_node, r_node):
        pass
