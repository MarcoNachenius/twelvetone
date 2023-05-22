import TwelveTone as tt
import unittest

class test_tone_row(unittest.TestCase):
    
    def test_prime_row_transformations(self):
        tc_matrix = tt.twelve_tone_matrix()
        tc_matrix.prime_row = [2, 5, 1, 6, 7, 9, 4, 11, 10, 3, 8, 0]
        
        self.assertEqual(tc_matrix.pr_retrograde, [2, 10, 5, 0, 1, 6, 11, 9, 8, 3, 7, 4])
        self.assertEqual(tc_matrix.pr_inversion, [2, 11, 3, 10, 9, 7, 0, 5, 6, 1, 8, 4])
        self.assertEqual(tc_matrix.pr_retrograde_inversion, [2, 6, 11, 4, 3, 10, 5, 7, 8, 1, 9, 0])
    
    def test_transpositions(self):
        tc_matrix = tt.twelve_tone_matrix()
        tc_matrix.prime_row = [6, 10, 5, 3, 4, 7, 9, 0, 2, 8, 11, 1]
        octave_up = tc_matrix.transpose_row(tc_matrix.prime_row, 12)
        octave_down = tc_matrix.transpose_row(tc_matrix.prime_row, -12)
        unison = tc_matrix.transpose_row(tc_matrix.prime_row, 12)
        tritone_up = tc_matrix.transpose_row(tc_matrix.prime_row, 6)
        tritone_down = tc_matrix.transpose_row(tc_matrix.prime_row, -6)
        
        self.assertEqual(octave_up, [6, 10, 5, 3, 4, 7, 9, 0, 2, 8, 11, 1])
        self.assertEqual(octave_down, [6, 10, 5, 3, 4, 7, 9, 0, 2, 8, 11, 1])
        self.assertEqual(unison, [6, 10, 5, 3, 4, 7, 9, 0, 2, 8, 11, 1])
        self.assertEqual(tritone_up, [0, 4, 11, 9, 10, 1, 3, 6, 8, 2, 5, 7])
        self.assertEqual(tritone_down, [0, 4, 11, 9, 10, 1, 3, 6, 8, 2, 5, 7])
    
    def test_matrix(self):
        tc_matrix = tt.twelve_tone_matrix()
        tc_matrix.prime_row = [2, 5, 1, 6, 7, 9, 4, 11, 10, 3, 8, 0]
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
        tc_tone_row = tt.tone_row()
        tc_tone_row.prime_row = list(range(12))
        
        self.assertEqual(tc_tone_row.return_transformation(tc_tone_row.prime_row, "P0"), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        self.assertEqual(tc_tone_row.return_transformation(tc_tone_row.prime_row, "P7"), [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6])
        self.assertEqual(tc_tone_row.return_transformation(tc_tone_row.prime_row, "I0"), [0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
        self.assertEqual(tc_tone_row.return_transformation(tc_tone_row.prime_row, "I6"), [6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7])
        self.assertEqual(tc_tone_row.return_transformation(tc_tone_row.prime_row, "R11"), [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
        self.assertEqual(tc_tone_row.return_transformation(tc_tone_row.prime_row, "R0"), [0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
        self.assertEqual(tc_tone_row.return_transformation(tc_tone_row.prime_row, "RI1"), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0])
        self.assertEqual(tc_tone_row.return_transformation(tc_tone_row.prime_row, "RI6"), [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5])
    
    def test_find_transformations(self):
        tc_matrix = tt.twelve_tone_matrix(list(range(12)))
        tc_matrix.prime_row = list(range(12))
        
        self.assertEqual(tc_matrix.find_transformations([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], row=True), ["P0"])
        self.assertEqual(tc_matrix.find_transformations([7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6], row=True), ["P7"])
        self.assertEqual(tc_matrix.find_transformations([0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1], inversion=True), ["I0"])
        self.assertEqual(tc_matrix.find_transformations([6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7], inversion=True), ["I6"])
        self.assertEqual(tc_matrix.find_transformations([11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0], row_retrograde=True), ["R11"])
        self.assertEqual(tc_matrix.find_transformations([0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1], row_retrograde=True), ["R0"])
        self.assertEqual(tc_matrix.find_transformations([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0], inv_retrograde=True), ["RI1"])
        self.assertEqual(tc_matrix.find_transformations([6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5], find_all=True), ["P6", "RI6"])
    
    def test_row_orders(self): 
        tc_matrix = tt.twelve_tone_matrix()
        tc_matrix.prime_row = list(range(12))
        
        self.assertEqual(tc_matrix.row_order, ["P0", "P11", "P10", "P9", "P8", "P7", "P6", "P5", "P4", "P3", "P2", "P1"])
        self.assertEqual(tc_matrix.retrograde_order, ["R11", "R10", "R9", "R8", "R7", "R6", "R5", "R4", "R3", "R2", "R1", "R0"])
        self.assertEqual(tc_matrix.inversion_order, ["I0", "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "I10", "I11"])
        self.assertEqual(tc_matrix.ret_inv_order, ["RI1", "RI2", "RI3", "RI4", "RI5", "RI6", "RI7", "RI8", "RI9", "RI10", "RI11", "RI0"])

class test_intervals(unittest.TestCase):

    def test_semitone_distance(self):
        self.assertEqual(tt.intervals.semitone_distance("A", "up", "A#"), 1)
    
    def test_note_interval_name(self):
        self.assertEqual(tt.intervals.note_interval_name("A##", "down", "E##"), "P4")
    
    def test_get_transposed_note(self):
        self.assertEqual(tt.intervals.get_transposed_note("A#", "m7", "down"), "B#")
if __name__ == '__main__':
    unittest.main()