import music21
import os
import numpy as np
from combinatoriality import combinatoriality
from note_names import note_names
from tone_row import tone_row

class music_xml_writer():
    
    @classmethod
    def write_twelvetone_report(cls, prime_row: np.ndarray, file_name: str, directory = None, score_title = None, include_combinatorials = True):
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
    def create_twelve_tone_report_xml(cls, prime_row: np.ndarray, score_title = None, include_combinatorials = True):
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
    def create_stemless_measure(cls, transformation_name: str, prime_row: np.ndarray):
        """
        Returns a music21 measure object.
        Part consists of twelve stemless quarter notes with a hidden 12/4
        time signature.
        """
        
        measure = music21.stream.Measure()
        measure.timeSignature = music21.meter.TimeSignature('12/4')
        measure.timeSignature.style.hideObjectOnPrint = True
        pr_part_notes = tone_row.get_transformation(prime_row, transformation_name)
        note_names.convert_numbers_to_note_names(pr_part_notes, note_names.number_to_sharp_treble_clef_positions)
        for pitch in pr_part_notes:
            note = music21.note.Note(pitch)
            note.stemDirection = "noStem"
            measure.append(note)
        
        return measure
    
    @classmethod
    def create_prime_transformation_part(cls, prime_transformation_name: str, prime_row: np.ndarray):
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
    def create_hexachord_combinatorial_part(cls, transformation_name: str, prime_row: np.ndarray): 
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
    def create_tetrachord_combinatorial_part(cls, transformation_name: str, prime_row: np.ndarray):
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
    def create_trichord_combinatorial_part(cls, transformation_name: str, prime_row: np.ndarray):
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
    
