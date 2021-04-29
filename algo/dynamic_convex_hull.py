from models import DynamicHull


def dynamic_convex_hull(points, point, op='add'):
    dh = DynamicHull(points)
    yield dh.x_ordered
    yield dh
    if op == 'add':
        dh.add(point)
    if op == 'remove':
        dh.remove(point)
    yield dh
