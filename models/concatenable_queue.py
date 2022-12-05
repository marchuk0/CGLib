import copy
from enum import Enum
from typing import Union, Any, Optional, Tuple


class NodeType(Enum):
    LEAF_NODE = 0
    TWO_NODE = 1
    THREE_NODE = 2


class Node:
    def __init__(self):
        self.type = NodeType.LEAF_NODE
        self.data1 = 0
        self.data2 = 0  # if the node has type LEAF_NODE, data2 is y-coordinate
        self.x_coord = 0
        self.left = None
        self.middle = None
        self.right = None
        self.parent = None
        self.biggest_y = None
        self.smallest_y = None


class ConcatenableQueue:
    def __init__(self):
        self.__root = None

    def clone(self) -> 'ConcatenableQueue':
        new_queue = ConcatenableQueue()
        if not self.is_empty():
            ConcatenableQueue.__add_queue_points_to_queue(new_queue, self.__root)
        return new_queue

    @staticmethod
    def __add_queue_points_to_queue(cq: 'ConcatenableQueue', current_node: Node):
        if current_node is not None:
            if current_node.type == NodeType.LEAF_NODE:
                cq.add_node(current_node.x_coord, current_node.data2)
            ConcatenableQueue.__add_queue_points_to_queue(cq, current_node.left)
            ConcatenableQueue.__add_queue_points_to_queue(cq, current_node.middle)
            ConcatenableQueue.__add_queue_points_to_queue(cq, current_node.right)

    def add_node(self, x_coord: float, y_coord: float) -> None:
        if self.__root is None:
            self.__root = self.__create_leaf_node(x_coord, y_coord)
        else:
            if self.__root.type == NodeType.LEAF_NODE:
                new_node1 = self.__create_leaf_node(x_coord, y_coord)
                new_node2 = self.__create_leaf_node(self.__root.x_coord, self.__root.data2)

                if y_coord < self.__root.data2:
                    new_node = self.__create_2_node(y_coord, self.__root.data2, new_node1, new_node2)
                else:
                    new_node = self.__create_2_node(self.__root.data2, y_coord, new_node2, new_node1)
                self.__root = new_node
                new_node1.parent = self.__root
                new_node2.parent = self.__root
            else:
                new_node = self.__create_leaf_node(x_coord, y_coord)
                father_node = self.__search_for_insert(new_node, self.__root)
                if father_node.type == NodeType.TWO_NODE:
                    new_node.parent = father_node
                    if father_node.data1 <= y_coord and y_coord <= father_node.data2:
                        father_node.middle = new_node
                        father_node.data2 = y_coord
                    elif father_node.data1 > y_coord:
                        father_node.middle = father_node.left
                        father_node.left = new_node
                        father_node.data1 = y_coord
                        father_node.data2 = father_node.middle.data2
                    else:
                        father_node.middle = father_node.right
                        father_node.right = new_node
                        father_node.data2 = father_node.middle.data2
                    father_node.type = NodeType.THREE_NODE
                    self.__update_values_insert(father_node, father_node.right.data2)

                else:
                    new_node.parent = father_node
                    if new_node.data2 > father_node.data2:
                        if (new_node.data2 > father_node.right.data2):
                            aux = father_node.right
                            father_node.right = new_node
                        else:
                            aux = new_node
                    else:
                        aux = father_node.middle
                        if (new_node.data2 > father_node.data1):
                            father_node.middle = new_node
                        else:
                            father_node.middle = father_node.left
                            father_node.left = new_node
                    father_node.data1 = father_node.left.data2
                    father_node.data2 = father_node.middle.data2
                    self.add_child_node(father_node, aux, y_coord)

    def __create_leaf_node(self, x_coord: float, y_coord: float) -> Node:
        new_node = Node()
        new_node.data1 = -1
        new_node.data2 = y_coord
        new_node.x_coord = x_coord
        return new_node

    def __create_2_node(self, l_value: float, r_value: float, left_child: Node, right_child: Node) -> Node:
        new_node = Node()
        new_node.data1 = l_value
        new_node.data2 = r_value
        new_node.type = NodeType.TWO_NODE
        new_node.left = left_child
        new_node.right = right_child

        if left_child.type == NodeType.LEAF_NODE:
            new_node.smallest_y = left_child
            new_node.biggest_y = right_child
        else:
            new_node.smallest_y = left_child.smallest_y
            new_node.biggest_y = right_child.biggest_y
        return new_node

    def __search_for_insert(self, new_node: Node, current_node: Node):
        if new_node.data2 < current_node.smallest_y.data2:
            current_node.smallest_y = new_node
        elif new_node.data2 > current_node.biggest_y.data2:
            current_node.biggest_y = new_node

        if current_node.left.type == NodeType.LEAF_NODE:
            return current_node

        if new_node.data2 <= current_node.data1:
            return self.__search_for_insert(new_node, current_node.left)
        else:
            if (current_node.middle is not None) and (new_node.data2 <= current_node.data2):
                return self.__search_for_insert(new_node, current_node.middle)
            else:
                return self.__search_for_insert(new_node, current_node.right)

    def __update_values_insert(self, current_node: Node, value: float):
        while current_node != self.__root:
            if current_node == current_node.parent.left and current_node.parent.data1 < value:
                current_node.parent.data1 = value
            elif current_node == current_node.parent.middle and current_node.parent.data2 < value:
                current_node.parent.data2 = value
            elif (current_node == current_node.parent.right and
                  current_node.parent.middle is None and
                  current_node.parent.data2 < value):
                current_node.parent.data2 = value
            current_node = current_node.parent
            value = current_node.data2

    def __update_values_delete(self, current_node: Node, current_value: float, new_value: float):
        while current_node != self.__root and current_node is not None:
            if current_node == current_node.parent.left and current_node.parent.data1 == current_value:
                current_node.parent.data1 = new_value
            elif current_node == current_node.parent.middle and current_node.parent.data2 == current_value:
                current_node.parent.data2 = new_value
            elif (current_node == current_node.parent.right and
                  current_node.parent.middle is None and
                  current_node.parent.data2 == current_value):
                current_node.parent.data2 = new_value
            current_node = current_node.parent

    def add_child_node(self, child: Node, aux: Node, value: float):
        if child.left.type == NodeType.LEAF_NODE:
            v1 = self.__create_2_node(aux.data2, child.right.data2, aux, child.right)
            child.biggest_y = child.middle
        else:
            v1 = self.__create_2_node(aux.biggest_y.data2, child.right.biggest_y.data2, aux, child.right)
            child.biggest_y = child.middle.biggest_y

        v1.left.parent = v1
        v1.right.parent = v1
        child.right = child.middle
        child.middle = None
        child.type = NodeType.TWO_NODE
        if child.parent is None:
            new_root = self.__create_2_node(self.__root.data2, v1.data2, child, v1)
            self.__root = new_root
            child.parent = self.__root
            v1.parent = self.__root
        else:
            v1.parent = child.parent
            if child.parent.type == NodeType.TWO_NODE:
                if child == child.parent.left:
                    child.parent.middle = v1
                    child.parent.data2 = v1.data2
                    child.parent.data1 = child.data2
                else:
                    child.parent.middle = child
                    child.parent.right = v1
                    child.parent.data2 = child.data2
                child.parent.type = NodeType.THREE_NODE
            else:
                if child == child.parent.left:
                    aux1 = child.parent.middle
                    child.parent.middle = v1
                else:
                    if child == child.parent.middle:
                        aux1 = v1
                    else:
                        aux1 = child
                        child.parent.right = v1

                if child.parent.left.type == NodeType.LEAF_NODE:
                    child.parent.data1 = child.parent.left.data2
                    child.parent.data2 = child.parent.middle.data2
                else:
                    child.parent.data1 = child.parent.left.biggest_y.data2
                    child.parent.data2 = child.parent.middle.biggest_y.data2

                self.add_child_node(child.parent, aux1, value)

    def __delete_node(self, node_to_delete: Node):
        if node_to_delete == self.__root:
            self.__root = None
        elif node_to_delete.parent == self.__root and self.__root.type == NodeType.TWO_NODE:
            if node_to_delete == self.__root.left:
                self.__root.right.parent = None
                self.__root = self.__root.right
            else:
                self.__root.left.parent = None
                self.__root = self.__root.left
        else:
            father = Node()
            father = node_to_delete.parent
            if father.type == NodeType.THREE_NODE:
                if father.left == node_to_delete:
                    father.left = father.middle
                elif father.right == node_to_delete:
                    father.right = father.middle
                father.middle = None
                father.type = NodeType.TWO_NODE
                father.data1 = father.left.data2
                father.data2 = father.right.data2
                self.__update_values_delete(father, node_to_delete.data2, father.data2)
            else:
                if father.left == node_to_delete:
                    brother = father.right
                else:
                    brother = father.left

                if father.parent.right == father:
                    if father.parent.type == NodeType.THREE_NODE:
                        fathers_brother = father.parent.middle
                    else:
                        fathers_brother = father.parent.left
                    left_brother = True
                else:
                    if father.parent.left == father:
                        if father.parent.type == NodeType.THREE_NODE:
                            fathers_brother = father.parent.middle
                        else:
                            fathers_brother = father.parent.right
                        left_brother = False
                    else:
                        fathers_brother = father.parent.left
                        left_brother = True

                if fathers_brother.type == NodeType.THREE_NODE:
                    aux_value1 = father.data2
                    if left_brother:
                        father.right = brother
                        aux_value2 = fathers_brother.right.data2
                        father.left = fathers_brother.right
                        father.left.parent = father
                        father.data1 = father.left.data2
                        father.data2 = father.right.data2
                        fathers_brother.right = fathers_brother.middle
                        father.data1 = father.left.data2
                        father.data2 = father.right.data2
                        fathers_brother.middle = None
                        fathers_brother.type = NodeType.TWO_NODE
                        self.__update_values_delete(father, aux_value1, father.right.data2)
                        self.__update_values_delete(fathers_brother, aux_value2, fathers_brother.right.data2)
                    else:
                        father.left = brother
                        father.right = fathers_brother.left
                        father.right.parent = father
                        fathers_brother.left = fathers_brother.middle
                        fathers_brother.data1 = fathers_brother.left.data2
                        fathers_brother.data2 = fathers_brother.right.data2
                        fathers_brother.middle = None
                        father.data1 = father.left.data2
                        father.data2 = father.right.data2
                        fathers_brother.type = NodeType.TWO_NODE
                        self.__update_values_delete(father, aux_value1, father.right.data2)
                else:
                    if left_brother:
                        fathers_brother.middle = fathers_brother.right
                        fathers_brother.right = brother
                        fathers_brother.right.parent = fathers_brother
                        self.__update_values_insert(fathers_brother, fathers_brother.right.data2)
                    else:
                        fathers_brother.middle = fathers_brother.left
                        fathers_brother.left = brother
                        fathers_brother.right.parent = fathers_brother
                    brother.parent = fathers_brother
                    fathers_brother.data1 = fathers_brother.left.data2
                    fathers_brother.data2 = fathers_brother.middle.data2
                    fathers_brother.type = NodeType.THREE_NODE
                    father.right = None
                    father.left = None
                    self.__delete_node(father)
                    self.__update_values_insert(fathers_brother, fathers_brother.right.data2)

    def delete_node(self, value: float):
        node_to_delete = self.__search_leaf_node(value, self.__root)
        if node_to_delete is None:
            print("The leaf with data {0} does not exist in the tree.".format(value))
        else:
            self.__delete_node(node_to_delete)
            print("The leaf with data {0} was deleted from the tree.".format(value))

    def __search_leaf_node(self, value: float, current: Node) -> Optional[Node]:
        if current.type == NodeType.LEAF_NODE:
            if current.data2 == value:
                return current
            else:
                return None
        elif value <= current.data1:
            return self.__search_leaf_node(value, current.left)
        elif (value <= current.data2) and (current.middle is not None):
            return self.__search_leaf_node(value, current.middle)
        return self.__search_leaf_node(value, current.right)

    def is_empty(self) -> bool:
        if self.__root is None:
            return True
        else:
            return False

    def print(self) -> None:
        if self.is_empty():
            print("Empty Queue")
        else:
            self.__print_values(self.__root)

    def __print_values(self, current_node: Node) -> None:
        if current_node is not None:
            if current_node.type == NodeType.LEAF_NODE:
                print("({0} , {1}), ".format(current_node.x_coord, current_node.data2))
            self.__print_values(current_node.left)
            self.__print_values(current_node.middle)
            self.__print_values(current_node.right)

    def search(self, value: float) -> None:
        res = self.__search_leaf_node(value, self.__root)
        if res is None:
            print("{0} is not a data of the tree".format(value))
        else:
            print("{0} was found".format(res.data2))

    def height(self) -> int:
        h = 0
        current_node = self.__root
        while current_node is not None:
            h += 1
            current_node = current_node.right
        return h

    def rightmost_node_at_level(self, level: int, bigger_y: Node) -> Node:
        current_node = self.__root
        current_node.biggest_y = bigger_y
        for i in range(1, level, 1):
            current_node = current_node.right
            current_node.biggest_y = bigger_y
        return current_node

    def leftmost_node_at_level(self, level: int, smaller_y: Node) -> Node:
        current_node = self.__root
        current_node.smallest_y = smaller_y
        for i in range(1, level, 1):
            current_node = current_node.left
            current_node.smallest_y = smaller_y
        return current_node

    def root(self) -> Node:
        return self.__root

    def set_root(self, new_root: Node) -> None:
        self.__root = new_root

    @staticmethod
    def concatenate(cq_1: 'ConcatenableQueue', cq_2: 'ConcatenableQueue') -> 'ConcatenableQueue':
        new_cq = ConcatenableQueue()
        if cq_1.is_empty():
            return copy.copy(cq_2)
        elif cq_2.is_empty():
            return copy.copy(cq_1)

        else:
            height_cq1 = cq_1.height()
            height_cq2 = cq_2.height()
            if (height_cq1 == height_cq2) and (height_cq1 > 0):
                new_root = Node()
                new_root.left = cq_1.root()
                new_root.left.parent = new_root
                new_root.right = cq_2.root()
                new_root.right.parent = new_root
                new_root.type = NodeType.TWO_NODE
                if cq_1.root().type != NodeType.LEAF_NODE:
                    new_root.data1 = cq_1.root().biggest_y.data2
                    new_root.data2 = cq_2.root().biggest_y.data2
                    new_root.smallest_y = cq_1.root().smallest_y
                    new_root.biggest_y = cq_2.root().biggest_y
                else:
                    new_root.smallest_y = cq_1.root()
                    new_root.biggest_y = cq_2.root()
                    new_root.data1 = cq_1.root().data2
                    new_root.data2 = cq_2.root().data2
                new_cq.set_root(new_root)
                new_cq.root().middle = None
            elif height_cq1 > height_cq2:
                new_cq = copy.copy(cq_1)
                new_cq.root().parent = None
                level = height_cq1 - height_cq2
                if cq_2.root().type != NodeType.LEAF_NODE:
                    attach_node = new_cq.rightmost_node_at_level(level, cq_2.root().biggest_y)
                else:
                    attach_node = new_cq.rightmost_node_at_level(level, cq_2.root())
                if attach_node.type == NodeType.TWO_NODE:
                    attach_node.type = NodeType.THREE_NODE
                    attach_node.middle = attach_node.right
                    attach_node.right = cq_2.root()
                    attach_node.right.parent = attach_node
                    current_node = attach_node.parent
                    while current_node is not None:
                        if current_node.type == NodeType.TWO_NODE:
                            if cq_2.root().type == NodeType.LEAF_NODE:
                                current_node.data2 = cq_2.root().data2
                            else:
                                current_node.data2 = cq_2.root().biggest_y.data2
                        current_node = current_node.parent
                elif attach_node.type == NodeType.THREE_NODE:
                    aux = attach_node.right
                    attach_node.right = cq_2.root()
                    attach_node.right.parent = attach_node
                    if attach_node == cq_1.root():
                        attach_node.parent = None
                    new_cq.add_child_node(attach_node, aux, attach_node.right.data2)
            else:
                new_cq = copy.copy(cq_2)
                new_cq.root().parent = None
                level = height_cq2 - height_cq1
                if cq_1.root().type != NodeType.LEAF_NODE:
                    attach_node = new_cq.leftmost_node_at_level(level, cq_1.root().smallest_y)
                else:
                    attach_node = new_cq.leftmost_node_at_level(level, cq_1.root())
                if attach_node.type == NodeType.TWO_NODE:
                    attach_node.type = NodeType.THREE_NODE
                    attach_node.middle = attach_node.left
                    attach_node.left = cq_1.root()
                    attach_node.left.parent = attach_node
                    if cq_1.root().type == NodeType.LEAF_NODE:
                        attach_node.data1 = attach_node.left.data2
                        attach_node.data2 = attach_node.middle.data2
                    else:
                        attach_node.data1 = attach_node.left.biggest_y.data2
                        attach_node.data2 = attach_node.middle.biggest_y.data2
                elif attach_node.type == NodeType.THREE_NODE:
                    aux = attach_node.middle
                    attach_node.middle = attach_node.left
                    attach_node.left = cq_1.root()
                    attach_node.left.parent = attach_node
                    attach_node.data2 = attach_node.data1
                    if cq_1.root().type == NodeType.LEAF_NODE:
                        attach_node.data1 = attach_node.left.data2
                    else:
                        attach_node.data1 = attach_node.left.biggest_y.data2
                    if attach_node == cq_2.root():
                        attach_node.parent = None
                    new_cq.add_child_node(attach_node, aux, attach_node.left.data2)
            return new_cq

    # split_left, second CQ keeps the node with value val
    @staticmethod
    def split_left(cq: 'ConcatenableQueue', split_value: float) -> Tuple[
        'ConcatenableQueue', 'ConcatenableQueue']:
        cqr1 = ConcatenableQueue()
        cqr2 = ConcatenableQueue()
        cqr = ConcatenableQueue()
        cql1 = ConcatenableQueue()
        cql2 = ConcatenableQueue()
        cql = ConcatenableQueue()
        aux1 = ConcatenableQueue()
        aux2 = ConcatenableQueue()
        current_node = cq.root()
        while current_node.type != NodeType.LEAF_NODE:
            if split_value <= current_node.data1:
                cqr1.set_root(current_node.right)
                cqr1.root().parent = None
                if current_node.type == NodeType.TWO_NODE:
                    if cqr.root() is None:
                        cqr = cqr1
                    else:
                        aux1 = cqr
                        cqr = ConcatenableQueue.concatenate(cqr1, aux1)
                else:
                    cqr2.set_root(current_node.middle)
                    cqr2.root().parent = None
                    if cqr.root() is None:
                        cqr = ConcatenableQueue.concatenate(cqr2, cqr1)
                    else:
                        aux1 = cqr
                        aux2 = ConcatenableQueue.concatenate(cqr2, cqr1)
                        cqr = ConcatenableQueue.concatenate(aux2, aux1)
                current_node = current_node.left
            elif (current_node.type == NodeType.THREE_NODE) and (split_value <= current_node.data2):
                cql1.set_root(current_node.left)
                cql1.root().parent = None
                cqr1.set_root(current_node.right)
                cqr1.root().parent = None
                if cqr.root() is None:
                    cqr = cqr1
                else:
                    aux1 = cqr
                    cqr = ConcatenableQueue.concatenate(cqr1, aux1)
                aux1 = cql
                if cql.root() is None:
                    cql = cql1
                else:
                    cql = ConcatenableQueue.concatenate(aux1, cql1)
                current_node = current_node.middle
            else:
                cql1.set_root(current_node.left)
                cql1.root().parent = None
                if current_node.type == NodeType.TWO_NODE:
                    if cql.root() is None:
                        cql = cql1
                    else:
                        aux1 = cql
                        cql = ConcatenableQueue.concatenate(aux1, cql1)
                else:
                    cql2.set_root(current_node.middle)
                    cql2.root().parent = None
                    if cql.root() is None:
                        cql = ConcatenableQueue.concatenate(cql1, cql2)
                    else:
                        aux1 = cql
                        aux2 = ConcatenableQueue.concatenate(cql1, cql2)
                        cql = ConcatenableQueue.concatenate(aux1, aux2)
                current_node = current_node.right

        if cql.root() is None:
            cql.set_root(current_node)
            cql.root().parent = None
        else:
            aux1.set_root(current_node)
            aux1.root().parent = None
            aux2 = cql
            cql = ConcatenableQueue.concatenate(aux2, aux1)
        return cql, cqr

    # split_right, second CQ keeps the node with value val
    @staticmethod
    def split_right(cq: 'ConcatenableQueue', split_value: float) -> Tuple[
        'ConcatenableQueue', 'ConcatenableQueue']:
        cqr1 = ConcatenableQueue()
        cqr2 = ConcatenableQueue()
        cqr = ConcatenableQueue()
        cql1 = ConcatenableQueue()
        cql2 = ConcatenableQueue()
        cql = ConcatenableQueue()
        aux1 = ConcatenableQueue()
        aux2 = ConcatenableQueue()
        current_node = cq.root()
        while current_node.type != NodeType.LEAF_NODE:
            if split_value <= current_node.data1:
                cqr1.set_root(current_node.right)
                cqr1.root().parent = None
                if current_node.type == NodeType.TWO_NODE:
                    if cqr.root() is None:
                        cqr.set_root(cqr1.root())
                    else:
                        aux1.set_root(cqr.root())
                        cqr = ConcatenableQueue.concatenate(cqr1, aux1)
                else:
                    cqr2.set_root(current_node.middle)
                    cqr2.root().parent = None
                    if cqr.root() is None:
                        cqr = ConcatenableQueue.concatenate(cqr2, cqr1)
                    else:
                        # aux1 = cqr
                        aux1.set_root(cqr.root())
                        aux2 = ConcatenableQueue.concatenate(cqr2, cqr1)
                        cqr = ConcatenableQueue.concatenate(aux2, aux1)
                current_node = current_node.left
            elif (current_node.type == NodeType.THREE_NODE) and (split_value <= current_node.data2):
                cql1.set_root(current_node.left)
                cql1.root().parent = None
                cqr1.set_root(current_node.right)
                cqr1.root().parent = None
                if cqr.root() is None:
                    # cqr = cqr1
                    cqr.set_root(cqr1.root())
                else:
                    aux1.set_root(cqr.root())
                    # aux1 = cqr
                    cqr = ConcatenableQueue.concatenate(cqr1, aux1)
                aux1 = cql
                aux1.set_root(cql.root())
                if cql.root() is None:
                    # cql = cql1
                    cql.set_root(cql1.root())
                else:
                    cql = ConcatenableQueue.concatenate(aux1, cql1)
                current_node = current_node.middle
            else:
                cql1.set_root(current_node.left)
                cql1.root().parent = None
                if current_node.type == NodeType.TWO_NODE:
                    if cql.root() is None:
                        # cql = cql1
                        cql.set_root(cql1.root())
                    else:
                        # aux1 = cql
                        aux1.set_root(cql.root())
                        cql = ConcatenableQueue.concatenate(aux1, cql1)
                else:
                    cql2.set_root(current_node.middle)
                    cql2.root().parent = None
                    if cql.root() is None:
                        cql = ConcatenableQueue.concatenate(cql1, cql2)
                    else:
                        aux1.set_root(cql.root())
                        # aux1 = cql
                        aux2 = ConcatenableQueue.concatenate(cql1, cql2)
                        cql = ConcatenableQueue.concatenate(aux1, aux2)
                current_node = current_node.right
        if cqr.root() is None:
            cqr.set_root(current_node)
            cqr.root().parent = None
        else:
            aux1.set_root(current_node)
            aux1.root().parent = None
            aux2 = cqr
            cqr = ConcatenableQueue.concatenate(aux1, aux2)
        return cql, cqr
