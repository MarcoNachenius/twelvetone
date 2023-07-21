import numpy as np
from twelve_tone_matrix import twelve_tone_matrix

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