class Node:
    def __init__(self, data):
        """By default Node has no children."""
        self.data = data
        self.left = None
        self.right = None

    def __eq__(self, other):
        """Recursive equality."""
        return (
                self.data == other.data
                and self.left == other.left
                and self.right == other.right
        )


class NodeWithParent(Node):
    def __init__(self, data, parent=None):
        self.parent = parent
        super().__init__(data)


class LQNode(Node):
    def __init__(self, data, l_left=None, l_right=None):
        self.l_left = l_left
        self.l_right = l_right
        super().__init__(data)
