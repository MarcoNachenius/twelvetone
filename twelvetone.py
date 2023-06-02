"""
This library is designed for the creation, analysis and graphic representation of 12-tone music.


SHORT INTRODUCTION
====================
In Western music, the octave is divided into twelve equal parts that correspond to specific notes.
This means that there are a total of 12 unique notes. 

This program will use numerical values instead of note names to make the numerical logic clearer
to a person who may not be familiar with how the relationship between pitch and note-names work in Western music.
The reader only needs to understand how this principle works on a numerical level.

Notes are ordered incrementally,
i.e. [0,1,2,3,4,5,6,7,8,9,10,11] = [C,C#,D,D#,E,F,Gb,G,G#,A,Bb,B]  
    ('C' is arbitrarily chosen as note 0 in this example)

The distance between two notes is measured in semitones. For example,
note 5 is two semitones higher than note 3 or four semitones lower than note 9.

This series of notes repeats itself once the end of the index is reached. i.e. 
...0,1,2,3,4,5,6,7,8,9,10,11,0,1,2,3,4,5,6,7,8,9,10,11,0,1,2,3,4,5,6,7,8,9,10,11...

For example, note 1 can be understood to be two semitones above 11
and three semitones below 10. This should lead the reader to the conclusion that
the distance between 0 and 1 can be simultaneously be expressed as the note
one semitone above 0 or eleven semitones below 0.

It is not important for the reader to know why or how this concept is implemented in music.
It is only important to understand that one note may reach another by moving up or down a 
certain number of steps in the aforementioned repeating series. 

In the 1920's Arnold Schoenberg invented a form of composition named 12-tone serialism.
This form of composition has one fundamental principle:
if a specific note is used, all other 11 notes must be used before it may be used again.
This gave rise to the use of a tone-row. A tone-row is a pre-selected set of 12 unique notes. 

Schoenberg found that a different, yet invariably related tone-row consisting of 12 unique notes that
can be generated from the primary tone-row by means of inversion. 
Creating a tone-row by inversion is achieved by reversing distance of traversal between every note of a tone row. 


For example, if we take the tone-row [2,5,1,6,7,9,4,11,10,3,8,0] the distances between notes may be expressed as follows:
 (+3) (-4) (+5) (+1) (+2) (-5) (-5)  (-1)  (+5) (+5) (+4)
  |    |    |    |    |    |    |     |     |    |    |
  v    v    v    v    v    v    v     v     v    v    v
2    5    1    6    7    9    4    11    10    3    8    0

By reversing the traversal of distance between every note, the inversion is generated as follows:
 (-3)  (+4) (-5)  (-1) (-2) (+5) (+5) (+1) (-5) (-5) (-4)
  |     |    |     |    |    |    |    |    |    |    |
  v     v    v     v    v    v    v    v    v    v    v
2   11     3    10    9    7    0    5    6    1    8    4

If every note of a tone row (or its inversion) is uniformly moved up or down by the same number of semitones,
it is referred to as a transposition. Schoenberg devised the 12-tone matrix as a way of representing every
possible transposition. A 12-tone matrix is a 12*12 two-dimensional array. The first row of the array(read from
left to right) is the primary tone-row. The first column(read from top to bottom) represents the inversion
of the primary tone-row. Every row of the matrix is a unique transposition of the tone-row,
and every column a unique transposition of the tone-row's inversion.

For example, the 12-tone matrix of the tone-row mentioned above will look as follows:
[2, 5, 1, 6, 7, 9, 4, 11, 10, 3, 8, 0]
[11, 2, 10, 3, 4, 6, 1, 8, 7, 0, 5, 9]
[3, 6, 2, 7, 8, 10, 5, 0, 11, 4, 9, 1]
[10, 1, 9, 2, 3, 5, 0, 7, 6, 11, 4, 8]
[9, 0, 8, 1, 2, 4, 11, 6, 5, 10, 3, 7]
[7, 10, 6, 11, 0, 2, 9, 4, 3, 8, 1, 5]
[0, 3, 11, 4, 5, 7, 2, 9, 8, 1, 6, 10]
[5, 8, 4, 9, 10, 0, 7, 2, 1, 6, 11, 3]
[6, 9, 5, 10, 11, 1, 8, 3, 2, 7, 0, 4]
[1, 4, 0, 5, 6, 8, 3, 10, 9, 2, 7, 11]
[8, 11, 7, 0, 1, 3, 10, 5, 4, 9, 2, 6]
[4, 7, 3, 8, 9, 11, 6, 1, 0, 5, 10, 2]

A notable feature of Schoenberg's 12-tone matrix is that every number spanning
from top-left to bottom-right ([0][0], [1][1], [2][2], [3][3] etc.) will always be
identical, regardless of which tone-row is used.
"""

import random
import copy
import numpy as np
import music21
import os

class tone_row (object): 
    
    def __init__(self, tone_row=None, *args, **kwargs):
        if tone_row is None:
            tone_row = []
        self.__prime_row = tone_row
    
    @property
    def prime_row(self):
        return self.__prime_row

    @prime_row.setter
    def prime_row(self, tone_row: list):
        self.__prime_row = tone_row
        
    def assign_random_row(self):
        """
        Assigns a random 12-tone row as the primary row(P0).
        """
        random_tone_row = list(range(12))
        random.shuffle(random_tone_row)
        self.prime_row = random_tone_row
    
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
        """
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

class twelve_tone_matrix(tone_row):
    
    def __init__(self, *args, **kwargs):
        tone_row.__init__(self)
    
    @classmethod
    def generate_twelve_tone_matrix(cls, prime_row: list):
        """
        Returns a twelve-tone matrix(two-dimensional 12*12 array)
        based on a given 12-tone row. 
        P0 is always the first row([0:0] -> [0:12]) and
        I0 is always the first column ([0:0] -> [12:0])
        """
        if len(prime_row) != 12:
            print("Warning: row provided is not the right length. (should be 12 tones long)")
        sorted_row = copy.deepcopy(prime_row)
        sorted_row.sort()
        if sorted_row != list(range(12)):
            print("Warning: the provided tone row is not a valid 12-tone row")
        matrix = [prime_row]
        for i in cls.prime_inversion(prime_row):
            if i == prime_row[0]:
                continue
            interval = i - prime_row[0]
            if interval < 0:
                interval += 12
            matrix.append(cls.transpose_row(prime_row, interval))
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
    
    def display_matrix(self):
        print("=======================\n" + "Random tone row:\n" + "=======================" )
        print(self.prime_row)
        print("\n=======================\n" + "Pone row matrix:\n" + "=======================\n" )
        print(self.inversion_order)
        for i in range(12):
            print(self.row_order[i] + str(self.matrix[i]) + self.retrograde_order[i])

class combinatoriality():
    
    @classmethod
    def find_hexachordal_combinatorials(cls, tone_row: list, find_all = True, rows=False, retrogrades=False, inversions=False, inv_retrogrades=False):
        """
        Returns a list of transformations that that share combinatorial hexachords with the primary row.
        i.e The first 6 notes of every returned transformation are the same as 
        the first 6 notes of the prime row, regardless of order.
        
        If include_tone_row is set to True, the function will return a list of 
        the transformation of the tone row that shares hexachordal combinatoriality, 
        followed by 
        
        If any specific transformations (rows, retrogrades, etc.) are declared as True
        when the function is invoked
        the function will search for them only.
        
        Returns an empty list if no hexachordal combinatorials exist.
        """
        if rows or retrogrades or inversions or inv_retrogrades:
            find_all == False
        if find_all:
            rows = True
            retrogrades = True
            inversions = True
            inv_retrogrades = True
        reference_hexachord = tone_row[:6]
        reference_hexachord.sort()
        hexachords = []
        if rows == False and retrogrades == False and inversions == False and inv_retrogrades == False:
                return None
        
        matrix = twelve_tone_matrix()
        matrix.prime_row = tone_row
        for i in range(12):
            #iterates through rows of matrix
            if i != 0 and rows:
                trans_row_hexachord = matrix.matrix[i][:6]
                trans_row_hexachord.sort()
                if trans_row_hexachord == reference_hexachord:
                    hexachords.append(matrix.row_order[i])
            if retrogrades:
                trans_row_hexachord = matrix.matrix[i][6:]
                trans_row_hexachord.sort()
                if trans_row_hexachord == reference_hexachord:
                    hexachords.append(matrix.retrograde_order[i])
            
            #iterates through columns of matrix
            if inversions:
                trans_row_hexachord = [matrix.matrix[x][i] for x in range(6)]
                trans_row_hexachord.sort()
                if trans_row_hexachord == reference_hexachord:
                    hexachords.append(matrix.inversion_order[i])
            if inv_retrogrades:
                trans_row_hexachord = [matrix.matrix[x][i] for x in range(6,12)]
                trans_row_hexachord.sort()
                if trans_row_hexachord == reference_hexachord:
                    hexachords.append(matrix.retrograde_inversion_order[i])

        return hexachords

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
            for count, note_number in enumerate(note_number_list):
                note_number_list[count] = dictionary[note_number]
            return
        
        if isinstance(note_number_list[0], list) and isinstance(note_number_list[0][0], int):
            for tone_row in note_number_list:
                for count, note_number in enumerate(tone_row):
                    tone_row[count] = dictionary[note_number]

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
            print(f"Starting note {starting_note[0]} should be written in uppercase")
        if final_note[0].isupper == False:
            print(f"Final note {final_note[0]} should be written in uppercase")
        if direction not in {"up", "down"}:
            print("Invalid direction indicator, direction can either be 'up' or 'down'")
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
            print(f"Starting note {starting_note[0]} should be written in uppercase")
        if final_note[0].isupper == False:
            print(f"Final note {final_note[0]} should be written in uppercase")
        if direction not in {"up", "down"}:
            print("Invalid direction indicator, direction should be 'up' or 'down'")
        
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

class music_xml_writer():
    
    @classmethod
    def write_twelvetone_report(cls, prime_row: list, file_name: str, directory = None, score_title = None, include_combinatoriality = True):
        """
        Creates a .musicxml file with parts in the following order:\n
        -P0\n
        -R0\n
        -I0\n
        -RI0\n
        (if include_combinatoriality = True)\n
        -hexachordal combinatorials, if they exist\n
        -tetrachordal combinatorials, if they exist\n
        -trichordal combinatorials, if they exist\n
        
        
        Every part's tone row is written in quarter notes between the top and bottom line of
        the treble clef (between F4 and E5). All notes are written as naturals or sharps(excluding 'E#' and B#').
        
        If directory is not specified, file will be written in 'xml_files' subfolder in the project file.
        """
        file_path = cls.create_file_path(directory, file_name)
        if file_path is None:
            return
        if score_title is None:
            score_title = "Analysis of a Twelve-tone Row"
        part_names = ["P0", "R0", "I0", "RI0"]
        full_score = music21.stream.Score()
        measure = music21.stream.Measure()
        measure.timeSignature = music21.meter.TimeSignature('12/4')
        measure.timeSignature.style.hideObjectOnPrint = True
        prime_row_part = music21.stream.Part()
        prime_row_part.partName = "P0"
        pr_part_notes = copy.deepcopy(prime_row)
        note_names.convert_numbers_to_note_names(pr_part_notes, note_names.number_to_sharp_treble_clef_positions)
        part_notes = tone_row.prime_transformations_list(prime_row)
        for pitch in pr_part_notes:
            note = music21.note.Note(pitch)
            note.stemDirection = "noStem"
            measure.append(note)
        prime_row_part.append(measure)
        
        full_score.append(prime_row_part)
        full_score.insert(0, music21.metadata.Metadata(title = score_title, composer = ""))
        full_score.write("musicxml", f"./xml_files/{file_name}")
        note_names.convert_numbers_to_note_names(part_notes, note_names.number_to_sharp_treble_clef_positions)
        print("\n=========================\nFile successfully created\n=========================")
    
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
                print(f"File creation stopped. Specified directory('{directory}')\n does not exist")
                return 
        if directory is None:
            directory = os.path.normpath("/xml_files/")
        file_name = os.path.normpath(f"{file_name}")
        return os.path.join(directory, file_name)
    
if __name__ == "__main__":
    row = twelve_tone_matrix()
    row.assign_random_row()
    row.prime_row = list(range(12))
    #row.display_matrix()
    music_xml_writer.write_twelvetone_report(row.prime_row, "test_file")
    for i in []:
        print(note_names.note_to_number_relations[i])
