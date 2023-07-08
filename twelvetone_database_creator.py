import numpy as np
import math
import database_entry_creator 
import sqlite3
"""
This is one of the main features of twelvetone.
This main class creates a database that holds the information
of every twelve-tone row in existence. This information includes the intervals
between every note of a tone row, every prime transformation(I0, R0, RI0) of a tone row, as well as
all of the hexachordal, tetrachordal and trichordal combinatorials of that row.

Database tables:
- prime_transformations
- combinatoriality
- interval_sizes
"""
class tone_row_permutations():
    
    @classmethod
    def build_database(cls, database_name: str, tone_row_length = 11):
        """Creates a database with (tone_row_length)! rows in the /twelve_tone_database
        project file subject, with a numbered int primary key and one column('intervals')
        where each row contains numpy.zeroes(tone_row_length).
        
        Args:
            database_name (str): name of database must include '.db' suffix
            tone_row_length (int): made adjustable to aid with testing.
        """
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        create_all_value_table = '''CREATE TABLE IF NOT EXISTS all_values (
                    prime_row TEXT,
                    prime_retrograde TEXT,
                    prime_inversion TEXT,
                    prime_retrograde_inversion TEXT,
                    prime_row_intervals TEXT,
                    prime_retrograde_intervals TEXT,
                    prime_inversion_intervals TEXT,
                    prime_retrograde_inversion_intervals TEXT,
                    combinatorial_hexachords TEXT,
                    combinatorial_tetrachords TEXT,
                    combinatorial_trichords TEXT
                    )'''
        cursor.execute(create_all_value_table)
        connection.commit()
        insert_query = '''INSERT INTO all_values (
                        prime_row,
                        prime_retrograde,
                        prime_inversion,
                        prime_retrograde_inversion,
                        prime_row_intervals,
                        prime_retrograde_intervals,
                        prime_inversion_intervals,
                        prime_retrograde_inversion_intervals,
                        combinatorial_hexachords,
                        combinatorial_tetrachords,
                        combinatorial_trichords
                        )
                        VALUES (
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?)''' #11 * '?'
        for i in range(math.factorial(tone_row_length)):
            #create object that contains all columns of linked tables
            entry = database_entry_creator.create_database_entry.all_values_entry(i)
            
            cursor.execute(insert_query, (
                str(entry.P0),
                str(entry.R0),
                str(entry.I0),
                str(entry.RI0),
                str(entry.P0_intervals),
                str(entry.R0_intervals),
                str(entry.I0_intervals),
                str(entry.RI0_intervals),
                str(entry.combinatorial_hexachords),
                str(entry.combinatorial_tetrachords),
                str(entry.combinatorial_trichords)
                ))
            connection.commit()
        connection.close()
    


        
        

if __name__== "__main__":
    tone_row_permutations.build_database("./twelve_tone_database/yo.db")