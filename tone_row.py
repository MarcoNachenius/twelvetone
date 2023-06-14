import numpy as np
from note_names import note_names

class tone_row (object): 
    
    def __init__(self, tone_row = None, *args, **kwargs):
        if tone_row is None:
            tone_row = np.arange(12)
        self.__prime_row = tone_row
    
    @property
    def prime_row(self):
        return self.__prime_row

    @prime_row.setter
    def prime_row(self, tone_row: np.ndarray):
        self.__prime_row = tone_row
    
    @classmethod
    def convert_notes_to_numbers(cls, first_note: str,
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
                                twelfth_note: str) -> np.ndarray:
        """
        Converts note names of tone row into a list of numerical values('C' = 0) that correspond to
        the project's numerical convention for note names( "C#"/"Db" = 1, "D" = 2, "D#"/"Eb" = 3 etc).
        \n
        Note names are to be entered in uppercase. 
        \n
        Accidental symbols:\n
        "#" = sharp\n
        "b" = flat\n
        "##" = double-sharp\n
        "bb" = double-flat\n
        """
        note_name_list = [first_note, second_note, third_note, fourth_note, fifth_note, sixth_note, seventh_note, eighth_note, ninth_note, tenth_note, eleventh_note, twelfth_note]
        note_numbers = np.zeros(12, dtype = int)
        for i, note in enumerate(note_name_list):
            note_numbers[i] = note_names.note_to_number_relations[note]
        return note_numbers
        

    @classmethod
    def generate_random_row(cls) -> np.ndarray:
        """
        Returns a random twelve-tone row
        """
        
        random_tone_row = np.arange(12)
        np.random.shuffle(random_tone_row)
        return random_tone_row
    
    @classmethod
    def prime_retrograde(cls, prime_row: np.ndarray) -> np.ndarray:
        """
        Returns R0
        
        R0 is the retrograde of a given tone row that starts on the same note as the prime row.
        """
        pr_retrograde = np.flip(prime_row)
        pr_retrograde = cls.transpose_row(pr_retrograde, prime_row[0] - pr_retrograde[0])
        return pr_retrograde

    
    @classmethod
    def prime_inversion(cls, prime_row: np.ndarray) -> np.ndarray:
        """
        Returns I0
        
        I0 is the inversion of the prime row
        """
        semitone_differences = np.zeros(11, dtype = int)
        for i in range(11):
            semitone_differences[i] = prime_row[i+1] - prime_row[i]
        semitone_differences = semitone_differences * -1 #reverses distances between prime row notes
        semitone_differences = (semitone_differences + 12) % 12 
        prime_inversion = np.zeros(12, dtype = int)
        prime_inversion[0] = prime_row[0]
        for i in range(1,12):
            prime_inversion[i] = prime_inversion[i-1] + semitone_differences[i-1]
        prime_inversion %=  12
        
        return prime_inversion
    
    @classmethod
    def prime_retrograde_inversion(cls, prime_row: np.ndarray) -> np.ndarray:
        """
        Returns RI0
        
        RI0 is the retrograde inversion of a tone row that 
        starts on the same note as the prime row
        """
        pr_ret_inv = np.flip(cls.prime_inversion(prime_row))
        pr_ret_inv = cls.transpose_row(pr_ret_inv, prime_row[0] - pr_ret_inv[0])
        return pr_ret_inv
    
    @classmethod
    def prime_transformations_list(cls, prime_row: np.ndarray, include_prime_row = True) -> np.ndarray:
        """
        Returns a numpy array of all prime transformations of a given row
        in the following order:\n
        [P0, R0, I0, RI0]\n
        
        Array includes prime row in position [0] by default
        """
        if include_prime_row:
            return np.array([prime_row, cls.prime_retrograde(prime_row), cls.prime_inversion(prime_row), cls.prime_retrograde_inversion(prime_row)])
        
        return np.array([cls.prime_retrograde(prime_row), cls.prime_inversion(prime_row), cls.prime_retrograde_inversion(prime_row)])
    
    @classmethod
    def transpose_row(cls, tone_row: np.ndarray, semitones: int) -> np.ndarray:
        """
        Moves all notes in a tone row up(positive int) or down(negative int) by a 
        number or semitones.
        
        Returns the transposed list as a numpy array
        """
        semitone_distance = semitones
        if semitone_distance < 0 and semitone_distance < -12:
            semitone_distance = ((semitone_distance + 12) * -1)
        if semitone_distance < 0 and semitone_distance > -12:
            semitone_distance += 12 
        
        return (tone_row + semitone_distance) % 12
    
    @classmethod
    def get_transformation(cls, prime_row: np.ndarray, transformation_name: str) -> np.ndarray:
        """
        Returns a tone tow that corresponds to the specified transformation name
        
        Transformations names:\n
        'P' refers to a specific transposition of the prime row.\n
        'P0' is the prime row.\n
        'I' refers to a specific inversion of the prime row.\n
        'I0' is the prime inversion.\n
        'R' refers to a specific retrograde(reverse order) of the prime row.\n
        'R0' is the prime retrograde.\n
        'RI' refers to a specific retrograde of the prime row's inversion.\n
        'RI0' is the prime retrograde inversion.\n
        """
        if transformation_name == "P0":
            return prime_row
        
        if transformation_name == "R0":
            return cls.prime_retrograde(prime_row)
        
        if transformation_name == "I0":
            return cls.prime_inversion(prime_row)
        
        if transformation_name == "RI0":
            return cls.prime_retrograde_inversion(prime_row)
        
        if transformation_name.startswith("P"):
            return cls.transpose_row(prime_row, int(transformation_name[1:]))
        
        if transformation_name.startswith("RI"):
            return cls.transpose_row(cls.prime_retrograde_inversion(prime_row), int(transformation_name[2:]))
        
        if transformation_name.startswith("R"):
            return cls.transpose_row(cls.prime_retrograde(prime_row), int(transformation_name[1:]))
        
        if transformation_name.startswith("I"):
            return cls.transpose_row(cls.prime_inversion(prime_row), int(transformation_name[1:]))
        
        raise ValueError("Invalid transformation name")
        
    @classmethod
    def find_transformations(cls, prime_row: np.ndarray, transformed_row: np.ndarray, find_all = False, row = False, inversion = False,  row_retrograde = False, inv_retrograde = False) -> list:
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
            if row and np.array_equal(transformed_row, cls.transpose_row(prime_row, i)):
                transformations.append(f"P{str(i)}")
            
            if row_retrograde and np.array_equal(transformed_row, cls.transpose_row(cls.prime_retrograde(prime_row), i)):
                transformations.append(f"R{str(i)}")
            
            if inversion and np.array_equal(transformed_row, cls.transpose_row(cls.prime_inversion(prime_row), i)):
                transformations.append(f"I{str(i)}")
            
            if inv_retrograde and np.array_equal(transformed_row, cls.transpose_row(cls.prime_retrograde_inversion(prime_row), i)):
                transformations.append(f"RI{str(i)}")
            
        return transformations
    
    @classmethod
    def validate_row(cls, tone_row: np.ndarray):
        """
        Checks if a tone row is 12 notes long and consists of 
        twelve unique notes.
        
        Raises ValueError if the parameters are not met.
        """
        if len(tone_row) != 12:
            raise ValueError("Row provided is not the right length. (should be 12 tones long)")
        sorted_row = np.sort(tone_row)
        reference_row = np.arange(12)
        if sorted_row.all() != reference_row.all():
            raise ValueError("The provided tone row is not a valid 12-tone row")