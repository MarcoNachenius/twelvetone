import random
import copy
import numpy as np
import music21
import os

class tone_row (object): 
    
    def __init__(self, tone_row = None, *args, **kwargs):
        if tone_row is None:
            tone_row = []
        self.__prime_row = tone_row
    
    @property
    def prime_row(self):
        return self.__prime_row

    @prime_row.setter
    def prime_row(self, tone_row: list):
        self.__prime_row = tone_row
    
    @classmethod
    def convert_note_to_numbers(cls, first_note: str,
                                second_note: str,
                                third_note: str,
                                fourth_note: str,
                                fifth_note: str,
                                sixth_note: str,
                                seventh_note: str,
                                eighth_note: str,
                                ninth_note: str,
                                tenth_note: str,
                                eleventh_note: str,
                                twelfth_note: str):
        """
        Converts arguments(note names of tone row) into a list of numerical values that correspond to
        the project's numerical convention for note names("C" = 0, "C#"/"Db" = 1, "D" = 2, etc).
        
        Note names are to be entered in uppercase. 
        
        Accidental symbols:
        "#" = sharp
        "b" = flat
        "##" = double-sharp
        "bb" = double-flat
        """
        numerical_list = [first_note, second_note, third_note, fourth_note, fifth_note, sixth_note, seventh_note, eighth_note, ninth_note, tenth_note, eleventh_note, twelfth_note]
        for i, note in enumerate(numerical_list):
            numerical_list[i] = note_names.note_to_number_relations[note]
        return numerical_list
        

    @classmethod
    def generate_random_row(cls):
        """
        Assigns a random 12-tone row as the primary row(P0).
        """
        random_tone_row = list(range(12))
        random.shuffle(random_tone_row)
        return random_tone_row
    
    @classmethod
    def prime_retrograde(cls, prime_row: list):
        """
        Returns R0
        
        R0 is the retrograde of a given tone row that starts on the same note as the prime row.
        """
        pr_retrograde = copy.deepcopy(prime_row)
        pr_retrograde.reverse()
        pr_retrograde = cls.transpose_row(pr_retrograde, prime_row[0] - pr_retrograde[0])
        return pr_retrograde

    
    @classmethod
    def prime_inversion(cls, prime_row: list):
        """
        Returns the inversion(I0) of a given tone row
        """
        row_inversion = [prime_row[0]]
        
        for i in range(1,12):
            semitones = prime_row[i] - prime_row[i-1]
            row_inversion.append(row_inversion[i-1] - semitones)
            if row_inversion[i] > 11:
                row_inversion[i] -= 12
                continue
            if row_inversion[i] < 0:
                row_inversion[i] += 12
        
        return row_inversion
    
    @classmethod
    def prime_retrograde_inversion(cls, prime_row: list):
        """
        Returns RI0
        
        RI0 is the retrograde inversion of a tone row that 
        starts on the same note as the prime row
        """
        pr_ret_inv = cls.prime_inversion(prime_row)
        pr_ret_inv.reverse()
        pr_ret_inv = cls.transpose_row(pr_ret_inv, prime_row[0] -pr_ret_inv[0])
        return pr_ret_inv
    
    @classmethod
    def prime_transformations_list(cls, prime_row: list, include_prime_row = True):
        """
        Returns a list of all prime transformations of a given row
        in the following order:\n
        [P0, R0, I0, RI0]
        """
        if include_prime_row:
            return [prime_row, cls.prime_retrograde(prime_row), cls.prime_inversion(prime_row), cls.prime_retrograde_inversion(prime_row)]
        return [cls.prime_retrograde(prime_row), cls.prime_inversion(prime_row), cls.prime_retrograde_inversion(prime_row)]
    
    @classmethod
    def transpose_row(cls, tone_row: list, semitones: int):
        """
        Moves all notes in a tone row up(positive int) or down(negative int) by a 
        number or semitones.
        
        Returns the transposed list
        """
        transposed_row = copy.deepcopy(tone_row)
        transposed_row = [note + semitones for note in transposed_row]
        for i in range(12):
            if transposed_row[i] > 11:
                transposed_row[i] -= 12
                continue
            if transposed_row[i] < 0:
                transposed_row[i] += 12
        
        return transposed_row
    
    @classmethod
    def get_transformation(cls, tone_row: list, transformation: str):
        """
        Transposition of a tone row occurs when all notes are moved up or
        down by the same amount of semitones.\n
        
        'P' refers to a specific transposition of the prime row.\n
        'P0' is the prime row(first row of the matrix)\n
        
        'I' refers to a specific inversion of the prime row.\n
        'I0' is the prime row(first row of the matrix)\n
        
        'R' refers to a specific retrograde(reverse order) of the prime row.\n
        'R0' is the retrograde of the prime row(prime row in reverse order)\n
        
        'RI' refers to a specific retrograde of the prime row's inversion.\n
        'RI0' is the retrograde of the prime row's inversion(first column of the matrix read from down to up)\n
        
        For example, consider the matrix of the tone row [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:\n
        
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]\n
        [11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n
        [10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]\n
        [9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8]\n
        [8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7]\n
        [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6]\n
        [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5]\n
        [5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4]\n
        [4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3]\n
        [3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2]\n
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1]\n
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]\n
        
        Here are some examples of how specific transpositions are written
        and what their values are:\n
        
        P0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]\n
        T7 = [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6]\n
        I0 = [0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]\n
        I6 = [6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7]\n
        R11 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]\n
        R0 = [0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]\n
        RI1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]\n
        RI6 = [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5]\n
        """
        if transformation == "P0":
            return tone_row
        
        if transformation == "R0":
            return cls.prime_retrograde(tone_row)
        
        if transformation == "I0":
            return cls.prime_inversion(tone_row)
        
        if transformation == "RI0":
            return cls.prime_retrograde_inversion(tone_row)
        
        if transformation.startswith("P"):
            return cls.transpose_row(tone_row, int(transformation[1:]))
        
        if transformation.startswith("RI"):
            return cls.transpose_row(cls.prime_retrograde_inversion(tone_row), int(transformation[2:]))
        
        if transformation.startswith("R"):
            return cls.transpose_row(cls.prime_retrograde(tone_row), int(transformation[1:]))
        
        if transformation.startswith("I"):
            return cls.transpose_row(cls.prime_inversion(tone_row), int(transformation[1:]))
        
    @classmethod
    def find_transformations(cls, prime_row: list, transformed_row: list, find_all = False, row = False, inversion = False,  row_retrograde = False, inv_retrograde = False):
        """
        Returns a list of transformations that apply to the primary row in relation to 
        a given tone row.
        
        By default, this function will search for all transformations.
        (i.e. find_all = True)
        
        If any specific transformations(row, inversion, row_inversion, inv_retrograde) are
        declared as True when this function is invoked, the function will search for them only. 
        """
        if row or inversion or row_retrograde or inv_retrograde:
            find_all = False
        
        if find_all:
            row = True
            inversion = True 
            row_retrograde = True
            inv_retrograde = True
        transformations = []
        for i in range(12):
            if row and transformed_row == cls.transpose_row(prime_row, i):
                transformations.append(f"P{str(i)}")
            
            if row_retrograde and transformed_row == cls.transpose_row(
                cls.prime_retrograde(prime_row), i):
                transformations.append(f"R{str(i)}")
            
            if inversion and transformed_row == cls.transpose_row(
                cls.prime_inversion(prime_row), i):
                transformations.append(f"I{str(i)}")
            
            if inv_retrograde and transformed_row == cls.transpose_row(
                cls.prime_retrograde_inversion(prime_row), i):
                transformations.append(f"RI{str(i)}")
            
        return transformations

class twelve_tone_matrix():
    
    @classmethod
    def generate_twelve_tone_matrix(cls, prime_row: list):
        """
        Returns a twelve-tone matrix(two-dimensional 12*12 array)
        based on a given 12-tone row. 
        P0 is always the first row([0:0] -> [0:12]) and
        I0 is always the first column ([0:0] -> [12:0])
        """
        if len(prime_row) != 12:
            raise ValueError("Row provided is not the right length. (should be 12 tones long)")
        sorted_row = copy.deepcopy(prime_row)
        sorted_row.sort()
        if sorted_row != list(range(12)):
            raise ValueError("The provided tone row is not a valid 12-tone row")
        matrix = [prime_row]
        for i in tone_row.prime_inversion(prime_row):
            if i == prime_row[0]:
                continue
            interval = i - prime_row[0]
            if interval < 0:
                interval += 12
            matrix.append(tone_row.transpose_row(prime_row, interval))
        return matrix
    
    @classmethod
    def row_order(cls, prime_row):
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
    def retrograde_order(cls, prime_row):
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

class combinatoriality():
    
    @classmethod
    def find_hexachordal_combinatorials(cls, prime_row: list, find_all = True, rows=False, retrogrades=False, inversions=False, inv_retrogrades=False):
        """
        Returns a list of transformations that that share combinatorial hexachords with the primary row.
        i.e The first 6 notes of every returned transformation are the same as 
        the first 6 notes of the prime row, regardless of order.\n
        
        If any specific transformations (rows, retrogrades, etc.) are declared as True
        when the function is invoked, the function will search for them only.\n
        
        Returns an empty list if no hexachordal combinatorials exist.\n
        """
        if rows or retrogrades or inversions or inv_retrogrades:
            find_all == False
        if find_all:
            rows = True
            retrogrades = True
            inversions = True
            inv_retrogrades = True
        reference_hexachord = prime_row[:6]
        reference_hexachord.sort()
        hexachords = []
        if rows == False and retrogrades == False and inversions == False and inv_retrogrades == False:
                return None
        
        tt_matrix = twelve_tone_matrix.generate_twelve_tone_matrix(prime_row)
        for i in range(12):
            #iterates through rows of matrix
            if i != 0 and rows:
                trans_row_hexachord = tt_matrix[i][:6]
                trans_row_hexachord.sort()
                if trans_row_hexachord == reference_hexachord:
                    hexachords.append(twelve_tone_matrix.row_order(prime_row)[i])
            if retrogrades:
                trans_row_hexachord = tt_matrix[i][6:]
                trans_row_hexachord.sort()
                if trans_row_hexachord == reference_hexachord:
                    hexachords.append(twelve_tone_matrix.retrograde_order(prime_row)[i])
            
            #iterates through columns of matrix
            if inversions:
                trans_row_hexachord = [tt_matrix[x][i] for x in range(6)]
                trans_row_hexachord.sort()
                if trans_row_hexachord == reference_hexachord:
                    hexachords.append(twelve_tone_matrix.inversion_order(prime_row)[i])
            if inv_retrogrades:
                trans_row_hexachord = [tt_matrix[x][i] for x in range(6,12)]
                trans_row_hexachord.sort()
                if trans_row_hexachord == reference_hexachord:
                    hexachords.append(twelve_tone_matrix.retrograde_inversion_order(prime_row)[i])

        return hexachords
    
    @classmethod
    def find_tetrachordal_combinatorials(cls, prime_row: list):
        """
        Returns a list of transformations that share tetrachordal combinatoriality
        with the prime row.\n
        
        SHORT EXPLANATION
        ==================
        
        """
        combinatorial_transformations = []
        first_tetrachord = prime_row[:4]
        first_tetrachord.sort()
        second_tetrachord = prime_row[4:8]
        second_tetrachord.sort()
        third_tetrachord = prime_row[8:]
        third_tetrachord.sort()
        
        #traversal of twelve-tone matrix
        tt_matrix = twelve_tone_matrix.generate_twelve_tone_matrix(prime_row)
        for i in range (12):
            compared_first_tetrachord = tt_matrix[i][:4]
            compared_first_tetrachord.sort()
            compared_second_tetrachord = tt_matrix[i][4:8]
            compared_second_tetrachord.sort()
            compared_third_tetrachord = tt_matrix[i][8:]
            compared_third_tetrachord.sort()
            
            #ITERATE THROUGH ROWS OF MATRIX
            #checks for row combinatoriality
            first_tetrachord_check = first_tetrachord == compared_first_tetrachord
            second_tetrachord_check = second_tetrachord == compared_second_tetrachord
            third_tetrachord_check = third_tetrachord == compared_third_tetrachord
            if i > 0 and first_tetrachord_check and second_tetrachord_check and third_tetrachord_check:
                combinatorial_transformations.append(twelve_tone_matrix.row_order(prime_row)[i])
            
            #checks for retrograde combinatoriality
            first_tetrachord_check = first_tetrachord == compared_third_tetrachord
            third_tetrachord_check = third_tetrachord == compared_first_tetrachord
            if i > 0 and first_tetrachord_check and second_tetrachord_check and third_tetrachord_check:
                combinatorial_transformations.append(twelve_tone_matrix.retrograde_order(prime_row)[i])
            
            #ITERATE THROUGH COLUMNS OF MATRIX
            matrix_column = [tt_matrix[x][i] for x in range(12)]
            compared_first_tetrachord = matrix_column[:4]
            compared_first_tetrachord.sort()
            compared_second_tetrachord = matrix_column[4:8]
            compared_second_tetrachord.sort()
            compared_third_tetrachord = matrix_column[8:]
            compared_third_tetrachord.sort()
            
            #checks for inversion combinatoriality
            first_tetrachord_check = first_tetrachord == compared_first_tetrachord
            second_tetrachord_check = second_tetrachord == compared_second_tetrachord
            third_tetrachord_check = third_tetrachord == compared_third_tetrachord
            if first_tetrachord_check and second_tetrachord_check and third_tetrachord_check:
                combinatorial_transformations.append(twelve_tone_matrix.inversion_order(prime_row)[i])
            
            #checks for inversion combinatoriality
            first_tetrachord_check = first_tetrachord == compared_third_tetrachord
            third_tetrachord_check = third_tetrachord == compared_first_tetrachord
            if first_tetrachord_check and second_tetrachord_check and third_tetrachord_check:
                combinatorial_transformations.append(twelve_tone_matrix.retrograde_inversion_order(prime_row)[i])
                
        return combinatorial_transformations
    
    @classmethod
    def find_trichordal_combinatorials(cls, prime_row: list):
        """
        Returns a list of transformations that share tetrachordal combinatoriality
        with the prime row.\n
        
        SHORT EXPLANATION
        ==================
        
        """
        combinatorial_transformations = []
        first_tetrachord = prime_row[:3]
        first_tetrachord.sort()
        second_tetrachord = prime_row[3:6]
        second_tetrachord.sort()
        third_tetrachord = prime_row[6:9]
        third_tetrachord.sort()
        fourth_tetrachord = prime_row[9:]
        fourth_tetrachord.sort()
        
        #traversal of twelve-tone matrix
        tt_matrix = twelve_tone_matrix.generate_twelve_tone_matrix(prime_row)
        for i in range (12):
            compared_first_tetrachord = tt_matrix[i][:3]
            compared_first_tetrachord.sort()
            compared_second_tetrachord = tt_matrix[i][3:6]
            compared_second_tetrachord.sort()
            compared_third_tetrachord = tt_matrix[i][6:9]
            compared_third_tetrachord.sort()
            compared_fourth_tetrachord = tt_matrix[i][9:]
            compared_fourth_tetrachord.sort()
            
            #ITERATE THROUGH ROWS OF MATRIX
            #checks for row combinatoriality
            first_tetrachord_check = first_tetrachord == compared_first_tetrachord
            second_tetrachord_check = second_tetrachord == compared_second_tetrachord
            third_tetrachord_check = third_tetrachord == compared_third_tetrachord
            fourth_tetrachord_check = fourth_tetrachord == compared_fourth_tetrachord
            if i > 0 and first_tetrachord_check and second_tetrachord_check and third_tetrachord_check and fourth_tetrachord_check:
                combinatorial_transformations.append(twelve_tone_matrix.row_order(prime_row)[i])
            
            #checks for retrograde combinatoriality
            first_tetrachord_check = first_tetrachord == compared_fourth_tetrachord
            second_tetrachord_check = second_tetrachord == compared_third_tetrachord
            third_tetrachord_check = third_tetrachord == compared_second_tetrachord
            fourth_tetrachord_check = fourth_tetrachord == compared_first_tetrachord
            if i > 0 and first_tetrachord_check and second_tetrachord_check and third_tetrachord_check and fourth_tetrachord_check:
                combinatorial_transformations.append(twelve_tone_matrix.retrograde_order(prime_row)[i])
            
            #ITERATE THROUGH COLUMNS OF MATRIX
            matrix_column = [tt_matrix[x][i] for x in range(12)]
            compared_first_tetrachord = matrix_column[:3]
            compared_first_tetrachord.sort()
            compared_second_tetrachord = matrix_column[3:6]
            compared_second_tetrachord.sort()
            compared_third_tetrachord = matrix_column[6:9]
            compared_third_tetrachord.sort()
            compared_fourth_tetrachord = matrix_column[9:]
            compared_fourth_tetrachord.sort()
            
            #checks for inversion combinatoriality
            first_tetrachord_check = first_tetrachord == compared_first_tetrachord
            second_tetrachord_check = second_tetrachord == compared_second_tetrachord
            third_tetrachord_check = third_tetrachord == compared_third_tetrachord
            fourth_tetrachord_check = fourth_tetrachord == compared_fourth_tetrachord
            if first_tetrachord_check and second_tetrachord_check and third_tetrachord_check and fourth_tetrachord_check:
                combinatorial_transformations.append(twelve_tone_matrix.inversion_order(prime_row)[i])
            
            #checks for inversion combinatoriality
            first_tetrachord_check = first_tetrachord == compared_fourth_tetrachord
            second_tetrachord_check = second_tetrachord == compared_third_tetrachord
            third_tetrachord_check = third_tetrachord == compared_second_tetrachord
            fourth_tetrachord_check = fourth_tetrachord == compared_first_tetrachord
            if first_tetrachord_check and second_tetrachord_check and third_tetrachord_check and fourth_tetrachord_check:
                combinatorial_transformations.append(twelve_tone_matrix.retrograde_inversion_order(prime_row)[i])
                
        return combinatorial_transformations

class note_names():
    
    @classmethod
    @property
    def note_to_number_relations(cls):
        """
        Returns a dictionary of note names and their position within 12 ordered semitones.
        'C' represents position 0
        (key = note name,  val = note number)
        """
        return {
            "Abb": 7,
            "Ab": 8,
            "A": 9,
            "A#": 10,
            "A##": 11,
            "Bbb": 9,
            "Bb": 10,
            "B": 11,
            "B#": 0,
            "B##": 1,
            "Cbb": 10,
            "Cb": 11,
            "C": 0,
            "C#": 1,
            "C##": 2,
            "Dbb": 0,
            "Db": 1,
            "D": 2,
            "D#": 3,
            "D##": 4,
            "Ebb": 2,
            "Eb": 3,
            "E": 4,
            "E#": 5,
            "E##": 6,
            "Fbb": 3,
            "Fb": 4,
            "F": 5,
            "F#": 6,
            "F##": 7,
            "Gbb": 5,
            "Gb": 6,
            "G": 7,
            "G#": 8,
            "G##": 9,
        }
    
    @classmethod
    @property
    def number_to_sharp_relations(cls):
        """
        {note number :  note name}
        
        Returns a dictionary of note names and their position within 12 ordered semitones.
        Every note name that cannot be expressed as a natural is expressed as a sharp.
        'C' represents position 0.
        
        Stockhausen proposed this format as a representation for atonal music that makes use
        of twelve equally-distanced semitones to divide an octave. As such, this library makes
        use of this dictionary as a default representation of numerical keys that represent a
        specific note name.
        """
        return {
            0 :"C",
            1 :"C#",
            2 :"D",
            3 :"D#",
            4 :"E",
            5 :"F",
            6 :"F#",
            7 :"G",
            8 :"G#",
            9 :"A",
            10 :"A#",
            11 :"B",
        }
    
    @classmethod
    @property
    def number_to_sharp_treble_clef_positions(cls):
        """
        {note number :  note name}
        
        Returns a dictionary of note names(between F4 and E5) that appear between the top and
        bottom line of a treble clef.
        Note numbers are ordered to correspond with 12 ordered semitones.
        Every note name that cannot be expressed as a natural is expressed as a sharp.
        'C5' represents position 0.
        
        """
        return {
            0 :"C5",
            1 :"C#5",
            2 :"D5",
            3 :"D#5",
            4 :"E5",
            5 :"F4",
            6 :"F#4",
            7 :"G4",
            8 :"G#4",
            9 :"A4",
            10 :"A#4",
            11 :"B4",
        }
    
    @classmethod
    def convert_numbers_to_note_names(cls, note_number_list: list, dictionary: dict):
        """
        Converts all of the numbers in a tone row(list) or list of tone rows(single-nested list)
        to note names, based on the provided dictionary.
        
        This function does not return a new list, it simply alters the existing list.
        """
        if isinstance(note_number_list[0], int):
            for i, note_number in enumerate(note_number_list):
                note_number_list[i] = dictionary[note_number]
            return
        
        if isinstance(note_number_list[0], list) and isinstance(note_number_list[0][0], int):
            for tone_row in note_number_list:
                for i, note_number in enumerate(tone_row):
                    tone_row[i] = dictionary[note_number]

class intervals(): 
    """
    An interval is the distance between two notes, measured in semitones.
    Interval sizes have specific names, some of which may refer to intervals of the same size.

    For example, the interval of one semitone is commonly referred to as 
    a 'minor second'(m2). If the note 'C' moves up by a semitone to
    the note 'Db', it can be said the 'Db' is a minor second(m2) higher
    than 'C'.
    
    Accidental symbols:
        # = sharp
        b = flat
        ## = double-sharp
        bb = double-flat
        
    Interval abbreviations: 
        m = minor
        M = Major
        P = perfect
        d = diminished
        A = augmented
        AA = double-augmented
        dd = double-diminished
        AAA = triple-augmented
        ddd = triple-diminished
        AAAA = quadruple-augmented
        dddd = quadruple-diminished
    """
    @classmethod
    @property
    def first_interval_sizes(cls):
        return {8: "dddd1", 9: "ddd1", 10: "dd1", 11: "d1", 0: "P1", 1: "A1", 2: "AA1", 3: "AAA1", 4: "AAAA1"}
    
    @classmethod
    @property
    def second_interval_sizes(cls):
        return {10: "ddd2", 11 : "dd2", 0: "d2", 1: "m2", 2: "M2", 3: "A2", 4: "AA2", 5: "AAA2"}
    
    @classmethod
    @property
    def third_interval_sizes(cls):
        return {0 : "ddd3", 1 : "dd3", 2: "d3", 3: "m3", 4: "M3", 5: "A3", 6: "AA3", 7: "AAA3"}
    
    @classmethod
    @property
    def fourth_interval_sizes(cls):
        return {2 : "ddd4", 3 : "dd4", 4: "d4", 5: "P4", 6: "A4", 7: "AA4", 8: "AAA4"}
    
    @classmethod
    @property
    def fifth_interval_sizes(cls):
        return {4: "ddd5", 5 : "dd5", 6: "d5", 7: "P5", 8: "A5", 9: "AA5", 10: "AAA5"}
    
    @classmethod
    @property
    def sixth_interval_sizes(cls):
        return {5: "ddd6", 6 : "dd6", 7: "d6", 8: "m6", 9: "M6", 10: "A6", 11: "AA6", 0: "AAA6"}
    
    @classmethod
    @property
    def seventh_interval_sizes(cls):
        return {7: "ddd7", 8 : "dd7", 9: "d7", 10: "m7", 11: "M7", 0: "A7", 1: "AA7", 2: "AAA7"}
    
    @classmethod
    def semitone_distance(cls, starting_note: str, direction: str, final_note: str):
        """
        Returns the number of semitones between two notes within an octave space
        """
        if starting_note[0].isupper == False:
            raise ValueError(f"Starting note {starting_note[0]} should be written in uppercase")
        if final_note[0].isupper == False:
            raise ValueError(f"Final note {final_note[0]} should be written in uppercase")
        if direction not in {"up", "down"}:
            raise ValueError("Invalid direction indicator, direction can either be 'up' or 'down'")
        if direction == "up":
            semitone_distance = note_names.note_to_number_relations[final_note] - note_names.note_to_number_relations[starting_note]
            if semitone_distance < 0:
                semitone_distance += 12
            return semitone_distance
        
        if direction == "down":
            semitone_distance = note_names.note_to_number_relations[starting_note] - note_names.note_to_number_relations[final_note]
            if semitone_distance < 0:
                semitone_distance += 12
            return semitone_distance
    @classmethod
    def note_interval_name(cls, starting_note: str, direction: str, final_note: str):
        """
        Returns the interval name between two notes.
        eg. interval_name('C', 'up', 'F#') will return 'A4'
        
        Note names should be entered in uppercase.
        
        Accidental symbols:
        # = sharp
        b = flat
        ## = double-sharp
        bb = double-flat
        
        Interval abbreviations: 
        m = minor
        M = Major
        P = perfect
        d = diminished
        A = augmented
        AA = double-augmented
        dd = double-diminished
        AAA = triple-augmented
        ddd = triple-diminished
        AAAA = quadruple-augmented
        dddd = quadruple-diminished
        
        Unison intervals(i.e. interval between two notes that share the same note letter) are expressed as 1
        eg. interval_name('Cb', 'up', 'C#') will return 'AA1'
        
        User should refrain from making use of double sharp/flat notes, even though their use is allowed in this function.
        This functions is written within the context of twelve-tone composition.
        Double sharps/flats are primarily used within a tonal context.
        In twelve-tone composition, double sharps/flats are mostly used in rare cases where it would
        make the readability of the score easier.
        Movements from a note with a double-sharp to a note with a double-flat(or vice versa) is 
        practically unheard of in 12-tone composition, as it would make the music extremely challenging to read
        and serves no practical purpose in visually demonstrating transformations of tone rows.
        """
        if starting_note[0].isupper == False:
            raise ValueError(f"Starting note '{starting_note[0]}' should be written in uppercase")
        if final_note[0].isupper == False:
            raise ValueError(f"Final note '{final_note[0]}' should be written in uppercase")
        if direction not in {"up", "down"}:
            raise ValueError("Invalid direction indicator, direction should be 'up' or 'down'")
        
        note_order = ("A", "B", "C", "D", "E", "F", "G")
        #assumes direction == "true"
        interval_number = note_order.index(final_note[0]) - note_order.index(starting_note[0]) +1
        if interval_number < 1:
            interval_number += 7
        if direction == "down":
            interval_number = 9 - interval_number
        
        if interval_number == 1:
            return cls.first_interval_sizes[cls.semitone_distance(starting_note, direction, final_note)]
        if interval_number == 2:
            return cls.second_interval_sizes[cls.semitone_distance(starting_note, direction, final_note)]
        if interval_number == 3:
            return cls.third_interval_sizes[cls.semitone_distance(starting_note, direction, final_note)]
        if interval_number == 4:
            return cls.fourth_interval_sizes[cls.semitone_distance(starting_note, direction, final_note)]
        if interval_number == 5:
            return cls.fifth_interval_sizes[cls.semitone_distance(starting_note, direction, final_note)]
        if interval_number == 6:
            return cls.sixth_interval_sizes[cls.semitone_distance(starting_note, direction, final_note)]
        if interval_number == 7:
            return cls.seventh_interval_sizes[cls.semitone_distance(starting_note, direction, final_note)]
    
    @classmethod
    def get_transposed_note(cls, starting_note: str, interval_name: str, direction: str):
        """
        Returns the note name of a note that is transposed by a specific interval
        in a specified direction.
        
        For example, if the used wants to find the name of the note that is a major
        second below 'C', the implementation of the function will look as follows:
        
        transposed_note = intervals.get_transposed_note('C', 'M2', 'down')
        (transposed_note = 'Bb')
        
        Accidental symbols:
        # = sharp
        b = flat
        ## = double-sharp
        bb = double-flat
        
        Interval abbreviations: 
        m = minor
        M = Major
        P = perfect
        d = diminished
        A = augmented
        AA = double-augmented
        dd = double-diminished
        AAA = triple-augmented
        ddd = triple-diminished
        AAAA = quadruple-augmented
        dddd = quadruple-diminished
        """
        
        for key in note_names.note_to_number_relations.keys():
            if cls.note_interval_name(starting_note, direction, key) == interval_name:
                return key

class music_xml_writer():#WIP
    
    @classmethod
    def write_twelvetone_report(cls, prime_row: list, file_name: str, directory = None, score_title = None, include_combinatorials = True):
        """
        Creates a .musicxml file with parts in the following order:\n
        -P0\n
        -R0\n
        -I0\n
        -RI0\n
        (if include_combinatorials = True)\n
        -hexachordal combinatorials, if they exist\n
        -tetrachordal combinatorials, if they exist\n
        -trichordal combinatorials, if they exist\n
        
        
        Every part's tone row is written in quarter notes between the top and bottom line of
        the treble clef (between F4 and E5). All notes are written as naturals or sharps(excluding 'E#' and B#').
        
        If directory is not specified, file will be written in 'xml_files' subfolder in the project file.
        
        Warning: If a specific file path is given as a root directory, user might encounter permission errors.
        """
        file_path = cls.create_file_path(directory, file_name)
        full_score = cls.create_twelve_tone_report_xml(prime_row, score_title)
        full_score.write("musicxml", file_path)
        print("\n=========================\nFile successfully written\n=========================")
    
    @classmethod
    def create_twelve_tone_report_xml(cls, prime_row: list, score_title = None, include_combinatorials = True):
        """
        Returns a .musicxml file with parts in the following order:\n
        -P0\n
        -R0\n
        -I0\n
        -RI0\n
        (if include_combinatorials = True)\n
        -hexachordal combinatorials, if they exist\n
        -tetrachordal combinatorials, if they exist\n
        -trichordal combinatorials, if they exist\n
        
        
        Every part's tone row is written in quarter notes between the top and bottom line of
        the treble clef (between F4 and E5). All notes are written as naturals or sharps(excluding 'E#' and B#').
        """
        if score_title is None:
            score_title = "Analysis of a Twelve-tone Row"
        prime_part_names = ["P0", "R0", "I0", "RI0"]
        full_score = music21.stream.Score()
        full_score.insert(0, music21.metadata.Metadata(title = score_title, composer = "", hideFirstNumber = True))
        
        for transformations in prime_part_names:
            part = cls.create_prime_transformation_part(transformations, prime_row)
            full_score.append(part)
        
        if include_combinatorials == False:
            return full_score
        
        combinatorial_hexachords = combinatoriality.find_hexachordal_combinatorials(prime_row)
        for transformations in combinatorial_hexachords:
            part = cls.create_hexachord_combinatorial_part(transformations, prime_row)
            full_score.append(part)
        
        combinatorial_tetrachords = combinatoriality.find_tetrachordal_combinatorials(prime_row)
        for transformations in combinatorial_tetrachords:
            part = cls.create_tetrachord_combinatorial_part(transformations, prime_row)
            full_score.append(part)
        
        return full_score
    
    @classmethod
    def create_stemless_measure(cls, transformation_name: str, prime_row: list):
        """
        Returns a music21 measure object.
        Part consists of twelve stemless quarter notes with a hidden 12/4
        time signature.
        """
        
        measure = music21.stream.Measure()
        measure.timeSignature = music21.meter.TimeSignature('12/4')
        measure.timeSignature.style.hideObjectOnPrint = True
        pr_part_notes = copy.deepcopy((tone_row.get_transformation(prime_row, transformation_name)))
        note_names.convert_numbers_to_note_names(pr_part_notes, note_names.number_to_sharp_treble_clef_positions)
        for pitch in pr_part_notes:
            note = music21.note.Note(pitch)
            note.stemDirection = "noStem"
            measure.append(note)
        
        return measure
    
    @classmethod
    def create_prime_transformation_part(cls, prime_transformation_name: str, prime_row: list):
        """
        Returns a music21 part object.
        Part consists of twelve stemless quarter notes with a hidden 12/4
        time signature.
        """
        measure = cls.create_stemless_measure(prime_transformation_name, prime_row)
        prime_row_part = music21.stream.Part()
        prime_row_part.partName = prime_transformation_name
        prime_row_part.append(measure)
        
        return prime_row_part
    
    @classmethod
    def create_hexachord_combinatorial_part(cls, transformation_name: str, prime_row: list):
        """
        Returns a music21 part object.
        Part consists of twelve stemless quarter notes with a hidden 12/4
        time signature.
        
        Dotted ties are added over each half of the tone row.
        Text is added above the part which indicates that it is a hexachordal combinatorial.
        """
        measure = cls.create_stemless_measure(transformation_name, prime_row)
        comment = music21.expressions.TextExpression("(hexachordal combinatorial)")
        measure.insert(0, comment)
        first_slur = music21.spanner.Slur([measure.notes[0],  measure.notes[5]])
        measure.insert(0.0, first_slur)
        second_slur = music21.spanner.Slur([measure.notes[6],  measure.notes[11]])
        measure.insert(0.0, second_slur)
        hex_row_part = music21.stream.Part()
        hex_row_part.partName = transformation_name
        hex_row_part.append(measure)
        
        return hex_row_part
    
    @classmethod
    def create_tetrachord_combinatorial_part(cls, transformation_name: str, prime_row: list):
        """
        Returns a music21 part object.
        Part consists of twelve stemless quarter notes with a hidden 12/4
        time signature.
        
        Dotted ties are added over each half of the tone row.
        Text is added above the part which indicates that it is a hexachordal combinatorial.
        """
        measure = cls.create_stemless_measure(transformation_name, prime_row)
        comment = music21.expressions.TextExpression("(tetrachordal combinatorial)")
        measure.insert(0, comment)
        first_slur = music21.spanner.Slur([measure.notes[0],  measure.notes[3]])
        measure.insert(0.0, first_slur)
        second_slur = music21.spanner.Slur([measure.notes[4],  measure.notes[7]])
        measure.insert(0.0, second_slur)
        third_slur = music21.spanner.Slur([measure.notes[8],  measure.notes[11]])
        measure.insert(0.0, third_slur)
        tetra_row_part = music21.stream.Part()
        tetra_row_part.partName = transformation_name
        tetra_row_part.append(measure)
        
        return tetra_row_part
    
    @classmethod
    def create_file_path(cls, directory, file_name):
        """
        Returns a file path(including the .musicxml file) as a normalized string.
        
        If directory = None, the function will create a directory within the project
        sub folder('xml_files')
        """
        if directory is not None:
            directory = os.path.normpath(directory)
            if os.path.exists(directory) == False:
                raise ValueError(f"Specified directory('{directory}')\n does not exist")
        if directory is None:
            directory = os.path.normpath("./xml_files/")
        return os.path.join(directory, file_name)
    
    


if __name__ == "__main__":
    
    found_tetrachord = False
    while not found_tetrachord:
        prime_row = tone_row.generate_random_row()
        tetrachords = combinatoriality.find_hexachordal_combinatorials(prime_row)
        if len(tetrachords) > 0:
            print("Row with tetrachordal combinatoriality has been found!")
            print(prime_row)
            print(tetrachords)
            music_xml_writer.write_twelvetone_report(prime_row, "test_file")
            found_tetrachord = True
    #print(combinatoriality.find_tetrachordal_combinatorials(list(range(12))))
