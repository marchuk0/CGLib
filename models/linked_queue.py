from models import BinTree, Node, Point


class LinkedQueue(BinTree):
    def __init__(self, items):
        node_ls = self.build_ls(items)
        self.ls_head = node_ls[0]
        super().__init__(node_ls[(len(node_ls) - 1) // 2])
        self.build_tree(self.root, node_ls)

    def list_of_nodes(self):
        node_ls = [self.ls_head]
        node = self.ls_head.data[2]
        while node != self.ls_head:
            node_ls.append(node)
            node = node.data[2]
        return node_ls

    @staticmethod
    def build_ls(items):
        node_ls = []
        for i in range(len(items)):
            node_ls.append(Node([items[i]]))
        for i in range(len(node_ls)):
            node_ls[i].data.append(node_ls[i - 1])
            node_ls[i].data.append(node_ls[(i + 1) % len(node_ls)])
        return node_ls

    @staticmethod
    def build_tree(node: Node, node_ls):
        mid = (len(node_ls) - 1) // 2
        l_ls, r_ls = node_ls[:mid], node_ls[mid + 1:]
        if l_ls:
            node.left = l_ls[(len(l_ls) - 1) // 2]
            LinkedQueue.build_tree(node.left, l_ls)
        if r_ls:
            node.right = r_ls[(len(l_ls) - 1) // 2]
            LinkedQueue.build_tree(node.right, r_ls)

    @staticmethod
    def search_left(node: Node, point):
        hn = node
        while True:
            ln, rn = hn.data[1:]
            t = LinkedQueue.v_type(point, hn.data[0], ln.data[0], rn.data[0])
            if t == "ltan" or t == "lonr":
                return hn
            if t == "ronr":
                return rn
            if t == "conc":
                hn = hn.left if hn.left else ln
            else:
                hn = hn.right if hn.right else rn

    @staticmethod
    def search_right(node: Node, point):
        hn = node
        while True:
            ln, rn = hn.data[1:]
            t = LinkedQueue.v_type(point, hn.data[0], ln.data[0], rn.data[0])
            if t == "rtan" or t == "ronl":
                return hn
            if t == "lonl":
                return ln
            if t == "conc":
                hn = hn.right if hn.right else rn
            else:
                hn = hn.left if hn.left else ln

    def insert(self, item, l_node: Node, r_node: Node):
        if Point.direction(l_node.data[0], r_node.data[0], self.root.data[0]) > 0:
            l_node, r_node = r_node, l_node
        n_node = Node([item, r_node, l_node])
        n = self.ls_head
        while n != r_node:
            if n == l_node:
                self.ls_head = l_node
                break
            n = n.data[2]
        l_node.data[1], r_node.data[2] = n_node, n_node
        node_ls = self.list_of_nodes()
        self.root = node_ls[(len(node_ls) - 1) // 2]
        self.build_tree(self.root, node_ls)

    @staticmethod
    def v_type(ep, hp, lp, rp):
        rp_dir, lp_dir = Point.direction(ep, hp, rp), Point.direction(ep, hp, lp)
        if rp_dir == 0:
            return "ronr" if lp_dir > 0 else "ronl"
        if lp_dir == 0:
            return "lonr" if rp_dir > 0 else "lonl"
        if (lp_dir ^ rp_dir) < 0:
            return "conc" if rp_dir > 0 else "conv"
        return "ltan" if rp_dir > 0 else "rtan"
