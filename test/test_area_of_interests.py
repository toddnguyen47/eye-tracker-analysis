import unittest
from core.area_of_interest import AreaOfInterest


class AreaOfInterestTest(unittest.TestCase):
    saccade_x = 20
    saccade_y = 20
    aoi_x = 10
    aoi_y = 10
    aoi_width = 50
    aoi_height = 50

    def setUp(self):
        self.aoi_obj = AreaOfInterest()

    def test_correct_check_if_saccade_in_aoi(self):
        """
        The saccade is indeed in the aoi
        """
        self.assertTrue(self.aoi_obj.check_if_saccade_in_aoi(self.saccade_x,
                        self.saccade_y, self.aoi_x, self.aoi_y, self.aoi_width, self.aoi_height))


    def test_correct_edge_left_check_if_saccade_in_aoi(self):
        """
        Check if the function can detect edge cases, on the left side
        """
        temp_saccade_x = self.aoi_x
        self.assertTrue(self.aoi_obj.check_if_saccade_in_aoi(temp_saccade_x,
                        self.saccade_y, self.aoi_x, self.aoi_y, self.aoi_width, self.aoi_height))


    def test_correct_edge_right_check_if_saccade_in_aoi(self):
        """
        Check if the function can detect edge cases, on the right side
        """
        temp_saccade_x = self.aoi_x + self.aoi_width
        self.assertTrue(self.aoi_obj.check_if_saccade_in_aoi(temp_saccade_x,
                        self.saccade_y, self.aoi_x, self.aoi_y, self.aoi_width, self.aoi_height))


    def test_correct_edge_top_check_if_saccade_in_aoi(self):
        """
        Check if the function can detect edge cases, on the top side
        """
        temp_saccade_y = self.aoi_y
        self.assertTrue(self.aoi_obj.check_if_saccade_in_aoi(self.saccade_x,
                        temp_saccade_y, self.aoi_x, self.aoi_y, self.aoi_width, self.aoi_height))


    def test_correct_edge_bot_check_if_saccade_in_aoi(self):
        """
        Check if the function can detect edge cases, on the bottom side
        """
        temp_saccade_y = self.aoi_y + self.aoi_width
        self.assertTrue(self.aoi_obj.check_if_saccade_in_aoi(self.saccade_x,
                        temp_saccade_y, self.aoi_x, self.aoi_y, self.aoi_width, self.aoi_height))


    def test_left_incorrect_check_if_saccade_in_aoi(self):
        """
        Test if the saccade is NOT in the aoi on the left side
        """
        temp_saccade_x = self.aoi_x - self.aoi_x
        self.assertFalse(self.aoi_obj.check_if_saccade_in_aoi(temp_saccade_x,
                         self.saccade_y, self.aoi_x, self.aoi_y, self.aoi_width, self.aoi_height))


    def test_right_incorrect_check_if_saccade_in_aoi(self):
        """
        Test if the saccade is NOT in the aoi on the right side
        """
        temp_saccade_x = self.aoi_x + self.aoi_x + self.aoi_width
        self.assertFalse(self.aoi_obj.check_if_saccade_in_aoi(temp_saccade_x,
                         self.saccade_y, self.aoi_x, self.aoi_y, self.aoi_width, self.aoi_height))


    def test_top_incorrect_check_if_saccade_in_aoi(self):
        """
        Test if the saccade is NOT in the aoi on the top side.
        """
        temp_saccade_y = self.aoi_y - self.aoi_y
        self.assertFalse(self.aoi_obj.check_if_saccade_in_aoi(self.saccade_x,
                         temp_saccade_y, self.aoi_x, self.aoi_y, self.aoi_width, self.aoi_height))

    def test_bot_incorrect_check_if_saccade_in_aoi(self):
        """
        Test if the saccade is NOT in the aoi on the bot side.
        """
        temp_saccade_y = self.aoi_y + self.aoi_y + self.aoi_height
        self.assertFalse(self.aoi_obj.check_if_saccade_in_aoi(self.saccade_x,
                         temp_saccade_y, self.aoi_x, self.aoi_y, self.aoi_width, self.aoi_height))
