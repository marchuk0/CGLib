from models import LinkedQueue


def preparata(points):
    x_ordered = sorted(points)
    yield x_ordered
    lq = LinkedQueue(x_ordered)
    yield lq
    yield lq.root
    while x_ordered:
        point = x_ordered.pop(0)
        ln = LinkedQueue.search_left(lq.root, point)
        rn = LinkedQueue.search_right(lq.root, point)
        yield ln, rn
        lq.insert(point, ln, rn)
        yield lq

