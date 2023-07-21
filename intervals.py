from note_names import note_names
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