from models import BNode, LinkedQueue, VType, Point


class DynamicHull:
    def __init__(self, points):
        self.root = self.build(sorted(points))

    @staticmethod
    def __merge(lh, rh):
        l_target = [VType.RPivot, VType.BothOnLine, VType.ROnLineL]
        r_target = [VType.LPivot, VType.BothOnLine, VType.LOnLineR]
        for i in range(len(lh)):
            for j in reversed(range(len(rh))):
                lt = LinkedQueue.v_type(rh[j], lh[i], lh[i - 1], lh[(i + 1) % len(lh)])
                rt = LinkedQueue.v_type(lh[i], rh[j], rh[j - 1], rh[(j + 1) % len(rh)])
                if (lt in l_target) and (rt in r_target):
                    lh, rh = lh[:i + 1], rh[j:]
                    return [lh + rh, len(lh)]
        return [lh + rh, len(lh)]

    @staticmethod
    def height_of(node: BNode):
        return node.height if node else 0

    @staticmethod
    def balance_of(node: BNode):
        return DynamicHull.height_of(node.left) - DynamicHull.height_of(node.right) if node else 0

    @staticmethod
    def split_hull(node: BNode):
        if DynamicHull.height_of(node) > 1:
            split = node.data[2]
            lh, rh = node.data[1][:split], node.data[1][split:]
            if DynamicHull.height_of(node.left) > 1:
                node.left.data[1] = lh + node.left.data[1]
            if DynamicHull.height_of(node.right) > 1:
                node.right.data[1] = node.right.data[1] + rh

    @staticmethod
    def merge_hulls(node: BNode):
        node.height = 1 + max(DynamicHull.height_of(node.left), DynamicHull.height_of(node.right))
        left, right = node.left.data, node.right.data
        l_hull = [left[0]] if len(left) == 1 else left[1]
        r_hull = [right[0]] if len(right) == 1 else right[1]
        hull = DynamicHull.__merge(l_hull, r_hull)
        node.data = [l_hull[-1]] + hull
        if len(left) > 1:
            node.left.data[1] = node.left.data[1][hull[1]:]
        if len(right) > 1:
            node.right.data[1] = node.right.data[1][:hull[1] - len(hull[0])]

    @staticmethod
    def build(ls):
        node = BNode(ls)
        mid = len(ls) // 2
        if mid >= 1:
            node.left = DynamicHull.build(ls[:mid])
            node.right = DynamicHull.build(ls[mid:])
            DynamicHull.merge_hulls(node)
        return node

    @staticmethod
    def rotate_left(node: BNode):
        DynamicHull.split_hull(node)
        top = node.right
        DynamicHull.split_hull(top)
        node.right = top.left
        DynamicHull.merge_hulls(node)
        top.left = node
        DynamicHull.merge_hulls(top)
        return top

    @staticmethod
    def rotate_right(node: BNode):
        DynamicHull.split_hull(node)
        top = node.left
        DynamicHull.split_hull(top)
        node.left = top.right
        DynamicHull.merge_hulls(node)
        top.right = node
        DynamicHull.merge_hulls(top)
        return top

    @staticmethod
    def __insert(node: BNode, point: Point):
        if node is None or node.data[0] == point:
            return None
        if DynamicHull.height_of(node) == 1:
            hull = sorted([node.data[0], point])
            new_node = BNode([hull[0], hull, 1], 2)
            new_node.left, new_node.right = [BNode([p]) for p in hull]
            return new_node
        DynamicHull.split_hull(node)
        if point < node.data[0]:
            new_node = DynamicHull.__insert(node.left, point)
            if new_node is None:
                return None
            node.left = new_node
        else:
            new_node = DynamicHull.__insert(node.right, point)
            if new_node is None:
                return None
            node.right = new_node
        DynamicHull.merge_hulls(node)
        balance = DynamicHull.balance_of(node)
        if balance > 1 and point < node.left.data[0]:
            return DynamicHull.rotate_right(node)
        if balance < -1 and point > node.right.data[0]:
            return DynamicHull.rotate_left(node)
        if balance > 1 and point > node.left.data[0]:
            node.left = DynamicHull.rotate_left(node.left)
            return DynamicHull.rotate_right(node)
        if balance < -1 and point < node.right.data[0]:
            node.right = DynamicHull.rotate_right(node.right)
            return DynamicHull.rotate_left(node)
        return node

    def insert(self, point: Point):
        new_root = DynamicHull.__insert(self.root, point)
        if new_root is not None:
            self.root = new_root
            return True
        return False

    @staticmethod
    def __remove(node: BNode, point: Point):
        if node is None:
            return node, False
        if DynamicHull.height_of(node) == 1:
            return (None, True) if node.data[0] == point else (node, False)
        DynamicHull.split_hull(node)
        if point <= node.data[0]:
            new_node, mod = DynamicHull.__remove(node.left, point)
            if new_node is None:
                return node.right, mod
            node.left = new_node
        else:
            new_node, mod = DynamicHull.__remove(node.right, point)
            if new_node is None:
                return node.left, mod
            node.right = new_node
        DynamicHull.merge_hulls(node)
        balance = DynamicHull.balance_of(node)
        if balance > 1 and DynamicHull.balance_of(node.left) >= 0:
            return DynamicHull.rotate_right(node), mod
        if balance < -1 and DynamicHull.balance_of(node.right) <= 0:
            return DynamicHull.rotate_left(node), mod
        if balance > 1 and DynamicHull.balance_of(node.left) < 0:
            node.left = DynamicHull.rotate_left(node.left)
            return DynamicHull.rotate_right(node), mod
        if balance < -1 and DynamicHull.balance_of(node.right) > 0:
            node.right = DynamicHull.rotate_right(node.right)
            return DynamicHull.rotate_left(node), mod
        return node, mod

    def remove(self, point):
        new_root, mod = DynamicHull.__remove(self.root, point)
        if mod:
            self.root = new_root
            return True
        return False
