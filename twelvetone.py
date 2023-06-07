import copy
import numpy as np
import music21
import os
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

class combinatoriality():
    
    @classmethod
    def find_hexachordal_combinatorials(cls, prime_row: np.ndarray, find_all = True, rows=False, retrogrades=False, inversions=False, inv_retrogrades=False) -> list:
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
                trans_row_hexachord = np.array(tt_matrix[i][:6])
                trans_row_hexachord.sort()
                if np.array_equal(trans_row_hexachord, reference_hexachord):
                    hexachords.append(twelve_tone_matrix.row_order(prime_row)[i])
            if retrogrades:
                trans_row_hexachord = np.array(tt_matrix[i][6:])
                trans_row_hexachord.sort()
                if np.array_equal(trans_row_hexachord, reference_hexachord):
                    hexachords.append(twelve_tone_matrix.retrograde_order(prime_row)[i])
            
            #iterates through columns of matrix
            if inversions:
                trans_row_hexachord = np.array([tt_matrix[x][i] for x in range(6)])
                trans_row_hexachord.sort()
                if np.array_equal(trans_row_hexachord, reference_hexachord):
                    hexachords.append(twelve_tone_matrix.inversion_order(prime_row)[i])
            if inv_retrogrades:
                trans_row_hexachord = np.array([tt_matrix[x][i] for x in range(6,12)])
                trans_row_hexachord.sort()
                if np.array_equal(trans_row_hexachord, reference_hexachord):
                    hexachords.append(twelve_tone_matrix.retrograde_inversion_order(prime_row)[i])

        return hexachords
    
    @classmethod
    def find_tetrachordal_combinatorials(cls, prime_row: np.ndarray):
        """
        Returns a list of transformations that share tetrachordal combinatoriality
        with the prime row.\n
        
        SHORT EXPLANATION
        ==================
        
        """
        combinatorial_transformations = []
        first_tetrachord = np.array(prime_row[:4])
        first_tetrachord.sort()
        second_tetrachord = np.array(prime_row[4:8])
        second_tetrachord.sort()
        third_tetrachord = np.array(prime_row[8:])
        third_tetrachord.sort()
        
        #traversal of twelve-tone matrix
        tt_matrix = twelve_tone_matrix.generate_twelve_tone_matrix(prime_row)
        for i in range (12):
            compared_first_tetrachord = np.array(tt_matrix[i][:4])
            compared_first_tetrachord.sort()
            compared_second_tetrachord = np.array(tt_matrix[i][4:8])
            compared_second_tetrachord.sort()
            compared_third_tetrachord = np.array(tt_matrix[i][8:])
            compared_third_tetrachord.sort()
            
            #ITERATE THROUGH ROWS OF MATRIX
            #checks for row combinatoriality
            first_tetrachord_check = np.array_equal(first_tetrachord, compared_first_tetrachord)
            second_tetrachord_check = np.array_equal(second_tetrachord, compared_second_tetrachord)
            third_tetrachord_check = np.array_equal(third_tetrachord, compared_third_tetrachord)
            if i > 0 and first_tetrachord_check and second_tetrachord_check and third_tetrachord_check:
                combinatorial_transformations.append(twelve_tone_matrix.row_order(prime_row)[i])
            
            #checks for retrograde combinatoriality
            first_tetrachord_check = np.array_equal(first_tetrachord, compared_third_tetrachord)
            third_tetrachord_check = np.array_equal(third_tetrachord, compared_first_tetrachord)
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
            first_tetrachord_check = np.array_equal(first_tetrachord, compared_first_tetrachord)
            second_tetrachord_check = np.array_equal(second_tetrachord, compared_second_tetrachord)
            third_tetrachord_check = np.array_equal(third_tetrachord, compared_third_tetrachord)
            if first_tetrachord_check and second_tetrachord_check and third_tetrachord_check:
                combinatorial_transformations.append(twelve_tone_matrix.inversion_order(prime_row)[i])
            
            #checks for inversion combinatoriality
            first_tetrachord_check = np.array_equal(first_tetrachord, compared_third_tetrachord)
            third_tetrachord_check = np.array_equal(third_tetrachord, compared_first_tetrachord)
            if first_tetrachord_check and second_tetrachord_check and third_tetrachord_check:
                combinatorial_transformations.append(twelve_tone_matrix.retrograde_inversion_order(prime_row)[i])
                
        return combinatorial_transformations
    
    @classmethod
    def find_trichordal_combinatorials(cls, prime_row: np.ndarray):
        """
        Returns a list of transformations that share tetrachordal combinatoriality
        with the prime row.\n
        
        SHORT EXPLANATION
        ==================
        
        """
        combinatorial_transformations = []
        first_tetrachord = np.array(prime_row[:3])
        first_tetrachord.sort()
        second_tetrachord = np.array(prime_row[3:6])
        second_tetrachord.sort()
        third_tetrachord = np.array(prime_row[6:9])
        third_tetrachord.sort()
        fourth_tetrachord = np.array(prime_row[9:])
        fourth_tetrachord.sort()
        
        #traversal of twelve-tone matrix
        tt_matrix = twelve_tone_matrix.generate_twelve_tone_matrix(prime_row)
        for i in range (12):
            compared_first_tetrachord = np.array(tt_matrix[i][:3])
            compared_first_tetrachord.sort()
            compared_second_tetrachord = np.array(tt_matrix[i][3:6])
            compared_second_tetrachord.sort()
            compared_third_tetrachord = np.array(tt_matrix[i][6:9])
            compared_third_tetrachord.sort()
            compared_fourth_tetrachord = np.array(tt_matrix[i][9:])
            compared_fourth_tetrachord.sort()
            
            #ITERATE THROUGH ROWS OF MATRIX
            #checks for row combinatoriality
            first_tetrachord_check = np.array_equal(first_tetrachord, compared_first_tetrachord)
            second_tetrachord_check = np.array_equal(second_tetrachord, compared_second_tetrachord)
            third_tetrachord_check = np.array_equal(third_tetrachord, compared_third_tetrachord)
            fourth_tetrachord_check = np.array_equal(fourth_tetrachord, compared_fourth_tetrachord)
            if i > 0 and first_tetrachord_check and second_tetrachord_check and third_tetrachord_check and fourth_tetrachord_check:
                combinatorial_transformations.append(twelve_tone_matrix.row_order(prime_row)[i])
            
            #checks for retrograde combinatoriality
            first_tetrachord_check = np.array_equal(first_tetrachord, compared_fourth_tetrachord)
            second_tetrachord_check = np.array_equal(second_tetrachord, compared_third_tetrachord)
            third_tetrachord_check = np.array_equal(third_tetrachord, compared_second_tetrachord)
            fourth_tetrachord_check = np.array_equal(fourth_tetrachord, compared_first_tetrachord)
            if i > 0 and first_tetrachord_check and second_tetrachord_check and third_tetrachord_check and fourth_tetrachord_check:
                combinatorial_transformations.append(twelve_tone_matrix.retrograde_order(prime_row)[i])
            
            #ITERATE THROUGH COLUMNS OF MATRIX
            matrix_column = np.array([tt_matrix[x][i] for x in range(12)])
            compared_first_tetrachord = np.array(matrix_column[:3])
            compared_first_tetrachord.sort()
            compared_second_tetrachord = np.array(matrix_column[3:6])
            compared_second_tetrachord.sort()
            compared_third_tetrachord = np.array(matrix_column[6:9])
            compared_third_tetrachord.sort()
            compared_fourth_tetrachord = np.array(matrix_column[9:])
            compared_fourth_tetrachord.sort()
            
            #checks for inversion combinatoriality
            first_tetrachord_check = np.array_equal(first_tetrachord, compared_first_tetrachord)
            second_tetrachord_check = np.array_equal(second_tetrachord, compared_second_tetrachord)
            third_tetrachord_check = np.array_equal(third_tetrachord, compared_third_tetrachord)
            fourth_tetrachord_check = np.array_equal(fourth_tetrachord, compared_fourth_tetrachord)
            if first_tetrachord_check and second_tetrachord_check and third_tetrachord_check and fourth_tetrachord_check:
                combinatorial_transformations.append(twelve_tone_matrix.inversion_order(prime_row)[i])
            
            #checks for inversion combinatoriality
            first_tetrachord_check = np.array_equal(first_tetrachord, compared_fourth_tetrachord)
            second_tetrachord_check = np.array_equal(second_tetrachord, compared_third_tetrachord)
            third_tetrachord_check = np.array_equal(third_tetrachord, compared_second_tetrachord)
            fourth_tetrachord_check = np.array_equal(fourth_tetrachord, compared_first_tetrachord)
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

class music_xml_writer():
    
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
        
        combinatorial_trichords = combinatoriality.find_trichordal_combinatorials(prime_row)
        for transformations in combinatorial_trichords:
            part = cls.create_trichord_combinatorial_part(transformations, prime_row)
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
    def create_trichord_combinatorial_part(cls, transformation_name: str, prime_row: list):
        """
        Returns a music21 part object.
        Part consists of twelve stemless quarter notes with a hidden 12/4
        time signature.
        
        Dotted ties are added over each half of the tone row.
        Text is added above the part which indicates that it is a hexachordal combinatorial.
        """
        measure = cls.create_stemless_measure(transformation_name, prime_row)
        comment = music21.expressions.TextExpression("(trichordal combinatorial)")
        measure.insert(0, comment)
        first_slur = music21.spanner.Slur([measure.notes[0],  measure.notes[2]])
        measure.insert(0.0, first_slur)
        second_slur = music21.spanner.Slur([measure.notes[3],  measure.notes[5]])
        measure.insert(0.0, second_slur)
        third_slur = music21.spanner.Slur([measure.notes[6],  measure.notes[8]])
        measure.insert(0.0, third_slur)
        fourth_slur = music21.spanner.Slur([measure.notes[9],  measure.notes[11]])
        measure.insert(0.0, fourth_slur)
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
    pass
