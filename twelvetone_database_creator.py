import math 
import sqlite3
from database_permutation_writer import *
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
class database_constructor():
    
    @classmethod
    def build_database(cls, database_name: str, tone_row_length = 12):
        test_range = 6000
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
                    P0 VARCHAR(100),
                    R0 VARCHAR(100),
                    I0 VARCHAR(100),
                    RI0 VARCHAR(100),
                    combinatorial_hexachords VARCHAR(100),
                    combinatorial_tetrachords VARCHAR(100),
                    combinatorial_trichords VARCHAR(100),
                    P0_intervals VARCHAR(100),
                    R0_intervals VARCHAR(100),
                    I0_intervals VARCHAR(100),
                    RI0_intervals VARCHAR(100)
                    )'''
        cursor.execute(create_all_value_table)
        connection.commit()
        insert_query = '''INSERT INTO all_values (
                        P0,
                        R0,
                        I0,
                        RI0,
                        combinatorial_hexachords,
                        combinatorial_tetrachords,
                        combinatorial_trichords,
                        P0_intervals,
                        R0_intervals,
                        I0_intervals,
                        RI0_intervals
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
                        ?
                        )''' # 11 Columns
        print("Creating database...")
        for i in range(test_range): #math.factorial(tone_row_length -1):
            # Create object that contains all columns of linked tables
            entry = create_database_entry.all_values_entry(i)
            
            # Convert tone row arrays to strings with a specific order
            p0_string = ", ".join(str(x) for x in entry.P0)
            r0_string = ", ".join(str(x) for x in entry.R0)
            i0_string = ", ".join(str(x) for x in entry.I0)
            ri0_string = ", ".join(str(x) for x in entry.RI0)
            combinatorial_hexachords_string = ", ".join(str(x) for x in entry.combinatorial_hexachords)  
            combinatorial_tetrachords_string = ", ".join(str(x) for x in entry.combinatorial_tetrachords)
            combinatorial_trichords_string = ", ".join(str(x) for x in entry.combinatorial_trichords)   
            p0_intervals_string = ", ".join(str(x) for x in entry.P0_intervals)
            r0_intervals_string = ", ".join(str(x) for x in entry.R0_intervals)
            i0_intervals_string = ", ".join(str(x) for x in entry.I0_intervals)
            ri0_intervals_string = ", ".join(str(x) for x in entry.RI0_intervals)

            cursor.execute(insert_query, (
                p0_string,
                r0_string,
                i0_string,
                ri0_string,
                combinatorial_hexachords_string,
                combinatorial_tetrachords_string,
                combinatorial_trichords_string,
                p0_intervals_string,
                r0_intervals_string,
                i0_intervals_string,
                ri0_intervals_string
            ))
            print("Progress: " + str(math.floor(i/(test_range-1) *  100)) + "%    Row number : " + str(i+1) + "   Permutation: " + p0_string, end="\r")
            connection.commit()
        connection.close()
        print("\nDatabase successfully created!")
        
        
def test_uniqueness():
    row_length = 12
    max_row_number = math.factorial(row_length-1)
    generated_tone_rows = set()
    test_number = 10000

    print("==============================\nChecking for duplicates in set")
    for row_number in range(test_number):
        tone_row = permutation_calculator.find_permutation(row_number)
        tuple_tone_row = tuple(tone_row) 
        if tuple_tone_row in generated_tone_rows:
            print(f"Duplicate found at row_number {row_number}. Row number:\n {tone_row}")
        generated_tone_rows.add(", ".join(str(x) for x in tuple_tone_row))
        print("Progress: " + str(math.floor(row_number/(test_number-1) *  100)) + "%    Rows tested: " + str(row_number+1), end="\r")

    print(f"\nNo duplicates were found!\n")

test_uniqueness()
database_constructor.build_database("./twelve_tone_database/small_database.db")