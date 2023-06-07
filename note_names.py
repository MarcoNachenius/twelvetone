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