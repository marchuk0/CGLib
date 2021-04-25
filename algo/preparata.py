from models import LinkedQueue, Point


def initial_hull(points):
    hull = points[:3]
    rest = points[3:]
    c_dir = Point.direction(*hull)
    while c_dir == 0:
        hull[1], hull[2] = hull[2], rest.pop(0)
        c_dir = Point.direction(*hull)
    if c_dir < 0:
        hull[1], hull[2] = hull[2], hull[1]
    return hull, rest


def preparata(points):
    x_ordered = sorted(points)
    yield x_ordered
    init_hull, pts = initial_hull(x_ordered)
    lq = LinkedQueue(init_hull)
    while pts:
        yield [node.data for node in lq.list_of_nodes()]
        yield lq.root
        point = pts.pop(0)
        ln = LinkedQueue.search_left(lq.root, point)
        rn = LinkedQueue.search_right(lq.root, point)
        yield [ln, rn]
        lq.insert(point, ln, rn)
    yield [node.data for node in lq.list_of_nodes()]
