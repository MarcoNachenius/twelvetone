"""
In Western music, the octave is divided into twelve equal parts that correspond to specific notes.
This means that there are a total of 12 unique notes. 

This program will use numerical values instead of note names to make the numerical logic clearer
to a person who may not be familiar with how the relationship between pitch and note-names work in Western music.
The reader only needs to understand how this principle works on a numerical level.

Notes are ordered incrementally,
i.e. [0,1,2,3,4,5,6,7,8,9,10,11] = [C,C#,D,D#,E,F,Gb,G,G#,A,Bb,B]   <---C is arbitrarily used as note 0

The distance between two notes is measured in semitones. For example:
note 5 can be two semitones higher than note 3 or four semitones lower than note 9.

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
from top-left to bottom-right ([1][1], [2][2], [3][3] etc.) will always be
identical, regardless of which tone-row is used.
"""

import random
import copy

class tone_row (object): #I wanted to use numpy arrays but my versions are mixed up and it wouldn't run
    
    def __init__(self, **args):
        self.__primary_row = []
    
    @property
    def primary_row_inversion(self):
        row_inversion = [self.primary_row[0]]
        for i in range(1,12):
            semitones = self.primary_row[i] - self.primary_row[i-1]
            row_inversion.append(row_inversion[i-1] - semitones)
            
            if row_inversion[i] > 11:
                row_inversion[i] -= 12
            elif row_inversion[i] < 0:
                row_inversion[i] += 12
        
        return row_inversion
    
    @property
    def primary_row(self):
        return self.__primary_row
    
    @primary_row.setter
    def primary_row(self, tone_row: list):
        self.__primary_row = tone_row
    
    @property
    def random_tone_row(self):
        random_tone_row = list(range(12))
        random.shuffle(random_tone_row)
        return random_tone_row

class twelve_tone_matrix(tone_row):
    
    def __init__(self, **args):
        tone_row.__init__(self)
        
    @property
    def matrix(self):
        
        #adds first row and column of 12-tone matrix
        matrix = [self.primary_row]
        matrix.extend(
            copy.deepcopy([self.primary_row_inversion[i]]) for i in range(1, 12)
        )
        
        #completes matrix by calculating the distance between the first note of the prime row
        #and the first note of every other row, and transposing the prime row by that distance
        for matrix_row in range(1,12):
            semitones = matrix[matrix_row][0] - matrix[0][0]
            for matrix_column in range(1,12):
                matrix[matrix_row].append(matrix[0][matrix_column] + semitones)
                if matrix[matrix_row][matrix_column] > 11:
                    matrix[matrix_row][matrix_column] -= 12
                elif matrix[matrix_row][matrix_column] < 0:
                    matrix[matrix_row][matrix_column] += 12

        return matrix

if __name__ == "__main__":
    row = twelve_tone_matrix()
    row.primary_row = row.random_tone_row
    row.primary_row = [2, 5, 1, 6, 7, 9, 4, 11, 10, 3, 8, 0]
    print(row.primary_row)
    print(row.primary_row_inversion)
    for i in row.matrix:
        print(i)
    print(row.matrix)