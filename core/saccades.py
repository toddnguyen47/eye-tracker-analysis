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


def calc_abs_angle(cur_coords, prev_coords, use_degrees=True):
    """
    Calculate the absolute angle of 2 fixations using atan2

    # ARGUMENTS
    cur_coords  -> Current coordinates in [x, y] form
    prev_coords -> Previous coordinates in [x, y] form
    use_degrees -> True to return in degrees, False to return in radians
    """
    x = float(cur_coords[0])
    y = float(cur_coords[1])
    prev_x = float(prev_coords[0])
    prev_y = float(prev_coords[1])

    x_dist = x - prev_x
    y_dist = y - prev_y

    abs_angle = math.atan2(y_dist, x_dist)
    # Convert to degrees if needed
    abs_angle = abs_angle * 180.0 / math.pi if use_degrees else abs_angle
    return abs_angle


def calc_rel_angle(cur_coords, prev_coords, next_coords, use_degrees=True):
    """
    Calculate the relative angle of 2 fixations using atan2

    CurrentX and CurrentY will be the "origin" in a cartesian coordinate
    Quadrant:
        |
      2 | 1
    ---------
      3 | 4
        |

    Truth Table for Quadrants: Greater than Zero Booleans
    e.g. If both vectors have x coordinates that are greater than 0
    and both coordinates have y coordinates that are greater than 0,
    then both vectors are in the same quadrant.
    
    Quad1: ( 1,  1)
    Quad2: (-1,  1)
    Quad3: (-1, -1)
    Quad4: ( 1, -1)
    
    Vector1 | Vector2 | Quadrant
    x1 | y1 | x2 | y2 |
    ----------------------------------------
    T  | T  | T  | T  | Same quadrant
    T  | T  | F  | T  | Horizontal quadrants
    T  | T  | F  | F  | Diagonal quadrants
    T  | T  | T  | F  | Vertical quadrants

    # ARGUMENTS
    cur_coords  -> Current coordinates in [x, y] form
    prev_coords -> Previous coordinates in [x, y] form
    next_coords -> Next coordinates in [x, y] form
    use_degrees -> True to return in degrees, False to return in radians
    """
    lastx = float(prev_coords[0])
    lasty = float(prev_coords[1])

    x = float(cur_coords[0])
    y = float(cur_coords[1])

    nextx = float(next_coords[0])
    nexty = float(next_coords[1])
    
    # If at any ime angle1 or angle2 == math.pi, that angle will be set to 0
    diffx1 = (lastx - x)
    diffy1 = (lasty - y)
    angle1 = math.atan2(abs(diffy1), abs(diffx1))
    angle1 = 0 if angle1 == math.pi else angle1

    # Is x1 and y1 greater than zero?
    x1_greater_than_zero = diffx1 > 0
    y1_greater_than_zero = diffy1 > 0

    diffx2 = (nextx - x)
    diffy2 = (nexty - y)
    angle2 = math.atan2(abs(diffy2), abs(diffx2))
    angle2 = 0 if angle2 == math.pi else angle2

    # Is x2 and y2 greater than zero?
    x2_greater_than_zero = diffx2 > 0
    y2_greater_than_zero = diffy2 > 0

    # If the vectors are in the same quadrant, then the formula is
    # abs(angle1 - angle2)
    if x1_greater_than_zero == x2_greater_than_zero and \
       y1_greater_than_zero == y2_greater_than_zero:
        rel_angle = abs(angle1 - angle2)
    # If the vectors are in horizontal quadrants, then the formula is
    # math.pi - angle1 - angle2
    elif x1_greater_than_zero != x2_greater_than_zero and \
            y1_greater_than_zero == y2_greater_than_zero:
        rel_angle = math.pi - angle1 - angle2
    # If the vectors are in diagonal quadrants, then the formula is
    # min((math.pi - angle1 + angle2), (math.pi - angle2 + angle1))
    elif x1_greater_than_zero != x2_greater_than_zero and \
            y1_greater_than_zero != y2_greater_than_zero:
        rel_angle = min((math.pi - angle1 + angle2), (math.pi - angle2 + angle1))
    # If the vectors are in vertical quadrants, then the formula is
    # angle1 + angle2
    elif x1_greater_than_zero == x2_greater_than_zero and \
            y1_greater_than_zero != y2_greater_than_zero:
        rel_angle = angle1 + angle2
    # Else, return an error
    else:
        raise ValueError("Could not find quadrants for the two vectors.")

    # Convert to degrees if needed
    rel_angle = rel_angle * 180.0 / math.pi if use_degrees else rel_angle
    return rel_angle
