"""
Various functions relating to areas of interests (AOI).
"""


class AreaOfInterest:
    def __init__(self):
        pass

    def check_if_saccade_in_aoi(self, saccade_x, saccade_y, aoi_x, aoi_y,
                                aoi_width, aoi_height):
        """
        Check if the saccade is in the Area of Interest.

        :param saccade_x: Saccade's x-coordinate
        :param saccade_y: Saccade's y-coordinate
        :param aoi_x: Area of Interest's x-coordinate
        :param aoi_y: Area of Interest's y-coordinate
        :param aoi_width: Area of Interest's width
        :param aoi_height: Area of Interest's height
        """
        # The area of interest has 4 values:
        # left_x: aoi_x
        # right_x: aoi_x + aoi_width
        # top_y: aoi_y
        # bot_y: aoi_y + aoi_height
        left_x = aoi_x
        right_x = aoi_x + aoi_width
        top_y = aoi_y
        bot_y = aoi_y + aoi_height

        # Check if the saccade x coordinates are within the aoi
        saccade_within_x = left_x <= saccade_x <= right_x
        if not saccade_within_x:
            return False

        # Check if the saccade y coordinates are within the aoi
        saccade_within_y = top_y <= saccade_y <= bot_y
        if not saccade_within_y:
            return False

        return saccade_within_x and saccade_within_y
