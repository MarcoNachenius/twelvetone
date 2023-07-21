import numpy as np
from tone_row import tone_row

class twelve_tone_matrix():
    
    @classmethod
    def generate_twelve_tone_matrix(cls, prime_row: np.ndarray) -> np.ndarray:
        """
        Returns a twelve-tone matrix(two-dimensional 12*12 array)
        based on a given 12-tone row. \n
        P0 is always the first row([0:0] -> [0:12])\n
        I0 is always the first column ([0:0] -> [12:0])
        """
        tone_row.validate_row(prime_row)
        matrix = np.zeros((12,12), dtype=int)
        matrix[0] = prime_row # add first row
        very_first_note = prime_row[0]
        first_column = tone_row.prime_inversion(prime_row)
        for i in range(1, 12):
            semitone_difference = first_column[i] - very_first_note
            matrix[i] = tone_row.transpose_row(prime_row, semitone_difference)
        return matrix
    
    @classmethod
    def row_order(cls, prime_row: np.ndarray) -> list:
        """
        Returns the order of row transpositions of 
        the 12-tone matrix from top to bottom
        """
        row_order = ["P0"]
        reference_note = prime_row[0]
        prime_inversion = tone_row.prime_inversion(prime_row)
        for i in range(1, 12):
            semitones_up = prime_inversion[i] - reference_note
            if semitones_up < 0:
                semitones_up += 12
            row_order.append(f"P{str(semitones_up)}")
        return row_order
    
    @classmethod
    def retrograde_order(cls, prime_row: np.ndarray) -> list:
        """
        Returns the order of retrograde transpositions of 
        the 12-tone matrix from top to bottom
        """
        row_order = []
        tt_matrix = cls.generate_twelve_tone_matrix(prime_row)
        last_column = [i[11] for i in tt_matrix]
        reference_note = prime_row[0]
        for i in range(12):
            semitones_up = last_column[i] - reference_note
            if semitones_up < 0:
                semitones_up += 12
            row_order.append(f"R{str(semitones_up)}")
        return row_order
    
    @classmethod
    def inversion_order(cls, prime_row):
        """
        Returns the order of inversion transpositions of 
        the 12-tone matrix from left to right
        """
        row_order = ["I0"]
        #The first row of the 12-tone matrix represents the first note of every inversion
        reference_note = prime_row[0]
        for i in range(1, 12):
            semitones_up = prime_row[i] - reference_note
            if semitones_up < 0:
                semitones_up += 12
            row_order.append(f"I{str(semitones_up)}")
        return row_order
    
    @classmethod
    def retrograde_inversion_order(cls, prime_row):
        """
        Returns the order of retrograde inversion transpositions of 
        the 12-tone matrix from left to right
        """
        row_order = []
        #The last row of the 12-tone matrix represents the first note of every retrograde inversion
        ret_inv_row = cls.generate_twelve_tone_matrix(prime_row)[11]
        reference_note = prime_row[0]
        for i in range(12):
            semitones_up = ret_inv_row[i] - reference_note
            if semitones_up < 0:
                semitones_up += 12
            row_order.append(f"RI{str(semitones_up)}")
        return row_order
    
    @classmethod
    def display_matrix(cls, prime_row: list):
        print("=======================\n" + "Random tone row:\n" + "=======================" )
        print(prime_row)
        print("\n=======================\n" + "Pone row matrix:\n" + "=======================\n" )
        print(cls.inversion_order(prime_row))
        for i in range(12):
            print(cls.row_order(prime_row)[i] + str(cls.generate_twelve_tone_matrix(prime_row)[i]) + cls.retrograde_order(prime_row)[i])
        print(cls.retrograde_inversion_order(prime_row))