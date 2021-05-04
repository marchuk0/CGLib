from models import DynamicHull


def dynamic_convex_hull(points, point, op='add'):
    dh = DynamicHull(points)
    yield sorted(points)
    yield dh
    if op == 'add':
        yield dh.insert(point)
        yield dh
    elif op == 'remove':
        yield dh.remove(point)
        yield dh
