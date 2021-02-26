import math
import json
import time
import itertools

# GLOBAL VARS #
dim = 450  # dimension of the 2d grid
axmax = 100000  # maximum value on any axis in data

# Image: https://i.imgur.com/sTDwJyf.png
# The boxes represent a 3x3 section of the grid. As we check each box, we also compare all the neighboring boxes.
# The highest possible score that we will miss this way is represented by the red line. This is a hypothetical trio with
# an average rating of 5, and the shortest possible distance between three points that wont be included in
# this 3x3 "search light".
# The score of this hypothetical trio will be 5 divided by the length of the red line. The shortest possible red line is
# the length of the side of one box.
# Using this, you can find a formula for the highest possible score you can miss for any box side length, score = 5/sl
# Where sl is the side length = total map length/number of boxes = 200000/dim
# Using the resulting formula of MaxMissedScore = 5/(200000/dim) we can find the highest dim that will ensure a
# minimum score

# Higher dim -> smaller boxes -> Fewer pizzerias to compare in each box -> less operations per box
# at the same time, the number of boxes increases with the square of dim, so you find a balancing point where more dim
# is slower because there are more boxes to check, even if there are points to compare in each box.


def pizzerias():
    """

    :return: returns a list of lists of lists (2d array of lists) where all pizzerias in pizzerias.json have been
    geographically divided into each list
    """
    with open('pizzerias.json') as json_file:
        data = json.load(json_file)
        # Data represents pizzas on a map where x and y both go from -100k to +100k

        # Pizzerias is a sl*sl square 2d grid of list with side length 200000/sl
        pizzerias = []
        for i in range(dim):
            pizzerias.append([])
            for j in range(dim):
                pizzerias[i].append([])

        for pizzeria in data:
            p = Pizzeria(pizzeria['rating'], pizzeria['x'], pizzeria['y'], pizzeria['name'])

            def box(z):
                # find x or y index for a given x or y coordinate
                z = (z + axmax)       # shift z up by maximum negative value on axis so we're working from zero
                ret = z/(2 * axmax / dim)  # divide by total map side length divided by number of indices
                return int(ret)

            # print("x: {}, y: {}".format(box(p.x), box(p.y)))
            pizzerias[box(p.x)][box(p.y)].append(p)

        return pizzerias


# distance function
def d(p1, p2):
    return math.sqrt(((p1.x - p2.x) ** 2) + ((p1.y - p2.y) ** 2))


class Pizzeria:
    def __init__(self, r, x, y, n):
        self.r = r
        self.x = x
        self.y = y
        self.n = n


def rating(p1, p2, p3):
    avg = (p1.r+p2.r+p3.r)/3
    dist = d(p1, p2) + d(p1, p3) + d(p2, p3)
    return avg/dist

start_time = time.time()

pizzerias = pizzerias()
print("Got pizzerias from json")

# vars to record result
highest_rating = 0
combination = 0

#boxesdone = 0
# For each spatial partition, check all combinations within that partition and adjacent partitions
for x in range(dim):
    for y in range(dim):
        pizzeriasInRegion = pizzerias[x][y][:]

        # Now we add the adjacent tiles' pizzerias
        for i in range(0, 2):
            for j in range(0, 2):
                if 0 <= x+i < dim and 0 <= y + j < dim:
                    pizzeriasInRegion += pizzerias[x+i][y+j]

        pizzeriasInRegion = list(set(pizzeriasInRegion))

        for c in itertools.combinations(pizzeriasInRegion, 3):
            r = rating(c[0], c[1], c[2])
            if r > highest_rating:
                highest_rating = r
                combination = c
                #print("New highest rating! {}".format(highest_rating))
        #boxesdone += 1
        #print("--- %s seconds --- %s of %s done, %s percent, minutes left: %s" % (time.time() - start_time, boxesdone, (dim*dim), 100*boxesdone/(dim**2), ((time.time() - start_time)/(boxesdone/(dim**2)))))


print("--- %s seconds ---" % (time.time() - start_time))
print("Highest rating: {}".format(highest_rating))
print("P1 x{}, y{}, rating: {}, name: {}".format(combination[0].x, combination[0].y, combination[0].r, combination[0].n))
print("P2 x{}, y{}, rating: {}, name: {}".format(combination[1].x, combination[1].y, combination[1].r, combination[1].n))
print("P3 x{}, y{}, rating: {}, name: {}".format(combination[2].x, combination[2].y, combination[2].r, combination[2].n))
# p1 = Pizzeria(4.6, -1, -1)
# p2 = Pizzeria(4.8, 1, 1)
# p3 = Pizzeria(5, 0, 1)

# x, y = list(),list()
# for p in pizzerias2:
#     x.append(p.x)
#     y.append(p.y)
#
# plt.scatter(x, y)
# plt.show()
# hs = 0
# for p in pizzerias2[2:]:
#     r = rating(pizzerias2[0],pizzerias2[1],p)
#     if r > hs: hs = r
# print(hs)



