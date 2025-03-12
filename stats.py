import numpy as np
from sklearn.metrics import mean_squared_error

def merge(points):
    points = list(points)
    finalPoints = list()
    for coordinate in points.pop(0):
        finalPoints.append([coordinate])
    for dimension in points:
        dimension = list(dimension)
        for i in range(0, len(dimension)):
            # print(i)
            finalPoint = finalPoints[i]
            finalPoint.append(dimension[i])
            finalPoints[i] = finalPoint
    return finalPoints

def distance(point1:list, point2:list):
    sumlist = list()
    for i in range(len(point1)):
        sumlist.append(point1[i]-point2[i])
    
    return float(np.sqrt(sum(np.square(sumlist))))

def frange(start, stop, step):
    current = start
    while current < stop:
        yield current
        current += step

def border(points1, points2, xmax, ymax, xmin=0, ymin=0, step=0.1):
    borderlist = list()
    flag = False
    for x in frange(xmin, xmax, step):
        category = False
        for y in frange(ymin, ymax, step):
            point = [x, y]
            category1Distance = False
            category2Distance = False
            for point1 in points1:
                if distance(point, point1) < category1Distance or not category1Distance:
                    category1Distance = distance(point, point1)
            for point2 in points2:
                if distance(point, point2) < category2Distance or not category2Distance:
                    category2Distance = distance(point, point2)
            if not category:
                if category1Distance < category2Distance:
                    category = 1
                else:
                    category = 2
                continue
            if category == 1:
                if category1Distance > category2Distance:
                    borderlist.append(point)
                    break
            elif category == 2:
                if category1Distance < category2Distance:
                    borderlist.append(point)
                    break
        else:
            if len(borderlist) != 0:
                last = borderlist[len(borderlist)-1]
                if last[1] != ymax-1:
                    borderlist.append([x, ymax-1])
                    flag = True
                elif flag:
                    flag = False
                    break
            else:
                borderlist.append([x,ymax-1])

    return borderlist

def longestdistance(points):
    point1 = points[0]
    point2 = None
    point3 = None
    dist = 0


    for item in points:
        if dist < distance(item, point1):
            dist = distance(item, point1)
            point1 = item

    while True:
        dist = 0
        for item in points:
            if dist < distance(item, point1):
                dist = distance(item, point1)
                point2 = item
        if point2 != None:
            dist = 0
            for item in points:
                if dist < distance(item, point2):
                    dist = distance(item, point2)
                    point3 = item
            if point3 != point1:
                point1 = point3
                point3, point2 = None, None
            else:
                break

    return dist

def shortestGroup(points1, points2):
    point1 = points1.pop(0)
    point2 = None
    dist = False
    for point in points2:
        if dist > distance(point, point1) or not dist:
            dist = distance(point, point1)
            point1 = point

    dist = False
    point = 1
    while True:
        tdist = False
        if point == 1:
            for point in points1:
                if tdist > distance(point, point1) or not tdist:
                    tdist = distance(point, point1)
                    point2 = point
            point = 2
        elif point == 2:
            for point in points2:
                if tdist > distance(point, point2) or not tdist:
                    tdist = distance(point, point2)
                    point1 = point
            point = 1
        if tdist == dist:
            break
        else:
            dist = tdist


    return point1, point2, dist

def avgDist(x0, y0, z0, x1, y1, z1):

    x0 = sum(x0)/len(x0)
    y0 = sum(y0)/len(y0)
    z0 = sum(z0)/len(z0)

    x1 = sum(x1)/len(x1)
    y1 = sum(y1)/len(y1)
    z1 = sum(z1)/len(z1)

    point0 = [x0, y0, z0]
    point1 = [x1, y1, z1]

    return distance(point1=point0, point2=point1)

def regressionDegree(borderx, bordery):
    best_degree = None
    lowest_bic = float('inf')

    for i in range(0, 50):
        coefficients = np.polyfit(borderx, bordery, i)
        polynomial = np.poly1d(coefficients)
        predictions = polynomial(borderx)
        mse = mean_squared_error(bordery, predictions)

        # Calculate log-likelihood (approximate)
        n = len(bordery)  # Number of data points
        log_likelihood = -n / 2 * (np.log(2 * np.pi) + np.log(mse) + 1)

        # Calculate BIC
        k = i + 1  # Number of parameters (coefficients, including intercept)
        bic = k * np.log(n) - 2 * log_likelihood

        # Track the best degree based on BIC
        if bic < lowest_bic and bic != float("-inf"):
            lowest_bic = bic
            best_degree = i

        print(f"Degree {i}: BIC = {bic:.2f}")
    
    return best_degree