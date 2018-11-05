import os
import math


def simpledotproduct(pt1, pt2):
    """
    Calculate a dot product.
    """
    x1 = float(pt1[0])
    y1 = float(pt1[1])

    x2 = float(pt2[0])
    y2 = float(pt2[1])

    return (x1 * x2) + (y1 * y2)


def calc_saccade_length(cur_coords, prev_coords):
    """
    Get the saccade length
    
    # Arguments
    cur_coords  -> [x, y] coordinates of the current point
    prev_coords -. [x, y] coordinates of the previous point
    """
    x = float(cur_coords[0])
    y = float(cur_coords[1])
    prev_x = float(prev_coords[0])
    prev_y = float(prev_coords[1])

    x_dist = x - prev_x
    y_dist = y - prev_y

    saccade_length = math.sqrt(x_dist**2 + y_dist**2)
    return saccade_length


def calc_abs_angle(cur_coords, prev_coords):
    """
    Calculate the absolute angle of 2 fixations using atan2
    """
    x = float(cur_coords[0])
    y = float(cur_coords[1])
    prev_x = float(prev_coords[0])
    prev_y = float(prev_coords[1])

    x_dist = x - prev_x
    y_dist = y - prev_y

    # Convert to degrees
    abs_angle = math.atan2(y_dist, x_dist) * 180.0 / math.pi
    return abs_angle


def calc_rel_angle(cur_coords, prev_coords, next_coords):
    """
    Reference: EMDAT, https://github.com/ATUAV/EMDAT/blob/master/src/EMDAT_core/Segment.py
    TODO: Add more references
    """
    lastx = float(prev_coords[0])
    lasty = float(prev_coords[1])

    x = float(cur_coords[0])
    y = float(cur_coords[1])
    nextx = float(next_coords[0])
    nexty = float(next_coords[1])
    v1 = (lastx - x, lasty - y)
    v2 = (nextx - x, nexty - y)

    if v1 != (0.0, 0.0) and v2 != (0.0, 0.0):
        v1_dot = math.sqrt(simpledotproduct(v1, v1))
        v2_dot = math.sqrt(simpledotproduct(v2, v2))**0.5
        normv1 = ((lastx - x) / v1_dot, (lasty - y) / v1_dot)
        normv2 = ((nextx - x) / v2_dot, (nexty - y) / v2_dot)
        dotproduct = simpledotproduct(normv1, normv2)
        if dotproduct < -1:
            dotproduct = -1.0
        if dotproduct > 1:
            dotproduct = 1.0
        theta = math.acos(dotproduct)
        rel_angles = theta
    else:
        rel_angles = 0.0

    # Convert to degrees
    rel_angles = rel_angles * 180.0 / math.pi
    return rel_angles
