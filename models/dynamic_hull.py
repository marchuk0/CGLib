from models import Node, BinTree, LinkedQueue, VType


class DynamicHull(BinTree):
    def __init__(self, points):
        self.x_ordered = sorted(points)
        super().__init__(self.build(self.x_ordered))

    @staticmethod
    def merge_hulls(lh, rh):
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
    def build(ls):
        node = Node(ls)
        mid = len(ls) // 2
        if mid >= 1:
            l_ls, r_ls = ls[:mid], ls[mid:]
            node.left, node.right = DynamicHull.build(l_ls), DynamicHull.build(r_ls)
            left, right = node.left.data, node.right.data
            l_hull = [left[0]] if len(left) == 1 else left[1]
            r_hull = [right[0]] if len(right) == 1 else right[1]
            node.data = [l_hull[-1]]
            hull = [l_ls + r_ls, 1] if len(ls) == 2 else DynamicHull.merge_hulls(l_hull, r_hull)
            node.data.extend(hull)
            if len(left) > 1:
                node.left.data[1] = node.left.data[1][hull[1]:]
            if len(right) > 1:
                node.right.data[1] = node.right.data[1][:hull[1] - len(hull[0])]
        return node

    def add(self, point):
        res = point not in set(self.x_ordered)
        self.x_ordered = sorted(self.x_ordered + [point])
        self.root = self.build(self.x_ordered)
        return res

    def remove(self, point):
        res = point in set(self.x_ordered)
        self.x_ordered = sorted(list(set(self.x_ordered) - set([point])))
        self.root = self.build(self.x_ordered)
        return res
