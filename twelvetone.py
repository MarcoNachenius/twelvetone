"""
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
possible transposition. A 12-tone matrix is a two-dimensional array. The first row of the array(read from
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
        Assigns a random 12-tone row as the primary row(T0).
        """
        random_tone_row = list(range(12))
        random.shuffle(random_tone_row)
        self.prime_row = random_tone_row

    @property
    def pr_retrograde(self):
        """
        Returns R0
        """
        pr_retrograde = copy.deepcopy(self.prime_row)
        pr_retrograde.reverse()
        pr_retrograde = self.transpose_row(pr_retrograde, self.prime_row[0] - pr_retrograde[0])
        return pr_retrograde

    @property
    def pr_inversion(self):
        """
        Returns I0
        """
        row_inversion = [self.prime_row[0]]
        
        for i in range(1,12):
            semitones = self.prime_row[i] - self.prime_row[i-1]
            row_inversion.append(row_inversion[i-1] - semitones)
            if row_inversion[i] > 11:
                row_inversion[i] -= 12
                continue
            if row_inversion[i] < 0:
                row_inversion[i] += 12
        
        return row_inversion
    
    @property
    def pr_retrograde_inversion(self):
        """
        Returns RI0
        """
        pr_ret_inv = copy.deepcopy(self.pr_inversion)
        pr_ret_inv.reverse()
        pr_ret_inv = self.transpose_row(pr_ret_inv, self.prime_row[0] -pr_ret_inv[0])
        return pr_ret_inv
    
    def transpose_row(self, tone_row: list, semitones: int):
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
    
    def return_transformation(self, transposition: str):
        """
        Transposition of a tone row occurs when all notes are moved up or
        down by the same amount of semitones.
        
        'P' refers to a specific transposition of the prime row.
        'P0' is the prime row(first row of the matrix)
        
        'I' refers to a specific inversion of the prime row.
        'I0' is the prime row(first row of the matrix)
        
        'R' refers to a specific retrograde(reverse order) of the prime row.
        'R0' is the retrograde of the prime row(prime row in reverse order)
        
        'RI' refers to a specific retrograde of the prime row's inversion.
        'RI0' is the retrograde of the prime row's inversion(first column of the matrix read from down to up)
        
        For example, consider the matrix of the tone row [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        [11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        [10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        [9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8]
        [8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7]
        [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6]
        [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5]
        [5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4]
        [4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3]
        [3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2]
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1]
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]
        
        Here are some examples of how specific transpositions are written
        and what their values are:
        
        T0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        T7 = [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6]
        I0 = [0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        I6 = [6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7]
        R0 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        R1 = [0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        RI0 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]
        RI5 = [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5]
        """
        if transposition.startswith("P"):
            return self.transpose_row(self.prime_row, int(transposition[1:]))

        if transposition.startswith("RI"):
            return self.transpose_row(self.pr_retrograde_inversion, int(transposition[2:]))
        
        if transposition.startswith("R"):
            return self.transpose_row(self.pr_retrograde, int(transposition[1:]))
        
        if transposition.startswith("I"):
            return self.transpose_row(self.pr_inversion, int(transposition[1:]))
    
    def find_transformations(self, tone_row: list, find_all = False, row = False, inversion = False,  row_retrograde = False, inv_retrograde = False):
        """
        Returns a list of transformations that apply to the primary row
        """
        if find_all:
            row = True
            inversion = True 
            row_retrograde = True
            inv_retrograde = True
        transformations = []
        for i in range(12):
            if row and tone_row == self.transpose_row(self.prime_row, i):
                transformations.append(f"P{str(i)}")
            
            if row_retrograde and tone_row == self.transpose_row(
                self.pr_retrograde, i):
                transformations.append(f"R{str(i)}")
            
            if inversion and tone_row == self.transpose_row(
                self.pr_inversion, i):
                transformations.append(f"I{str(i)}")
            
            if inv_retrograde and tone_row == self.transpose_row(
                self.pr_retrograde_inversion, i):
                transformations.append(f"RI{str(i)}")

        return transformations
    

class twelve_tone_matrix(tone_row):
    
    def __init__(self, *args, **kwargs):
        tone_row.__init__(self)
    
    @property
    def matrix(self):
        """
        Returns a two-dimensional 12*12 array
        T0 is always the first row([0:0] -> [0:12]) and
        I0 is always the first column ([0:0] -> [12:0])
        """
        
        #adds first row and column of 12-tone matrix
        matrix = [self.prime_row]
        matrix.extend(
            copy.deepcopy([self.pr_inversion[i]]) for i in range(1, 12))
        
        #completes matrix by calculating the distance between the first note of the prime row
        #and the first note of every other row, and transposing the prime row by that distance
        for matrix_row in range(1,12):
            semitones = matrix[matrix_row][0] - matrix[0][0]
            for matrix_column in range(1,12):
                matrix[matrix_row].append(matrix[0][matrix_column] + semitones)
                if matrix[matrix_row][matrix_column] > 11:
                    matrix[matrix_row][matrix_column] -= 12
                    continue
                if matrix[matrix_row][matrix_column] < 0:
                    matrix[matrix_row][matrix_column] += 12
        return matrix
    
    @property
    def row_order(self):
        row_order = ["P0"]
        reference_note = self.prime_row[0]
        for i in range(1, 12):
            semitones_up = self.pr_inversion[i] - reference_note
            if semitones_up < 0:
                semitones_up += 12
            row_order.append(f"P{str(semitones_up)}")
        return row_order
    
    @property
    def retrograde_order(self):
        """
        The last column of the 12-tone matrix represents the first note of every retrograde
        """
        row_order = []
        ret_row = [i[11] for i in self.matrix]
        reference_note = self.prime_row[0]
        for i in range(12):
            semitones_up = ret_row[i] - reference_note
            if semitones_up < 0:
                semitones_up += 12
            row_order.append(f"R{str(semitones_up)}")
        return row_order
    
    @property
    def inversion_order(self):
        row_order = ["I0"]
        reference_note = self.prime_row[0]
        for i in range(1, 12):
            semitones_up = self.prime_row[i] - reference_note
            if semitones_up < 0:
                semitones_up += 12
            row_order.append(f"I{str(semitones_up)}")
        return row_order
    
    @property
    def ret_inv_order(self):
        """
        The last row of the 12-tone matrix represents the first note of every retrograde inversion
        """
        row_order = []
        ret_inv_row = self.matrix[11]
        reference_note = self.prime_row[0]
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
        print("\t" + str(self.inversion_order))
        for i in self.matrix:
            print(i)
    
    def find_hexachordal_combinatorials(self, find_all = True, rows=False, retrogrades=False, inversions=False, inv_retrogrades=False):
        """
        Returns a list of transformations that that share combinatorial hexachords with the primary row.
        i.e The first 6 notes of every returned transformation are the same as 
        the first 6 notes of the prime row, regardless of order.
        
        If any specific transformations (rows, retrogrades, etc.) are declared as True,
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
        reference_hexachord = self.prime_row[:6]
        reference_hexachord.sort()
        hexachords = []
        if rows == False and retrogrades == False and inversions == False and inv_retrogrades == False:
                return None
            
        for i in range(12):
            #iterates through rows of matrix
            if i != 0 and rows:
                trans_row_hexachord = self.matrix[i][:6]
                trans_row_hexachord.sort()
                if trans_row_hexachord == reference_hexachord:
                    hexachords.append(self.row_order[i])
            if retrogrades:
                trans_row_hexachord = self.matrix[i][6:]
                trans_row_hexachord.sort()
                if trans_row_hexachord == reference_hexachord:
                    hexachords.append(self.retrograde_order[i])
            
            #iterates through columns of matrix
            if inversions:
                trans_row_hexachord = [self.matrix[x][i] for x in range(6)]
                trans_row_hexachord.sort()
                if trans_row_hexachord == reference_hexachord:
                    hexachords.append(self.inversion_order[i])
            if inv_retrogrades:
                trans_row_hexachord = [self.matrix[x][i] for x in range(6,12)]
                trans_row_hexachord.sort()
                if trans_row_hexachord == reference_hexachord:
                    hexachords.append(self.ret_inv_order[i])
        
        return hexachords

if __name__ == "__main__":
    row = twelve_tone_matrix()
    row.assign_random_row()
    #row.prime_row = list(range(12))
    row.display_matrix()
    trans_row = row.transpose_row(row.prime_row, 6)
    print(row.row_order)
    print(row.inversion_order)
    print(row.retrograde_order)
    print(row.ret_inv_order)
    hexachords = row.find_hexachordal_combinatorials()
    print(hexachords)