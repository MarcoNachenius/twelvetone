import twelvetone
import unittest

class test_tone_row(unittest.TestCase):
    
    def test_primary_row_transformations(self):
        tc_matrix = twelvetone.twelve_tone_matrix()
        tc_matrix.primary_row = [2, 5, 1, 6, 7, 9, 4, 11, 10, 3, 8, 0]
        
        self.assertEqual(tc_matrix.primary_row_retrograde, [0, 8, 3, 10, 11, 4, 9, 7, 6, 1, 5, 2])
        self.assertEqual(tc_matrix.primary_row_inversion, [2, 11, 3, 10, 9, 7, 0, 5, 6, 1, 8, 4])
        self.assertEqual(tc_matrix.pr_retrograde_inversion, [4, 8, 1, 6, 5, 0, 7, 9, 10, 3, 11, 2])
    
    def test_transpositions(self):
        tc_matrix = twelvetone.twelve_tone_matrix()
        tc_matrix.primary_row = [6, 10, 5, 3, 4, 7, 9, 0, 2, 8, 11, 1]
        octave_up = tc_matrix.transpose_row(tc_matrix.primary_row, 12)
        octave_down = tc_matrix.transpose_row(tc_matrix.primary_row, -12)
        unison = tc_matrix.transpose_row(tc_matrix.primary_row, 12)
        tritone_up = tc_matrix.transpose_row(tc_matrix.primary_row, 6)
        tritone_down = tc_matrix.transpose_row(tc_matrix.primary_row, 6)
        
        self.assertEqual(octave_up, [6, 10, 5, 3, 4, 7, 9, 0, 2, 8, 11, 1])
        self.assertEqual(octave_down, [6, 10, 5, 3, 4, 7, 9, 0, 2, 8, 11, 1])
        self.assertEqual(unison, [6, 10, 5, 3, 4, 7, 9, 0, 2, 8, 11, 1])
        self.assertEqual(tritone_up, [0, 4, 11, 9, 10, 1, 3, 6, 8, 2, 5, 7])
        self.assertEqual(tritone_down, [0, 4, 11, 9, 10, 1, 3, 6, 8, 2, 5, 7])
    
    def test_matrix(self):
        tc_matrix = twelvetone.twelve_tone_matrix()
        tc_matrix.primary_row = [2, 5, 1, 6, 7, 9, 4, 11, 10, 3, 8, 0]
        self.assertEqual(tc_matrix.matrix, [[2, 5, 1, 6, 7, 9, 4, 11, 10, 3, 8, 0], 
                                            [11, 2, 10, 3, 4, 6, 1, 8, 7, 0, 5, 9], 
                                            [3, 6, 2, 7, 8, 10, 5, 0, 11, 4, 9, 1], 
                                            [10, 1, 9, 2, 3, 5, 0, 7, 6, 11, 4, 8], 
                                            [9, 0, 8, 1, 2, 4, 11, 6, 5, 10, 3, 7], 
                                            [7, 10, 6, 11, 0, 2, 9, 4, 3, 8, 1, 5], 
                                            [0, 3, 11, 4, 5, 7, 2, 9, 8, 1, 6, 10], 
                                            [5, 8, 4, 9, 10, 0, 7, 2, 1, 6, 11, 3], 
                                            [6, 9, 5, 10, 11, 1, 8, 3, 2, 7, 0, 4], 
                                            [1, 4, 0, 5, 6, 8, 3, 10, 9, 2, 7, 11], 
                                            [8, 11, 7, 0, 1, 3, 10, 5, 4, 9, 2, 6], 
                                            [4, 7, 3, 8, 9, 11, 6, 1, 0, 5, 10, 2]])
    
    def test_return_transformation(self):
        tc_matrix = twelvetone.twelve_tone_matrix()
        tc_matrix.primary_row = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        
        self.assertEqual(tc_matrix.return_transformation("T0"), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        self.assertEqual(tc_matrix.return_transformation("T7"), [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6])
        self.assertEqual(tc_matrix.return_transformation("I0"), [0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
        self.assertEqual(tc_matrix.return_transformation("I6"), [6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7])
        self.assertEqual(tc_matrix.return_transformation("R0"), [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
        self.assertEqual(tc_matrix.return_transformation("R1"), [0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
        self.assertEqual(tc_matrix.return_transformation("RI0"), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0])
        self.assertEqual(tc_matrix.return_transformation("RI5"), [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5])
    
if __name__ == '__main__':
    unittest.main()