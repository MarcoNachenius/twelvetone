
import unittest
import numpy as np
import math
from tone_row import tone_row
#from music_xml_writer import music_xml_writer
from note_names import note_names
from intervals import intervals
from combinatoriality import combinatoriality
from twelve_tone_matrix import twelve_tone_matrix
from database_permutation_writer import permutation_calculator


class test_tone_row(unittest.TestCase):
    
    def test_prime_row_transformations(self):
        prime_row = np.array([2, 5, 1, 6, 7, 9, 4, 11, 10, 3, 8, 0])
        self.assertTrue(np.array_equal(tone_row.prime_retrograde(prime_row), np.array([2, 10, 5, 0, 1, 6, 11, 9, 8, 3, 7, 4])))
        self.assertTrue(np.array_equal(tone_row.prime_inversion(prime_row), np.array([2, 11, 3, 10, 9, 7, 0, 5, 6, 1, 8, 4])))
        self.assertTrue(np.array_equal(tone_row.prime_retrograde_inversion(prime_row), np.array([2, 6, 11, 4, 3, 10, 5, 7, 8, 1, 9, 0])))
    
    def test_transpositions(self):
        prime_row = np.array([6, 10, 5, 3, 4, 7, 9, 0, 2, 8, 11, 1])
        octave_up = tone_row.transpose_row(prime_row, 12)
        two_octaves_down = tone_row.transpose_row(prime_row, -24)
        unison = tone_row.transpose_row(prime_row, 12)
        tritone_up = tone_row.transpose_row(prime_row, 6)
        tritone_down = tone_row.transpose_row(prime_row, -6)
        self.assertTrue(np.array_equal(octave_up, np.array([6, 10, 5, 3, 4, 7, 9, 0, 2, 8, 11, 1])))
        self.assertTrue(np.array_equal(two_octaves_down, np.array([6, 10, 5, 3, 4, 7, 9, 0, 2, 8, 11, 1])))
        self.assertTrue(np.array_equal(unison, np.array([6, 10, 5, 3, 4, 7, 9, 0, 2, 8, 11, 1])))
        self.assertTrue(np.array_equal(tritone_up, np.array([0, 4, 11, 9, 10, 1, 3, 6, 8, 2, 5, 7])))
        self.assertTrue(np.array_equal(tritone_down, np.array([0, 4, 11, 9, 10, 1, 3, 6, 8, 2, 5, 7])))
    
    def test_return_transformation(self):
        tc_tone_row = tone_row()
        tc_tone_row.prime_row = np.arange(12)
        self.assertTrue(np.array_equal(tone_row.get_transformation(tc_tone_row.prime_row, "P0"), np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])))
        self.assertTrue(np.array_equal(tone_row.get_transformation(tc_tone_row.prime_row, "P7"), np.array([7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6])))
        self.assertTrue(np.array_equal(tone_row.get_transformation(tc_tone_row.prime_row, "I0"), np.array([0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])))
        self.assertTrue(np.array_equal(tone_row.get_transformation(tc_tone_row.prime_row, "I6"), np.array([6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7])))
        self.assertTrue(np.array_equal(tone_row.get_transformation(tc_tone_row.prime_row, "R11"), np.array([11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])))
        self.assertTrue(np.array_equal(tone_row.get_transformation(tc_tone_row.prime_row, "R0"), np.array([0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])))
        self.assertTrue(np.array_equal(tone_row.get_transformation(tc_tone_row.prime_row, "RI1"), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0])))
        self.assertTrue(np.array_equal(tone_row.get_transformation(tc_tone_row.prime_row, "RI6"), np.array([6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5])))
        
    def test_convert_note_to_numbers(self):
        self.assertTrue(np.array_equal(tone_row.convert_notes_to_numbers("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"), np.arange(12)))
    
    def test_row_interval_sizes(self):
        tc_interval_sizes = np.ones(11, dtype=int)
        self.assertTrue(np.array_equal(tone_row.row_interval_sizes(np.arange(12)), tc_interval_sizes))
    
class test_twelve_tone_matrix(unittest.TestCase):
    
    def test_matrix(self):
        prime_row = np.array([2, 5, 1, 6, 7, 9, 4, 11, 10, 3, 8, 0])
        self.assertTrue(np.array_equal(twelve_tone_matrix.generate_twelve_tone_matrix(prime_row), np.array(
                                            [[2, 5, 1, 6, 7, 9, 4, 11, 10, 3, 8, 0], 
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
                                            [4, 7, 3, 8, 9, 11, 6, 1, 0, 5, 10, 2]])))
    
    def test_find_transformations(self):
        prime_row = np.arange(12)
        self.assertEqual(tone_row.find_transformations(prime_row, np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]), row=True), ["P0"])
        self.assertEqual(tone_row.find_transformations(prime_row, np.array([7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6]), row=True), ["P7"])
        self.assertEqual(tone_row.find_transformations(prime_row, np.array([0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]), inversion=True), ["I0"])
        self.assertEqual(tone_row.find_transformations(prime_row, np.array([6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7]), inversion=True), ["I6"])
        self.assertEqual(tone_row.find_transformations(prime_row, np.array([11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]), row_retrograde=True), ["R11"])
        self.assertEqual(tone_row.find_transformations(prime_row, np.array([0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]), row_retrograde=True), ["R0"])
        self.assertEqual(tone_row.find_transformations(prime_row, np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]), inv_retrograde=True), ["RI1"])
        self.assertEqual(tone_row.find_transformations(prime_row, np.array([6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5]), find_all=True), ["P6", "RI6"])
    
    def test_row_orders(self): 
        prime_row = np.arange(12)
        self.assertEqual(twelve_tone_matrix.row_order(prime_row), ["P0", "P11", "P10", "P9", "P8", "P7", "P6", "P5", "P4", "P3", "P2", "P1"])
        self.assertEqual(twelve_tone_matrix.retrograde_order(prime_row), ["R11", "R10", "R9", "R8", "R7", "R6", "R5", "R4", "R3", "R2", "R1", "R0"])
        self.assertEqual(twelve_tone_matrix.inversion_order(prime_row), ["I0", "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "I10", "I11"])
        self.assertEqual(twelve_tone_matrix.retrograde_inversion_order(prime_row), ["RI1", "RI2", "RI3", "RI4", "RI5", "RI6", "RI7", "RI8", "RI9", "RI10", "RI11", "RI0"])

class test_intervals(unittest.TestCase):

    def test_semitone_distance(self):
        self.assertEqual(intervals.semitone_distance("A", "up", "A#"), 1)
        self.assertEqual(intervals.semitone_distance("A", "up", "G#"), 11)
    
    def test_note_interval_name(self):
        self.assertEqual(intervals.note_interval_name("A##", "down", "E##"), "P4")
    
    def test_get_transposed_note(self):
        self.assertEqual(intervals.get_transposed_note("A#", "m7", "down"), "B#")

class test_combinatoriality(unittest.TestCase):
    
    def test_find_hexachordal_combinatoriality(self):
        prime_row = np.arange(12)
        self.assertEqual(combinatoriality.find_hexachordal_combinatorials(prime_row), ['I5', 'R5', 'RI0'])
        self.assertEqual(combinatoriality.find_tetrachordal_combinatorials(prime_row), ['RI0'])
        self.assertEqual(combinatoriality.find_trichordal_combinatorials(prime_row), ['RI0'])
        
        prime_row = [10, 8, 0, 9, 4, 6, 3, 7, 1, 5, 11, 2]
        self.assertEqual(combinatoriality.find_hexachordal_combinatorials(prime_row), ['RI11'])
    

class test_note_names(unittest.TestCase):
    
    def test_convert_numbers_to_note_names(self):
        prime_row = np.arange(12)
        self.assertEqual(note_names.convert_numbers_to_note_names(prime_row, note_names.number_to_sharp_treble_clef_positions), ['C5', 'C#5', 'D5', 'D#5', 'E5', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4'])

class test_database_permutation_writer(unittest.TestCase):
    
    def test_find_permutation(self):
        self.assertTrue(np.array_equal(permutation_calculator.find_permutation(0, 5), np.arange(5)))
        self.assertTrue(np.array_equal(permutation_calculator.find_permutation(119, 5), np.flip(np.arange(5))))

if __name__ == '__main__':
    unittest.main()