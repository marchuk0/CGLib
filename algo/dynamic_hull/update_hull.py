import time
from algo.dynamic_hull.toplevel_tree import Point, Tree


def print_menu() -> None:
    print()
    print("1. Add a point")
    print("2. Delete a point")
    print("3. Exit")


def main():
    i = 1
    toptree = 'y'
    lc_rchulls = 'y'
    p = Point()
    tree1 = Tree()
    print_menu()
    while i != 3:
        i = int(input(">> "))
        if i == 1:
            p.x_coord = float(input("Enter the x-coordinate of the point: "))
            p.y_coord = float(input("Enter the y-coordinate of the point: "))
            toptree = input("See the structure of the top level tree after and after each update y/n: ")
            lc_rchulls = input(
                "See the lc/rc-hull splitting at each level of the tree while going down before the insertion y/n: ")
            if (toptree == 'y') or (toptree == 'Y'):
                print("Top level tree before inserting the point ({}, {})".format(p.x_coord, p.y_coord))
                tree1.print()
                print()
            if (lc_rchulls == 'y') or (lc_rchulls == 'Y'):
                tree1.set_show(True)
            else:
                tree1.set_show(False)
            start = time.time()
            tree1.add_Node(p)
            end = time.time()
            time_diff = end - start
            print("{} milliseconds spent updating the convex hull".format(time_diff))
            print("The new convex hull is:")
            root = tree1.root()
            root.Ql.print()
            print()
            root.Qr.print()
            print()
            if (toptree == 'y') or (toptree == 'Y'):
                print("Top level tree after inserting the point ({}, {})".format(p.x_coord, p.y_coord))
                tree1.print()
                print()
            print_menu()
        elif i == 2:
            p.x_coord = float(input("Enter the x-coordinate of the point: "))
            p.y_coord = float(input("Enter the y-coordinate of the point: "))
            toptree = input("See the structure of the top level tree after and after each update y/n: ")
            lc_rchulls = input(
                "See the lc/rc-hull splitting at each level of the tree while going down before the insertion y/n: ")
            if (toptree == 'y') or (toptree == 'Y'):
                print("Top level tree before deleting the point ({}, {})".format(p.x_coord, p.y_coord))
                tree1.print()
                print()
            if (lc_rchulls == 'y') or (lc_rchulls == 'Y'):
                tree1.set_show(True)
            else:
                tree1.set_show(False)
            start = time.time()
            tree1.delete_Node(p)
            end = time.time()
            time_diff = end - start
            print("{} milliseconds spent updating the convex hull".format(time_diff))
            print("The new convex hull is:")
            root = tree1.root()
            root.Ql.print()
            print()
            root.Qr.print()
            print()
            if (toptree == 'y') or (toptree == 'Y'):
                print("Top level tree after deleting the point ({}, {})".format(p.x_coord, p.y_coord))
                tree1.print()
                print()
            print_menu()


if __name__ == "__main__":
    main()
