from enum import Enum
from models import BinTree, LQNode, Point


class VType(Enum):
    Convex = 1
    Concave = 2
    LPivot = 3
    RPivot = 4
    ROnLineL = 5
    ROnLineR = 6
    LOnLineL = 7
    LOnLineR = 8


class LinkedQueue(BinTree):
    def __init__(self, items):
        node_ls = self.build_ls(items)
        self.ls_head = node_ls[0]
        super().__init__(node_ls[(len(node_ls) - 1) // 2])
        self.build_tree(self.root, node_ls)

    def list_of_nodes(self):
        node_ls = [self.ls_head]
        node = self.ls_head.l_right
        while node != self.ls_head:
            node_ls.append(node)
            node = node.l_right
        return node_ls

    @staticmethod
    def build_ls(items):
        node_ls = [LQNode(i) for i in items]
        for i in range(len(node_ls)):
            node_ls[i].l_left = node_ls[i - 1]
            node_ls[i].l_right = node_ls[(i + 1) % len(node_ls)]
        return node_ls

    @staticmethod
    def build_tree(node: LQNode, node_ls):
        mid = (len(node_ls) - 1) // 2
        l_ls, r_ls = node_ls[:mid], node_ls[mid + 1:]
        node.left, node.right = None, None
        if l_ls:
            node.left = l_ls[(len(l_ls) - 1) // 2]
            LinkedQueue.build_tree(node.left, l_ls)
        if r_ls:
            node.right = r_ls[(len(l_ls) - 1) // 2]
            LinkedQueue.build_tree(node.right, r_ls)

    def insert(self, item, l_node: LQNode, r_node: LQNode):
        n_node = LQNode(item, r_node, l_node)
        n = self.ls_head
        while n != r_node:
            if n == l_node:
                self.ls_head = l_node
                break
            n = n.l_right
        l_node.l_left, r_node.l_right = n_node, n_node
        node_ls = self.list_of_nodes()
        self.root = node_ls[(len(node_ls) - 1) // 2]
        self.build_tree(self.root, node_ls)

    @staticmethod
    def search_left(node: LQNode, point):
        hn = node
        while True:
            ln, rn = hn.l_left, hn.l_right
            t = LinkedQueue.v_type(point, hn.data, ln.data, rn.data)
            if t == VType.LPivot or t == VType.LOnLineR:
                return hn
            if t == VType.ROnLineR:
                return rn
            if t == VType.Concave:
                hn = hn.left if hn.left else ln
            else:
                hn = hn.right if hn.right else rn

    @staticmethod
    def search_right(node: LQNode, point):
        hn = node
        while True:
            ln, rn = hn.l_left, hn.l_right
            t = LinkedQueue.v_type(point, hn.data, ln.data, rn.data)
            if t == VType.RPivot or t == VType.ROnLineL:
                return hn
            if t == VType.LOnLineL:
                return ln
            if t == VType.Concave:
                hn = hn.right if hn.right else rn
            else:
                hn = hn.left if hn.left else ln

    @staticmethod
    def v_type(ep, hp, lp, rp):
        rp_dir, lp_dir = Point.direction(ep, hp, rp), Point.direction(ep, hp, lp)
        if rp_dir == 0:
            return VType.ROnLineR if lp_dir > 0 else VType.ROnLineL
        if lp_dir == 0:
            return VType.LOnLineR if rp_dir > 0 else VType.LOnLineL
        if lp_dir < 0:
            return VType.Concave if rp_dir > 0 else VType.RPivot
        return VType.LPivot if rp_dir > 0 else VType.Convex
