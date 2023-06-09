This library is designed for the creation, analysis and graphic representation of 12-tone music.

The most developed part of this code at the moment is its ability to create an analytic score(.musicxml file) based on a tone row provided by the user. The score contains all of the row's prime transformations(R0, I0, RI0), as well as all of the transformations that are combinatorials(hexachordal, tetrachordal and trichordal) of the prime row. 

SHORT INTRODUCTION
====================
In Western music, the octave is divided into twelve equal parts that correspond to specific notes.
This means that there are a total of 12 unique notes. 

This program primarily uses numerical values instead of note names. This should make the program somewhat more accessible to a user who may not be familiar with how the relationship between pitch and note-names work in Western music.

The reader only needs to understand how this note ordering works on a numerical level.
Notes are ordered incrementally:
i.e. [0,1,2,3,4,5,6,7,8,9,10,11] = [C,C#,D,D#,E,F,Gb,G,G#,A,Bb,B]  
    ('C' was chosen as note 0 in order to conform to MIDI pitch numbering)

This series of notes repeats itself once the end of the index is reached. i.e. 
...0,1,2,3,4,5,6,7,8,9,10,11,0,1,2,3,4,5,6,7,8,9,10,11,0,1,2,3,4,5,6,7,8,9,10,11...

The distance between two notes is measured in semitones. For example,
note 5 is two semitones higher than note 3 or four semitones lower than note 9.
Furthermore, note 1 can be understood to be two semitones above 11
and three semitones below 10. 

It is not important for the reader to know why or how this concept is implemented in music.
It is only important to understand that one note may reach another by moving up or down a 
certain number of steps in the aforementioned repeating series. 

In the 1920's Arnold Schoenberg invented a form of composition named 12-tone serialism.
This form of composition has one fundamental principle:
if a specific note is used, all other 11 notes must be used before it may be used again.
This gave rise to the use of a tone-row. A tone-row is a pre-selected permutation of 12 unique notes. 

TONE ROW TRANSFORMATIONS
=========================

TRANSPOSITION

If every note of a tone row (or its inversion) is uniformly moved up or down by the same number of semitones,
it is referred to as a transposition.

Schoenberg found that a different, yet invariably related tone-row consisting of 12 unique notes that
can be generated from the primary tone-row by means of inversion. 
Creating a tone-row by inversion is achieved by reversing distance of traversal between every note of a tone row. 


For example, if we take the tone-row [2,5,1,6,7,9,4,11,10,3,8,0] the distances between notes may be expressed as follows:

2 (+3)

5 (-4)

1 (+5)

6 (+1)

7 (+2)

9 (-5)

4 (-5)

11 (-1)

10 (+5)

3 (+5)

8 (+4)

0


By reversing the traversal of distance between every note, the inversion is generated as follows:

2 (-3)

11 (+4)

3 (-5)

10 (-1)

9 (-2)

7 (+5)

0 (+5)

5 (+1) 

6 (-5)

1 (-5)

8 (-4)

4

TWELVE-TONE MATRIX
===================
Schoenberg devised the 12-tone matrix as a way of representing every
possible transformation of a tone tone row. A 12-tone matrix is a 12*12 two-dimensional array. The first row of the array(read from
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

TRANSFORMATION NAMES
======================

'P' refers to a specific transposition of the prime row.

'P0' is the prime row


'I' refers to a specific inversion of the prime row.

'I0' is the prime inversion


'R' refers to a specific retrograde(reverse order) of the prime row.

'R0' is the prime retrograde


'RI' refers to a specific retrograde of the prime row's inversion.

'RI0' is the prime retrograde inversion


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


P0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

T7 = [7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5, 6]

I0 = [0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

I6 = [6, 5, 4, 3, 2, 1, 0, 11, 10, 9, 8, 7]

R11 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

R0 = [0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

RI1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]

RI6 = [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5]
