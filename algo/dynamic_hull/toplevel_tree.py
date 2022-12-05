from typing import Optional

from models.concatenable_queue import ConcatenableQueue, Node, NodeType


class Point:
    def __init__(self):
        self.x_coord = 0
        self.y_coord = 0


class TreeNode:
    def __init__(self):
        self.p = None  # only leaf nodes have a point stored in them
        self.bridge1_lc = None
        self.bridge2_lc = None
        self.bridge1_rc = None
        self.bridge2_rc = None
        self.label = 0.0  # it is the y-coord of the point stored rightmost leaf of the subtree rooted on the left child
        self.Ql = None
        self.Qr = None
        self.leftchild = None
        self.rightchild = None
        self.parent = None
        self.balance_factor = 0


class BoolReference:
    def __init__(self, value: bool):
        self.value = value


class PointReference:
    def __init__(self, point: Point = None):
        self.value = point


class Tree:
    def __init__(self):
        self.root_ = None
        self.show_ = False

    def updateHull(self, current_node: TreeNode):
        self.updateBridgeHull(current_node, 0)
        self.updateBridgeHull(current_node, 1)
        lowerLcHull, aux1 = ConcatenableQueue.split_left(current_node.leftchild.Ql.clone(),
                                                         current_node.bridge1_lc.y_coord)
        lowerRcHull, aux3 = ConcatenableQueue.split_left(current_node.leftchild.Qr.clone(),
                                                         current_node.bridge1_rc.y_coord)
        current_node.leftchild.Ql = aux1
        current_node.leftchild.Qr = aux3
        aux2, upperLcHull = ConcatenableQueue.split_right(current_node.rightchild.Ql.clone(),
                                                          current_node.bridge2_lc.y_coord)
        aux4, upperRcHull = ConcatenableQueue.split_right(current_node.rightchild.Qr.clone(),
                                                          current_node.bridge2_rc.y_coord)
        current_node.rightchild.Ql = aux2
        current_node.rightchild.Qr = aux4
        completeLcHull = ConcatenableQueue.concatenate(lowerLcHull, upperLcHull)
        completeRcHull = ConcatenableQueue.concatenate(lowerRcHull, upperRcHull)
        current_node.Ql = completeLcHull
        current_node.Qr = completeRcHull

    # bridge lc hull operations

    def getPointsRightHalf(self, v_node: Node, p: PointReference, p0: PointReference, p1: PointReference) -> int:
        if v_node.left.type != NodeType.LEAF_NODE:
            flag = 0
            p.value.x_coord = v_node.right.smallest_y.x_coord
            p.value.y_coord = v_node.right.smallest_y.data2
            if v_node.type == NodeType.THREE_NODE:
                p0.value.x_coord = v_node.middle.biggest_y.x_coord
                p0.value.y_coord = v_node.middle.biggest_y.data2
            else:
                p0.value.x_coord = v_node.left.biggest_y.x_coord
                p0.value.y_coord = v_node.left.biggest_y.data2
            if v_node.right.smallest_y.parent.type == NodeType.THREE_NODE:
                p1.value.x_coord = v_node.right.smallest_y.parent.middle.x_coord
                p1.value.y_coord = v_node.right.smallest_y.parent.middle.data2
            else:
                p1.value.x_coord = v_node.right.smallest_y.parent.right.x_coord
                p1.value.y_coord = v_node.right.smallest_y.parent.right.data2
        else:
            p0.value.x_coord = v_node.left.x_coord
            p0.value.y_coord = v_node.left.data2
            if v_node.type == NodeType.THREE_NODE:
                p.value.x_coord = v_node.middle.x_coord
                p.value.y_coord = v_node.middle.data2
                p1.value.x_coord = v_node.right.x_coord
                p1.value.y_coord = v_node.right.data2
                flag = 0
            else:
                p.value.x_coord = v_node.right.x_coord
                p.value.y_coord = v_node.right.data2
                if v_node.parent is None:
                    flag = 1
                else:
                    if v_node.parent.right == v_node:
                        flag = 1
                    elif (v_node.parent.middle == v_node) or (v_node.parent.type == NodeType.TWO_NODE):
                        p1.value.x_coord = v_node.parent.right.smallest_y.x_coord
                        p1.value.y_coord = v_node.parent.right.smallest_y.data2
                        flag = 0
                    else:
                        p1.value.x_coord = v_node.parent.middle.smallest_y.x_coord
                        p1.value.y_coord = v_node.parent.middle.smallest_y.data2
                        flag = 0
        return flag

    def getPointsLeftHalf(self, v_node: Node, q: PointReference, q0: PointReference, q1: PointReference) -> int:
        if v_node.left.type != NodeType.LEAF_NODE:
            flag = 0
            q.value.x_coord = v_node.left.biggest_y.x_coord
            q.value.y_coord = v_node.left.biggest_y.data2
            if v_node.type == NodeType.THREE_NODE:
                q1.value.x_coord = v_node.middle.smallest_y.x_coord
                q1.value.y_coord = v_node.middle.smallest_y.data2
            else:
                q1.value.x_coord = v_node.right.smallest_y.x_coord
                q1.value.y_coord = v_node.right.smallest_y.data2
            if v_node.left.biggest_y.parent.type == NodeType.THREE_NODE:
                q0.value.x_coord = v_node.left.biggest_y.parent.middle.x_coord
                q0.value.y_coord = v_node.left.biggest_y.parent.middle.data2
            else:
                q0.value.x_coord = v_node.left.biggest_y.parent.left.x_coord
                q0.value.y_coord = v_node.left.biggest_y.parent.left.data2
        else:
            q1.value.x_coord = v_node.right.x_coord
            q1.value.y_coord = v_node.right.data2
            if v_node.type == NodeType.THREE_NODE:
                q.value.x_coord = v_node.middle.x_coord
                q.value.y_coord = v_node.middle.data2
                q0.value.x_coord = v_node.left.x_coord
                q0.value.y_coord = v_node.left.data2
                flag = 0
            else:
                q.value.x_coord = v_node.left.x_coord
                q.value.y_coord = v_node.left.data2
                if v_node.parent is None:
                    flag = 1
                else:
                    if v_node.parent.left == v_node:
                        flag = 1
                    elif (v_node.parent.middle == v_node) or (v_node.parent.type == NodeType.TWO_NODE):
                        q0.value.x_coord = v_node.parent.left.biggest_y.x_coord
                        q0.value.y_coord = v_node.parent.left.biggest_y.data2
                        flag = 0
                    else:
                        q0.value.x_coord = v_node.parent.middle.biggest_y.x_coord
                        q0.value.y_coord = v_node.parent.middle.biggest_y.data2
                        flag = 0
        return flag

    @staticmethod
    def rightTurn(p1: PointReference, p2: PointReference, p3: PointReference) -> int:
        cross_prod = ((p3.value.x_coord - p1.value.x_coord) * (p2.value.y_coord - p1.value.y_coord)) - \
                     ((p3.value.y_coord - p1.value.y_coord) * (p2.value.x_coord - p1.value.x_coord))
        if cross_prod == 0:
            return 2  # no turn (colinear points)
        elif cross_prod < 0:
            return 0  # turn left
        else:
            return 1  # turn right

    def case9(self, p: PointReference, p0: PointReference, p1: PointReference,
              q: PointReference, q0: PointReference, q1: PointReference,
              flag_lh: int, flag_uh: int) -> float:
        if flag_uh == 1:
            m2 = 0
        else:
            m2 = (p.value.y_coord - p1.value.y_coord) / (p.value.x_coord - p1.value.x_coord)

        if p0.value.x_coord != p.value.x_coord:
            m1 = (p0.value.y_coord - p.value.y_coord) / (p0.value.x_coord - p.value.x_coord)
            if m1 > 0:
                mp = m1 - ((m1 - m2) / 2)
            else:
                mp = m1 + ((m2 - m1) / 2)
        else:
            if m2 > 0:
                mp = m2 + 0.05
            else:
                mp = m2 - 0.05

        if flag_lh == 1:
            m1 = 0
        else:
            m1 = (q0.value.y_coord - q.value.y_coord) / (q0.value.x_coord - q.value.x_coord)

        if q.value.x_coord != q1.value.x_coord:
            m2 = (q.value.y_coord - q1.value.y_coord) / (q.value.x_coord - q1.value.x_coord)
            if m2 < 0:
                mq = m1 - ((m1 - m2) / 2)
            else:
                mq = m1 + ((m2 - m1) / 2)
        else:
            if m2 < 0:
                mq = m1 - 0.05
            else:
                mq = m1 + 0.05
        bp = p.value.y_coord - (mp * p.value.x_coord)
        bq = q.value.y_coord - (mq * q.value.x_coord)

        return ((mq * bp) - (mp * bq)) / (mq - mp)

    def bridgeCasesLcHull(self, p: PointReference, p0: PointReference, p1: PointReference,
                          q: PointReference, q0: PointReference, q1: PointReference,
                          half: float, flag_lh: int, flag_uh: int) -> int:
        if flag_lh == 0:
            chck_q0 = self.rightTurn(p, q, q0)
            chck_q1 = self.rightTurn(p, q, q1)
        elif flag_lh == 1:
            chck_q0 = 0
            chck_q1 = self.rightTurn(p, q, q1)
        else:
            chck_q0 = 0
            chck_q1 = 0
        if flag_uh == 0:
            chck_p0 = self.rightTurn(q, p, p0)
            chck_p1 = self.rightTurn(q, p, p1)
        elif flag_uh == 1:
            chck_p1 = 1
            chck_p0 = self.rightTurn(q, p, p0)
        else:
            chck_p0 = 1
            chck_p1 = 1
        if ((chck_p1 == 1) or (chck_p1 == 2)) and (chck_p0 == 1) and (chck_q1 == 0) and (
                (chck_q0 == 0) or (chck_q0 == 2)):
            return 1
        elif ((chck_p1 == 1) or (chck_p1 == 2)) and (chck_p0 == 1) and (chck_q1 == 0) and (chck_q0 == 1):
            return 2
        elif ((chck_p1 == 1) or (chck_p1 == 2)) and (chck_p0 == 1) and ((chck_q1 == 1) or (chck_q1 == 2)) and (
                (chck_q0 == 0) or (chck_q0 == 2)):
            return 3
        elif (chck_p1 == 0) and (chck_p0 == 1) and (chck_q1 == 0) and ((chck_q0 == 0) or (chck_q0 == 2)):
            return 4
        elif ((chck_p1 == 1) or (chck_p1 == 2)) and ((chck_p0 == 0) or (chck_p0 == 2)) and (chck_q1 == 0) and (
                (chck_q0 == 0) or (chck_q0 == 2)):
            return 5
        elif (chck_p1 == 0) and (chck_p0 == 1) and (chck_q1 == 0 or chck_q1 == 2) and (chck_q0 == 1):
            return 6
        elif (chck_p1 == 1) and (chck_p0 == 0) and (chck_q1 == 0) and (chck_q0 == 1):
            return 7
        elif (chck_p1 == 0) and (chck_p0 == 1) and (chck_q1 == 1) and (chck_q0 == 0):
            return 8
        elif (chck_p1 == 1) and (chck_p0 == 0) and (chck_q1 == 1) and (chck_q0 == 0):
            intersec = self.case9(p, p0, p1, q, q0, q1, flag_lh, flag_uh)
            if intersec < half:
                return 9
            else:
                return 10
        print("ERROR in LcHull bridge case: chck_p0={}  chck_p1={}  chck_q1={}  chck_q0={}".format(chck_p0, chck_p1,
                                                                                                   chck_q1, chck_q0))
        print("p0=({},{}) p=({},{}) p1=({},{})".format(p0.value.x_coord, p0.value.y_coord, p.value.x_coord,
                                                       p.value.y_coord, p1.value.x_coord, p1.value.y_coord))
        print("q0=({},{}) q=({},{}) q1=({},{})".format(q0.value.x_coord, q0.value.y_coord, q.value.x_coord,
                                                       q.value.y_coord, q1.value.x_coord, q1.value.y_coord))

    def bridgeCasesRcHull(self, p: PointReference, p0: PointReference, p1: PointReference,
                          q: PointReference, q0: PointReference, q1: PointReference,
                          half: float, flag_lh: int, flag_uh: int) -> int:
        if flag_lh == 0:
            chck_q0 = self.rightTurn(p, q, q0)
            chck_q1 = self.rightTurn(p, q, q1)
        elif flag_lh == 1:
            chck_q0 = 1
            chck_q1 = self.rightTurn(p, q, q1)
        else:
            chck_q0 = 1
            chck_q1 = 1
        if flag_uh == 0:
            chck_p0 = self.rightTurn(q, p, p0)
            chck_p1 = self.rightTurn(q, p, p1)
        elif flag_uh == 1:
            chck_p1 = 0
            chck_p0 = self.rightTurn(q, p, p0)
        else:
            chck_p0 = 0
            chck_p1 = 0
        if ((chck_p1 == 0) or (chck_p1 == 2)) and (chck_p0 == 0) and (chck_q1 == 1) and (
                (chck_q0 == 1) or (chck_q0 == 2)):
            return 1
        elif ((chck_p1 == 0) or (chck_p1 == 2)) and (chck_p0 == 0) and (chck_q1 == 1) and (chck_q0 == 0):
            return 2
        elif ((chck_p1 == 0) or (chck_p1 == 2)) and (chck_p0 == 0) and ((chck_q1 == 0) or (chck_q1 == 2)) and (
                (chck_q0 == 1) or (chck_q0 == 2)):
            return 3
        elif (chck_p1 == 1) and (chck_p0 == 0) and (chck_q1 == 1) and ((chck_q0 == 1) or (chck_q0 == 2)):
            return 4
        elif ((chck_p1 == 0) or (chck_p1 == 2)) and ((chck_p0 == 1) or (chck_p0 == 2)) and (chck_q1 == 1) and (
                (chck_q0 == 1) or (chck_q0 == 2)):
            return 5
        elif (chck_p1 == 1) and (chck_p0 == 0) and (chck_q1 == 1 or chck_q1 == 2) and (chck_q0 == 0):
            return 6
        elif (chck_p1 == 0) and (chck_p0 == 1) and (chck_q1 == 1) and (chck_q0 == 0):
            return 7
        elif (chck_p1 == 1) and (chck_p0 == 0) and (chck_q1 == 0) and (chck_q0 == 1):
            return 8
        elif (chck_p1 == 0) and (chck_p0 == 1) and (chck_q1 == 0) and (chck_q0 == 1):
            intersec = self.case9(p, p0, p1, q, q0, q1, flag_lh, flag_uh)
            if intersec < half:
                return 9
            else:
                return 10
        print("ERROR in RcHull bridge case: chck_p0={}  chck_p1={}  chck_q1={}  chck_q0={}".format(chck_p0, chck_p1,
                                                                                                   chck_q1, chck_q0))
        print("p0=({},{}) p=({},{}) p1=({},{})".format(p0.value.x_coord, p0.value.y_coord, p.value.x_coord,
                                                       p.value.y_coord, p1.value.x_coord, p1.value.y_coord))
        print("q0=({},{}) q=({},{}) q1=({},{})".format(q0.value.x_coord, q0.value.y_coord, q.value.x_coord,
                                                       q.value.y_coord, q1.value.x_coord, q1.value.y_coord))

    def newSSLhLeft(self, current: Node, q: PointReference, q0: PointReference, q1: PointReference,
                    onepoint: BoolReference) -> Optional[Node]:
        if current.type == NodeType.LEAF_NODE:
            if not onepoint.value:
                onepoint.value = True
                if current.parent is not None:
                    if current.parent.right == current:
                        q1.value.y_coord = q.value.y_coord
                        q1.value.x_coord = q.value.x_coord
                        if current.parent.type == NodeType.THREE_NODE:
                            q.value.y_coord = current.parent.middle.data2
                            q.value.x_coord = current.parent.middle.x_coord
                        else:
                            q.value.y_coord = current.parent.left.data2
                            q.value.x_coord = current.parent.left.x_coord
                        onepoint.value = False
            return None
        elif current.left.type == NodeType.LEAF_NODE:
            if current.type == NodeType.THREE_NODE:
                q1.value = q.value
                onepoint.value = False
            else:
                onepoint.value = True
            q.value.x_coord = current.left.x_coord
            q.value.y_coord = current.left.data2
            return current.left
        elif q.value.y_coord == current.left.biggest_y.data2:
            return current.left
        elif q.value.y_coord == current.right.smallest_y.data2:
            q1.value = q.value
            q.value = q0
            onepoint.value = False
            return current.right.smallest_y
        else:
            if q.value.y_coord == current.middle.smallest_y.data2:
                q1.value = q
                q.value = q0
                onepoint.value = False
                return current.right.smallest_y
            else:
                return current.middle

    def newSSUhRight(self, current: Node, p: PointReference, p0: PointReference, p1: PointReference,
                     onepoint: BoolReference) -> Optional[Node]:
        if current.type == NodeType.LEAF_NODE:
            if not onepoint.value:
                onepoint.value = True
                if current.parent is not None:
                    if current.parent.left == current:
                        p0.value = p
                        if current.parent.type == NodeType.THREE_NODE:
                            p.value.y_coord = current.parent.middle.data2
                            p.value.x_coord = current.parent.middle.x_coord
                        else:
                            p.value.y_coord = current.parent.right.data2
                            p.value.x_coord = current.parent.right.x_coord
                        onepoint.value = False
            return None
        elif current.right.type == NodeType.LEAF_NODE:
            if current.type == NodeType.THREE_NODE:
                p0.value = p.value
                onepoint.value = False
            else:
                onepoint.value = True
            p.value.x_coord = current.right.x_coord
            p.value.y_coord = current.right.data2
            return current.right
        elif p.value.y_coord == current.right.smallest_y.data2:
            return current.right
        elif p.value.y_coord == current.left.biggest_y.data2:
            p0.value = p.value
            p.value = p1.value
            onepoint.value = False
            return current.left.biggest_y
        else:
            if p.value.y_coord == current.middle.biggest_y.data2:
                p0.value = p.value
                p.value = p1.value
                onepoint.value = False
                return current.middle.biggest_y
            else:
                return current.middle

    def newSSLhRight(self, current: Node, q: PointReference, q0: PointReference, q1: PointReference,
                     onepoint: BoolReference, out: BoolReference) -> Optional[Node]:
        newcurrent = None
        if current.type == NodeType.LEAF_NODE:
            out.value = True
        elif current.left.type == NodeType.LEAF_NODE:
            onepoint.value = False
            out.value = True
            newcurrent = current.right
        elif q.value.y_coord == current.right.smallest_y.data2:
            newcurrent = current.right
            out.value = True
        elif current.type == NodeType.THREE_NODE:
            aux = q1.value
            if q.value.y_coord == current.left.biggest_y.data2:
                if current.middle.smallest_y.parent.type == NodeType.THREE_NODE:
                    q1.value.x_coord = current.middle.smallest_y.parent.middle.x_coord
                    q1.value.y_coord = current.middle.smallest_y.parent.middle.data2
                else:
                    q1.value.x_coord = current.middle.smallest_y.parent.right.x_coord
                    q1.value.y_coord = current.middle.smallest_y.parent.right.data2
                q0.value = q.value
                q.value = aux
            elif q.value.y_coord == current.middle.smallest_y.data2:
                q1.value.x_coord = current.right.smallest_y.x_coord
                q1.value.y_coord = current.right.smallest_y.data2
                q.value.x_coord = current.middle.biggest_y.x_coord
                q.value.y_coord = current.middle.biggest_y.data2
                if current.middle.biggest_y.parent.type == NodeType.THREE_NODE:
                    q0.value.x_coord = current.middle.biggest_y.parent.middle.x_coord
                    q0.value.y_coord = current.middle.biggest_y.parent.middle.data2
                else:
                    q0.value.x_coord = current.middle.biggest_y.parent.left.x_coord
                    q0.value.y_coord = current.middle.biggest_y.parent.left.data2
            else:
                if current.right.smallest_y.parent.type == NodeType.THREE_NODE:
                    q1.value.x_coord = current.right.smallest_y.parent.middle.x_coord
                    q1.value.y_coord = current.right.smallest_y.parent.middle.data2
                else:
                    q1.value.x_coord = current.right.smallest_y.parent.right.x_coord
                    q1.value.y_coord = current.right.smallest_y.parent.right.data2
                q0.value.value = q.value
                q.value.value = aux
        else:
            aux = q1.value
            if current.right.smallest_y.parent.type == NodeType.THREE_NODE:
                q1.value.x_coord = current.right.smallest_y.parent.middle.x_coord
                q1.value.y_coord = current.right.smallest_y.parent.middle.data2
            else:
                q1.value.x_coord = current.right.smallest_y.parent.right.x_coord
                q1.value.y_coord = current.right.smallest_y.parent.right.data2
            q0.value = q.value
            q.value = aux
        return newcurrent

    def newSSUhLeft(self, current: Node, p: PointReference, p0: PointReference, p1: PointReference,
                    onepoint: BoolReference, out: BoolReference) -> Optional[Node]:
        newcurrent = None
        if current.type == NodeType.LEAF_NODE:
            out.value = True
        elif current.left.type == NodeType.LEAF_NODE:
            onepoint.value = False
            out.value = True
            newcurrent = current.left
        elif p.value.y_coord == current.left.biggest_y.data2:
            newcurrent = current.left
            out.value = True
        elif current.type == NodeType.THREE_NODE:
            aux = p0.value
            if p.value.y_coord == current.right.smallest_y.data2:
                if current.middle.biggest_y.parent.type == NodeType.THREE_NODE:
                    p0.value.x_coord = current.middle.biggest_y.parent.middle.x_coord
                    p0.value.y_coord = current.middle.biggest_y.parent.middle.data2
                else:
                    p0.value.x_coord = current.middle.biggest_y.parent.left.x_coord
                    p0.value.y_coord = current.middle.biggest_y.parent.left.data2

                p1.value = p.value
                p.value = aux
            elif p.value.y_coord == current.middle.biggest_y.data2:
                p0.value.x_coord = current.left.biggest_y.x_coord
                p0.value.y_coord = current.left.biggest_y.data2
                p.value.x_coord = current.middle.smallest_y.x_coord
                p.value.y_coord = current.middle.smallest_y.data2
                if current.middle.smallest_y.parent.type == NodeType.THREE_NODE:
                    p1.value.x_coord = current.middle.smallest_y.parent.middle.x_coord
                    p1.value.y_coord = current.middle.smallest_y.parent.middle.data2
                else:
                    p1.value.x_coord = current.middle.smallest_y.parent.right.x_coord
                    p1.value.y_coord = current.middle.smallest_y.parent.right.data2
            else:
                if current.left.biggest_y.parent.type == NodeType.THREE_NODE:
                    p0.value.x_coord = current.left.biggest_y.parent.middle.x_coord
                    p0.value.y_coord = current.left.biggest_y.parent.middle.data2
                else:
                    p0.value.x_coord = current.left.biggest_y.parent.left.x_coord
                    p0.y_coord = current.left.biggest_y.parent.left.data2
                p1.value = p.value
                p.value = aux
        else:
            aux = p0.value
            if current.left.smallest_y.parent.type == NodeType.THREE_NODE:
                p0.value.x_coord = current.left.smallest_y.parent.middle.x_coord
                p0.value.y_coord = current.left.smallest_y.parent.middle.data2
            else:
                p0.value.x_coord = current.left.smallest_y.parent.left.x_coord
                p0.value.y_coord = current.left.smallest_y.parent.left.data2
            p1.value = p.value
            p.value = aux
        return newcurrent

    def buildChildrensHulls(self, parent_node: TreeNode) -> None:
        lowerLcHull, upperLcHull = ConcatenableQueue.split_right(parent_node.Ql.clone(), parent_node.bridge2_lc.y_coord)
        lowerRcHull, upperRcHull = ConcatenableQueue.split_right(parent_node.Qr.clone(), parent_node.bridge2_rc.y_coord)
        completeUpperLcHull = ConcatenableQueue.concatenate(parent_node.rightchild.Ql, upperLcHull)
        completeUpperRcHull = ConcatenableQueue.concatenate(parent_node.rightchild.Qr, upperRcHull)
        completeLowerLcHull = ConcatenableQueue.concatenate(lowerLcHull, parent_node.leftchild.Ql)
        completeLowerRcHull = ConcatenableQueue.concatenate(lowerRcHull, parent_node.leftchild.Qr)
        parent_node.rightchild.Ql = completeUpperLcHull
        parent_node.leftchild.Ql = completeLowerLcHull
        parent_node.rightchild.Qr = completeUpperRcHull
        parent_node.leftchild.Qr = completeLowerRcHull

    def updateBridgeHull(self, v_node: TreeNode, hull: int) -> None:
        # bool bridgefound, onepoint_lh, onepoint_uh, out
        # double half
        # int chk_case, flag_lh = 0, flag_uh = 0
        p, p0, p1 = PointReference(Point()), PointReference(Point()), PointReference(Point())
        q, q0, q1 = PointReference(Point()), PointReference(Point()), PointReference(Point())
        # node *current_lh, *current_uh, *aux
        bridgefound = False
        onepoint_lh = BoolReference(True)
        onepoint_uh = BoolReference(True)
        if hull == 0:
            current_lh = v_node.leftchild.Ql.root()
            current_uh = v_node.rightchild.Ql.root()
        else:
            current_lh = v_node.leftchild.Qr.root()
            current_uh = v_node.rightchild.Qr.root()
        if (current_lh.type != NodeType.LEAF_NODE) and (current_uh.type != NodeType.LEAF_NODE):
            half = current_uh.smallest_y.data2 - ((current_uh.smallest_y.data2 - current_lh.biggest_y.data2) / 2)
        elif current_lh.type != NodeType.LEAF_NODE:
            half = current_uh.data2 - ((current_uh.data2 - current_lh.biggest_y.data2) / 2)
        elif current_uh.type != NodeType.LEAF_NODE:
            half = current_uh.smallest_y.data2 - ((current_uh.smallest_y.data2 - current_lh.data2) / 2)
        else:
            half = current_uh.data2 - ((current_uh.data2 - current_lh.data2) / 2)
        p.value.x_coord = current_uh.x_coord
        p.value.y_coord = current_uh.data2
        q.value.x_coord = current_lh.x_coord
        q.value.y_coord = current_lh.data2
        while not bridgefound:
            if (current_lh.type == NodeType.LEAF_NODE) and (current_uh.type == NodeType.LEAF_NODE):
                if onepoint_lh.value and onepoint_uh.value:
                    bridgefound = True
                elif onepoint_lh.value:
                    if hull == 0:
                        chk_case = self.bridgeCasesLcHull(p, p0, p1, q, q0, q1, half, 2, 1)
                    else:
                        chk_case = self.bridgeCasesRcHull(p, p0, p1, q, q0, q1, half, 2, 1)
                    if chk_case != 1:
                        p = p0
                    bridgefound = True
                elif onepoint_uh:
                    if hull == 0:
                        chk_case = self.bridgeCasesLcHull(p, p0, p1, q, q0, q1, half, 1, 2)
                    else:
                        chk_case = self.bridgeCasesRcHull(p, p0, p1, q, q0, q1, half, 1, 2)
                    if chk_case != 1:
                        q = q1
                    bridgefound = True
                else:
                    if hull == 0:
                        chk_case = self.bridgeCasesLcHull(p, p0, p1, q, q0, q1, half, 1, 1)
                    else:
                        chk_case = self.bridgeCasesRcHull(p, p0, p1, q, q0, q1, half, 1, 1)
                    if chk_case != 1:
                        if hull == 0:
                            chk_case = self.bridgeCasesLcHull(p0, p, p1, q, q0, q1, half, 1, 2)
                        else:
                            chk_case = self.bridgeCasesRcHull(p0, p, p1, q, q0, q1, half, 1, 2)
                        if chk_case != 1:
                            if hull == 0:
                                chk_case = self.bridgeCasesLcHull(p, p0, p1, q1, q0, q, half, 2, 1)
                            else:
                                chk_case = self.bridgeCasesRcHull(p, p0, p1, q1, q0, q, half, 2, 1)
                            if chk_case != 1:
                                p = p0
                                q = q1
                            else:
                                q = q1
                        else:
                            p = p0
                    bridgefound = True
            else:
                if current_uh.type == NodeType.LEAF_NODE:
                    flag_lh = self.getPointsLeftHalf(current_lh, q, q0, q1)
                    if onepoint_uh.value:
                        flag_uh = 2
                    else:
                        flag_uh = 1
                elif current_lh.type == NodeType.LEAF_NODE:
                    flag_uh = self.getPointsRightHalf(current_uh, p, p0, p1)
                    if onepoint_lh.value:
                        flag_lh = 2
                    else:
                        flag_lh = 1
                else:
                    flag_lh = self.getPointsLeftHalf(current_lh, q, q0, q1)
                    flag_uh = self.getPointsRightHalf(current_uh, p, p0, p1)
                out = BoolReference(False)
                while not out.value:
                    if hull == 0:
                        chk_case = self.bridgeCasesLcHull(p, p0, p1, q, q0, q1, half, flag_lh, flag_uh)
                    else:
                        chk_case = self.bridgeCasesRcHull(p, p0, p1, q, q0, q1, half, flag_lh, flag_uh)
                    if chk_case == 1:
                        bridgefound = True
                        out.value = True
                    elif chk_case == 2 or chk_case == 4 or chk_case == 6:
                        aux = self.newSSLhLeft(current_lh, q, q0, q1, onepoint_lh)
                        if aux is not None:
                            current_lh = aux
                        aux = self.newSSUhRight(current_uh, p, p0, p1, onepoint_uh)
                        if aux is not None:
                            current_uh = aux
                        out.value = True
                    elif chk_case == 7:
                        aux = self.newSSLhLeft(current_lh, q, q0, q1, onepoint_lh)
                        if aux is not None:
                            current_lh = aux
                        out.value = True
                    elif chk_case == 8:
                        aux = self.newSSUhRight(current_uh, p, p0, p1, onepoint_uh)
                        if aux is not None:
                            current_uh = aux
                        out.value = True
                    elif chk_case == 3:
                        aux = self.newSSLhRight(current_lh, q, q0, q1, onepoint_lh, out)
                        if aux is not None:
                            current_lh = aux
                        if out.value:
                            aux = self.newSSUhRight(current_uh, p, p0, p1, onepoint_uh)
                            if aux is not None:
                                current_uh = aux
                    elif chk_case == 5:
                        aux = self.newSSUhLeft(current_uh, p, p0, p1, onepoint_uh, out)
                        if aux is not None:
                            current_uh = aux
                        if out.value:
                            aux = self.newSSLhLeft(current_lh, q, q0, q1, onepoint_lh)
                            if aux is not None:
                                current_lh = aux
                    elif chk_case == 9:
                        aux = self.newSSLhRight(current_lh, q, q0, q1, onepoint_lh, out)
                        if aux is not None:
                            current_lh = aux
                        if (current_lh.type == NodeType.LEAF_NODE) and (current_uh.type != NodeType.LEAF_NODE):
                            out.value = False
                            flag_lh = 2
                            q.value.y_coord = q1.value.y_coord
                            q.value.x_coord = q1.value.x_coord
                    elif chk_case == 10:
                        aux = self.newSSUhLeft(current_uh, p, p0, p1, onepoint_uh, out)
                        if aux is not None:
                            current_uh = aux
                        if (current_uh.type == NodeType.LEAF_NODE) and (current_lh.type != NodeType.LEAF_NODE):
                            out.value = False
                            flag_uh = 2
                            p.value.y_coord = p0.value.y_coord
                            p.value.x_coord = p0.value.x_coord
        if hull == 0:
            v_node.bridge1_lc = q.value
            v_node.bridge2_lc = p.value
        else:
            v_node.bridge1_rc = q.value
            v_node.bridge2_rc = p.value

    def createLabel(self, new_label: float, left_child: TreeNode, right_child: TreeNode) -> TreeNode:
        new_node = TreeNode()
        new_node.label = new_label
        new_node.Ql = ConcatenableQueue.concatenate(left_child.Ql, right_child.Ql)
        new_node.Qr = ConcatenableQueue.concatenate(left_child.Qr, right_child.Qr)
        new_node.bridge1_lc = left_child.p
        new_node.bridge2_lc = right_child.p
        new_node.bridge1_rc = left_child.p
        new_node.bridge2_rc = right_child.p
        left_child.Ql.set_root(None)
        right_child.Ql.set_root(None)
        left_child.Qr.set_root(None)
        right_child.Qr.set_root(None)
        new_node.leftchild = None
        new_node.rightchild = None
        new_node.parent = None
        new_node.balance_factor = 0
        return new_node

    def createObject(self, new_point: Point) -> TreeNode:
        lc_hull = ConcatenableQueue()
        lc_hull.add_node(new_point.x_coord, new_point.y_coord)
        rc_hull = ConcatenableQueue()
        rc_hull.add_node(new_point.x_coord, new_point.y_coord)

        new_node = TreeNode()
        new_node.p = new_point
        new_node.label = new_point.y_coord
        new_node.Ql = lc_hull
        new_node.Qr = rc_hull
        new_node.leftchild = None
        new_node.rightchild = None
        new_node.parent = None
        new_node.balance_factor = 0
        return new_node

    def anticlockwiseRotation(self, z_node: TreeNode) -> None:
        y_node = z_node.rightchild
        z_node.rightchild = y_node.leftchild
        y_node.leftchild.parent = z_node
        y_node.leftchild = z_node
        if z_node == self.root_:
            y_node.parent = None
            self.root_ = y_node
        elif z_node == z_node.parent.leftchild:
            z_node.parent.leftchild = y_node
            y_node.parent = z_node.parent
        else:
            y_node.parent = z_node.parent
            z_node.parent.rightchild = y_node

        z_node.parent = y_node
        if y_node.balance_factor == 1:
            z_node.balance_factor = 0
            y_node.balance_factor = 0
        else:
            z_node.balance_factor = 1
            y_node.balance_factor = -1

    def clockwiseRotation(self, z_node: TreeNode) -> None:
        y_node = z_node.leftchild
        z_node.leftchild = y_node.rightchild
        y_node.rightchild.parent = z_node
        y_node.rightchild = z_node
        if z_node == self.root_:
            y_node.parent = None
            self.root_ = y_node
        elif z_node == z_node.parent.leftchild:
            z_node.parent.leftchild = y_node
            y_node.parent = z_node.parent
        else:
            z_node.parent.rightchild = y_node
            y_node.parent = z_node.parent
        z_node.parent = y_node
        if y_node.balance_factor == -1:
            z_node.balance_factor = 0
            y_node.balance_factor = 0
        else:
            z_node.balance_factor = -1
            y_node.balance_factor = 1

    def clockwiseAnticlockDoubleRotation(self, z_node: TreeNode) -> None:
        y_node = z_node.rightchild
        x_node = y_node.leftchild
        z_node.rightchild = x_node.leftchild
        x_node.leftchild.parent = z_node
        y_node.leftchild = x_node.rightchild
        x_node.rightchild.parent = y_node
        x_node.rightchild = y_node
        y_node.parent = x_node
        x_node.parent = z_node.parent
        x_node.leftchild = z_node
        if z_node == self.root_:
            self.root_ = x_node
        elif z_node.parent.leftchild == z_node:
            z_node.parent.leftchild = x_node
        else:
            z_node.parent.rightchild = x_node
        z_node.parent = x_node
        if x_node.balance_factor == 0:
            y_node.balance_factor = 0
            z_node.balance_factor = 0
        elif x_node.balance_factor == 1:
            y_node.balance_factor = 0
            z_node.balance_factor = -1
        else:
            y_node.balance_factor = 1
            z_node.balance_factor = 0
        x_node.balance_factor = 0

    def anticlockwiseClockDoubleRotation(self, z_node: TreeNode) -> None:
        y_node = z_node.leftchild
        x_node = y_node.rightchild
        z_node.leftchild = x_node.rightchild
        x_node.rightchild.parent = z_node
        y_node.rightchild = x_node.leftchild
        x_node.leftchild.parent = y_node
        x_node.leftchild = y_node
        y_node.parent = x_node
        x_node.parent = z_node.parent
        x_node.rightchild = z_node
        if z_node == self.root_:
            self.root_ = x_node
        elif z_node.parent.leftchild == z_node:
            z_node.parent.leftchild = x_node
        else:
            z_node.parent.rightchild = x_node
        z_node.parent = x_node
        if x_node.balance_factor == 0:
            y_node.balance_factor = 0
            z_node.balance_factor = 0
        elif x_node.balance_factor == 1:
            y_node.balance_factor = -1
            z_node.balance_factor = 0
        else:
            y_node.balance_factor = 0
            z_node.balance_factor = 1
        x_node.balance_factor = 0

    def add_Node(self, new_point: Point) -> None:
        right = False
        new_node = self.createObject(new_point)
        if self.root_ is None:
            self.root_ = new_node
        else:
            current = self.root_
            i = 1
            while current.leftchild is not None:
                self.buildChildrensHulls(current)
                if self.show_:
                    print("The lc hull of the lower half at level {}".format(i))
                    current.leftchild.Ql.print()
                    print("The rc hull of the lower half at level {}".format(i))
                    current.leftchild.Qr.print()
                    print("The lc hull of the upper half at level {}".format(i))
                    current.rightchild.Ql.print()
                    print("The rc hull of the upper half at level {}".format(i))
                    current.rightchild.Qr.print()
                if new_node.label <= current.label:
                    current = current.leftchild
                else:
                    current = current.rightchild
                i += 1
            if current == self.root_:
                if current.label <= new_node.label:
                    new_label_node = self.createLabel(current.label, current, new_node)
                    new_label_node.leftchild = current
                    new_label_node.rightchild = new_node
                    new_node.parent = new_label_node
                    new_label_node.leftchild.parent = new_label_node
                else:
                    new_label_node = self.createLabel(new_node.label, new_node, current)
                    new_label_node.rightchild = current
                    new_label_node.leftchild = new_node
                    new_node.parent = new_label_node
                    new_label_node.rightchild.parent = new_label_node
                self.root_ = new_label_node
            else:
                parent = current.parent
                if current.label <= new_node.label:
                    new_label_node = self.createLabel(current.label, current, new_node)
                    new_label_node.leftchild = current
                    new_label_node.rightchild = new_node
                    new_node.parent = new_label_node
                    new_label_node.leftchild.parent = new_label_node
                else:
                    new_label_node = self.createLabel(new_node.label, new_node, current)
                    new_label_node.rightchild = current
                    new_label_node.leftchild = new_node
                    new_node.parent = new_label_node
                    new_label_node.rightchild.parent = new_label_node
                if parent.rightchild == current:
                    parent.rightchild = new_label_node
                    right = True
                else:
                    parent.leftchild = new_label_node
                    right = False
                current.parent = new_label_node
                new_label_node.parent = parent
            self.updateBalanceFactor(new_label_node.parent, right)

    def updateBalanceFactor(self, current: TreeNode, right: bool) -> None:
        updatelabel = True
        while current is not None:
            if right:
                if updatelabel:
                    current.balance_factor += 1
                if current.balance_factor == 2:
                    if current.rightchild.balance_factor == -1:
                        self.buildChildrensHulls(current.rightchild)
                        self.buildChildrensHulls(current.rightchild.leftchild)
                        self.clockwiseAnticlockDoubleRotation(current)
                        self.updateHull(current)
                        self.updateHull(current.parent.rightchild)
                    else:
                        self.buildChildrensHulls(current.rightchild)
                        self.anticlockwiseRotation(current)
                        self.updateHull(current)
                    updatelabel = False
                    current = current.parent
                    self.updateHull(current)
                else:
                    self.updateHull(current)
            else:
                if updatelabel:
                    current.balance_factor -= 1
                if current.balance_factor == -2:
                    if current.leftchild.balance_factor == 1:
                        self.buildChildrensHulls(current.leftchild)
                        self.buildChildrensHulls(current.leftchild.rightchild)
                        self.anticlockwiseClockDoubleRotation(current)
                        self.updateHull(current)
                        self.updateHull(current.parent.leftchild)
                    else:
                        self.buildChildrensHulls(current.leftchild)
                        self.clockwiseRotation(current)
                        self.updateHull(current)
                    updatelabel = False
                    current = current.parent
                    self.updateHull(current)
                else:
                    self.updateHull(current)
            if (current == self.root_) or (current.balance_factor == 0):
                updatelabel = False
            elif current == current.parent.rightchild:
                right = True
            else:
                right = False
            if self.show_:
                print("The updated lc-hull of the node with label  {}".format(current.label))
                current.Ql.print()
                print("The updated rc-hull of the node with label   {}".format(current.label))
                current.Qr.print()
            current = current.parent

    def delete_Node(self, point_to_delete: Point) -> None:
        # bool right, uLabel, update
        node_to_delete = self.search_Node(point_to_delete)
        if node_to_delete is not None:
            if node_to_delete == self.root_:
                # TODO: (check if root has to be deleted
                self.root_ = None
            else:
                parent = node_to_delete.parent
                if parent == self.root_:
                    if parent.rightchild == node_to_delete:
                        self.root_ = parent.leftchild
                    else:
                        self.root_ = parent.rightchild
                    self.root_.parent = None
                else:
                    if parent.rightchild == node_to_delete:
                        brother = parent.leftchild
                        uLabel = True
                        update = False
                    else:
                        brother = parent.rightchild
                        uLabel = False
                        update = True
                    if parent.parent.rightchild == parent:
                        parent.parent.rightchild = brother
                        right = True
                    else:
                        right = False
                        parent.parent.leftchild = brother
                    brother.parent = parent.parent
                    if parent.parent.parent is not None:
                        if (parent.parent.parent.rightchild == parent.parent) and right:
                            uLabel = False
                        elif not right:
                            uLabel = True
                        else:
                            uLabel = False
                    if brother.rightchild is None:
                        self.updateBalanceFactorDelete(parent.parent, right, uLabel, update, brother.label)
                    else:
                        self.updateBalanceFactorDelete(parent.parent, right, uLabel, update, brother.rightchild.label)

    def updateBalanceFactorDelete(self, current: TreeNode, right: bool, update_label: bool, update_label_done: bool,
                                  label: float) -> None:
        updateBF = True
        while current is not None:
            balanced = False
            if update_label and (not update_label_done):
                current.label = label
                update_label_done = True
            if right:
                if updateBF:
                    current.balance_factor -= 1
                if current.balance_factor == -2:
                    if current.leftchild.balance_factor == 1:
                        self.buildChildrensHulls(current.leftchild)
                        self.buildChildrensHulls(current.leftchild.rightchild)
                        self.anticlockwiseClockDoubleRotation(current)
                        self.updateHull(current)
                        self.updateHull(current.parent.leftchild)
                        balanced = True
                    elif current.leftchild.balance_factor == -1:
                        self.buildChildrensHulls(current.leftchild)
                        self.clockwiseRotation(current)
                        self.updateHull(current)
                        balanced = True
                    else:
                        self.buildChildrensHulls(current.leftchild)
                        self.clockwiseRotation(current)
                        self.updateHull(current)
                    current = current.parent
                    self.updateHull(current)
                else:
                    self.updateHull(current)
            else:
                if updateBF:
                    current.balance_factor += 1
                if current.balance_factor == 2:
                    if current.rightchild.balance_factor == -1:
                        self.buildChildrensHulls(current.rightchild)
                        self.buildChildrensHulls(current.rightchild.leftchild)
                        self.clockwiseAnticlockDoubleRotation(current)
                        self.updateHull(current)
                        self.updateHull(current.parent.rightchild)
                        balanced = True
                    elif current.rightchild.balance_factor == 1:
                        self.buildChildrensHulls(current.rightchild)
                        self.anticlockwiseRotation(current)
                        self.updateHull(current)
                        balanced = True
                    else:
                        self.buildChildrensHulls(current.rightchild)
                        self.anticlockwiseRotation(current)
                        self.updateHull(current)
                    current = current.parent
                    self.updateHull(current)
                else:
                    self.updateHull(current)
            if current.parent is not None:
                if current.parent.rightchild == current:
                    right = True
                else:
                    right = False
            if (current.balance_factor != 0) and (not balanced):
                updateBF = False
            if self.show_:
                print("The updated lc-hull of the node with label {}".format(current.label))
                current.Ql.print()
                print("The updated rc-hull of the node with label {}".format(current.label))
                current.Qr.print()
            current = current.parent
            if current is not None:
                if current.parent is not None:
                    if (current.parent.rightchild == current) and (right):
                        update_label = False
                    elif not right:
                        update_label = True
                    else:
                        update_label = False
                elif not right:
                    update_label = True
                else:
                    update_label = False

    def search_Node(self, point_to_search: Point) -> Optional[TreeNode]:
        current = self.root_
        i = 1
        while current.rightchild is not None:
            self.buildChildrensHulls(current)
            if self.show_:
                print("The lc-hull of the lower half at level {}".format(i))
                current.leftchild.Ql.print()
                print("The rc-hull of the lower half at level {}".format(i))
                current.leftchild.Qr.print()
                print("The lc-hull of the upper half at level {}".format(i))
                current.rightchild.Ql.print()
                print("The rc-hull of the upper half at level {}".format(i))
                current.rightchild.Qr.print()
            if point_to_search.y_coord <= current.label:
                current = current.leftchild
            else:
                current = current.rightchild
            i += 1
        if current.p == point_to_search:
            return current
        else:
            return None

    def print(self) -> None:
        self.printValues(self.root_, 0)

    def printValues(self, current_node: TreeNode, indent: int) -> None:
        if current_node is not None:
            for i in range(indent):
                print("---", end="")
            if current_node.rightchild is None:
                print("-- ({}, {})".format(current_node.p.x_coord, current_node.p.y_coord))
            else:
                print("-- {}".format(current_node.label))
            print()
            self.printValues(current_node.leftchild, indent + 1)
            self.printValues(current_node.rightchild, indent + 1)

    def root(self) -> Optional[TreeNode]:
        return self.root_

    def set_show(self, show: bool) -> None:
        self.show_ = show
