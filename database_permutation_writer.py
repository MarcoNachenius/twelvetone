import math
import numpy as np
import sqlite3
from dataclasses import dataclass
from tone_row import tone_row
from combinatoriality import combinatoriality
"""
This library provides an algorithm for producing every possible unique permutation of a tone row.

The method for producing every possible permutation of a tone row of a specific length is
derived from basic probability theory.


Starting values:
====================
Index number: 0   Remaining notes: [A, B, C, D]  Final set: []
Index number: 1   Remaining notes: [A, B, C, D]  Final set: []
Index number: 2   Remaining notes: [A, B, C, D]  Final set: []
Index number: 3   Remaining notes: [A, B, C, D]  Final set: []
Index number: 4   Remaining notes: [A, B, C, D]  Final set: []
Index number: 5   Remaining notes: [A, B, C, D]  Final set: []
Index number: 6   Remaining notes: [A, B, C, D]  Final set: []
Index number: 7   Remaining notes: [A, B, C, D]  Final set: []
Index number: 8   Remaining notes: [A, B, C, D]  Final set: []
Index number: 9   Remaining notes: [A, B, C, D]  Final set: []
Index number: 10  Remaining notes: [A, B, C, D]  Final set: []
Index number: 11  Remaining notes: [A, B, C, D]  Final set: []
Index number: 12  Remaining notes: [A, B, C, D]  Final set: []
Index number: 13  Remaining notes: [A, B, C, D]  Final set: []
Index number: 14  Remaining notes: [A, B, C, D]  Final set: []
Index number: 15  Remaining notes: [A, B, C, D]  Final set: []
Index number: 16  Remaining notes: [A, B, C, D]  Final set: []
Index number: 17  Remaining notes: [A, B, C, D]  Final set: []
Index number: 18  Remaining notes: [A, B, C, D]  Final set: []
Index number: 19  Remaining notes: [A, B, C, D]  Final set: []
Index number: 20  Remaining notes: [A, B, C, D]  Final set: []
Index number: 21  Remaining notes: [A, B, C, D]  Final set: []
Index number: 22  Remaining notes: [A, B, C, D]  Final set: []
Index number: 23  Remaining notes: [A, B, C, D]  Final set: []

Extract first notes:
====================
Index number: 0   Remaining notes: [B, C, D] Final set: [A]
Index number: 1   Remaining notes: [B, C, D] Final set: [A]
Index number: 2   Remaining notes: [B, C, D] Final set: [A]
Index number: 3   Remaining notes: [B, C, D] Final set: [A]
Index number: 4   Remaining notes: [B, C, D] Final set: [A]
Index number: 5   Remaining notes: [B, C, D] Final set: [A]
Index number: 6   Remaining notes: [A, C, D] Final set: [B]
Index number: 7   Remaining notes: [A, C, D] Final set: [B]
Index number: 8   Remaining notes: [A, C, D] Final set: [B]
Index number: 9   Remaining notes: [A, C, D] Final set: [B]
Index number: 10  Remaining notes: [A, C, D] Final set: [B]
Index number: 11  Remaining notes: [A, C, D] Final set: [B]
Index number: 12  Remaining notes: [A, B, D] Final set: [C]
Index number: 13  Remaining notes: [A, B, D] Final set: [C]
Index number: 14  Remaining notes: [A, B, D] Final set: [C]
Index number: 15  Remaining notes: [A, B, D] Final set: [C]
Index number: 16  Remaining notes: [A, B, D] Final set: [C]
Index number: 17  Remaining notes: [A, B, D] Final set: [C]
Index number: 18  Remaining notes: [A, B, C] Final set: [D]
Index number: 19  Remaining notes: [A, B, C] Final set: [D]
Index number: 20  Remaining notes: [A, B, C] Final set: [D]
Index number: 21  Remaining notes: [A, B, C] Final set: [D]
Index number: 22  Remaining notes: [A, B, C] Final set: [D]
Index number: 23  Remaining notes: [A, B, C] Final set: [D]

Extract second notes:
====================
Index number: 0   Remaining notes: [C, D]    Final set: [A, B]
Index number: 1   Remaining notes: [B, D]    Final set: [A, C]
Index number: 2   Remaining notes: [C, D]    Final set: [A, B]
Index number: 3   Remaining notes: [B, C]    Final set: [A, D]
Index number: 4   Remaining notes: [B, D]    Final set: [A, C]
Index number: 5   Remaining notes: [C, D]    Final set: [B, A]
Index number: 6   Remaining notes: [B, C]    Final set: [A, D]
Index number: 7   Remaining notes: [A, D]    Final set: [B, C]
Index number: 8   Remaining notes: [C, D]    Final set: [B, A]
Index number: 9   Remaining notes: [A, C]    Final set: [B, D]
Index number: 10  Remaining notes: [A, D]    Final set: [B, C]
Index number: 11  Remaining notes: [B, D]    Final set: [C, A]
Index number: 12  Remaining notes: [A, C]    Final set: [B, D]
Index number: 13  Remaining notes: [A, D]    Final set: [C, B]
Index number: 14  Remaining notes: [B, D]    Final set: [C, A]
Index number: 15  Remaining notes: [A, B]    Final set: [C, D]
Index number: 16  Remaining notes: [A, D]    Final set: [C, B]
Index number: 17  Remaining notes: [B, C]    Final set: [D, A]
Index number: 18  Remaining notes: [A, B]    Final set: [C, D]
Index number: 19  Remaining notes: [A, C]    Final set: [D, B]
Index number: 20  Remaining notes: [B, C]    Final set: [D, A]
Index number: 21  Remaining notes: [A, B]    Final set: [D, C]
Index number: 22  Remaining notes: [A, C]    Final set: [D, B]
Index number: 23  Remaining notes: [A, B]    Final set: [D, C]

Extract third notes:
====================
Index number: 0   Remaining notes: [D]   Final set: [A, B, C]
Index number: 1   Remaining notes: [C]   Final set: [A, B, D]
Index number: 2   Remaining notes: [D]   Final set: [A, C, B]
Index number: 3   Remaining notes: [B]   Final set: [A, C, D]
Index number: 4   Remaining notes: [C]   Final set: [A, D, B]
Index number: 5   Remaining notes: [B]   Final set: [A, D, C]
Index number: 6   Remaining notes: [D]   Final set: [B, A, C]
Index number: 7   Remaining notes: [C]   Final set: [B, A, D]
Index number: 8   Remaining notes: [D]   Final set: [B, C, A]
Index number: 9   Remaining notes: [A]   Final set: [B, C, D]
Index number: 10  Remaining notes: [C]   Final set: [B, D, A]
Index number: 11  Remaining notes: [A]   Final set: [B, D, C]
Index number: 12  Remaining notes: [D]   Final set: [C, A, B]
Index number: 13  Remaining notes: [B]   Final set: [C, A, D]
Index number: 14  Remaining notes: [D]   Final set: [C, B, A]
Index number: 15  Remaining notes: [A]   Final set: [C, B, D]
Index number: 16  Remaining notes: [B]   Final set: [C, D, A]
Index number: 17  Remaining notes: [A]   Final set: [C, D, B]
Index number: 18  Remaining notes: [C]   Final set: [D, A, B]
Index number: 19  Remaining notes: [B]   Final set: [D, A, C]
Index number: 20  Remaining notes: [C]   Final set: [D, B, A]
Index number: 21  Remaining notes: [A]   Final set: [D, B, C]
Index number: 22  Remaining notes: [B]   Final set: [D, C, A]
Index number: 23  Remaining notes: [A]   Final set: [D, C, B]

Extract fourth notes:
====================
Index number: 0   Remaining notes: []    Final set: [A, B, C, D]
Index number: 1   Remaining notes: []    Final set: [A, B, D, C]
Index number: 2   Remaining notes: []    Final set: [A, C, B, D]
Index number: 3   Remaining notes: []    Final set: [A, C, D, B]
Index number: 4   Remaining notes: []    Final set: [A, D, B, C]
Index number: 5   Remaining notes: []    Final set: [A, D, C, B]
Index number: 6   Remaining notes: []    Final set: [B, A, C, D]
Index number: 7   Remaining notes: []    Final set: [B, A, D, C]
Index number: 8   Remaining notes: []    Final set: [B, C, A, D]
Index number: 9   Remaining notes: []    Final set: [B, C, D, A]
Index number: 10  Remaining notes: []    Final set: [B, D, A, C]
Index number: 11  Remaining notes: []    Final set: [B, D, C, A]
Index number: 12  Remaining notes: []    Final set: [C, A, B, D]
Index number: 13  Remaining notes: []    Final set: [C, A, D, B]
Index number: 14  Remaining notes: []    Final set: [C, B, A, D]
Index number: 15  Remaining notes: []    Final set: [C, B, D, A]
Index number: 16  Remaining notes: []    Final set: [C, D, A, B]
Index number: 17  Remaining notes: []    Final set: [C, D, B, A]
Index number: 18  Remaining notes: []    Final set: [D, A, B, C]
Index number: 19  Remaining notes: []    Final set: [D, A, C, B]
Index number: 20  Remaining notes: []    Final set: [D, B, A, C]
Index number: 21  Remaining notes: []    Final set: [D, B, C, A]
Index number: 22  Remaining notes: []    Final set: [D, C, A, B]
Index number: 23  Remaining notes: []    Final set: [D, C, B, A]

"""
class permutation_calculator():
    
    @classmethod
    def find_permutation(cls, row_number: int, row_length = 11) -> np.ndarray:
        """
        Returns the tone row that would be located at a
        specific row number within a database containing
        every possible permutation of a tone row.
        """
        all_options = np.arange(row_length)
        tone_row = np.zeros(row_length, dtype= int)
        if row_number < 0 or row_number > math.factorial(row_length):
            raise ValueError(f"Invalid index number({row_number})\n row_number must be a number between 0 and {math.factorial(row_length) - 1}")
        
        #calculate first element of tone row
        index_number = math.floor(row_number/math.factorial(row_length-1))
        tone_row[0] = all_options[index_number]
        
        for i in range(1, row_length):
            #Get remaining options
            #Create a Boolean mask of elements in all_options that are present in tone_row so far
            mask = np.isin(all_options, tone_row[:i])
            #Filter all_options using the mask to remove the values
            remaining_options = all_options[~mask]
            
            rem_index_num = row_number % math.factorial(len(remaining_options))
            index_number = math.floor(rem_index_num/math.factorial(len(remaining_options)-1))
            tone_row[i] = remaining_options[index_number]
        
        return tone_row
    
    
@dataclass
class all_value_entry:
    row_id: int = None
    #prime transformations
    P0: np.ndarray = None
    R0: np.ndarray = None
    I0: np.ndarray = None
    RI0: np.ndarray = None
    #interval sizes of prime transformations 
    P0_intervals: np.ndarray = None
    R0_intervals: np.ndarray = None
    I0_intervals: np.ndarray = None
    RI0_intervals: np.ndarray = None
    #combinatorials
    combinatorial_hexachords: list = None
    combinatorial_tetrachords: list = None
    combinatorial_trichords: list = None
    
class create_database_entry():
    
    @classmethod
    def all_values_entry(cls, row_number: int) -> all_value_entry:
        entry = all_value_entry()
        entry.row_id = row_number
        #prime transformations
        entry.P0 = np.append(np.zeros(1, dtype=int), permutation_calculator.find_permutation(row_number) + 1)
        entry.R0 = tone_row.prime_retrograde(entry.P0)
        entry.I0 = tone_row.prime_inversion(entry.P0)
        entry.RI0 = tone_row.prime_retrograde_inversion(entry.P0)
        #interval sizes of prime transformations 
        entry.P0_intervals = tone_row.row_interval_sizes(entry.P0)
        entry.R0_intervals = tone_row.row_interval_sizes(entry.R0)
        entry.I0_intervals = tone_row.row_interval_sizes(entry.I0)
        entry.RI0_intervals = tone_row.row_interval_sizes(entry.RI0)
        #combinatorials
        entry.combinatorial_hexachords = tuple(combinatoriality.find_hexachordal_combinatorials(entry.P0))
        entry.combinatorial_tetrachords = tuple(combinatoriality.find_tetrachordal_combinatorials(entry.P0))
        entry.combinatorial_trichords = tuple(combinatoriality.find_trichordal_combinatorials(entry.P0))
        
        return entry
        
        





