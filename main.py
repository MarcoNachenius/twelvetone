import TwelveTone as tt

print(tt.twelve_tone_matrix.generate_twelve_tone_matrix(tt.tone_row.generate_random_row()))
    #found_single_combinatorials = False
    #while not found_single_combinatorials:
    #    prime_row = tone_row.generate_random_row()
    #    trichords = combinatoriality.find_trichordal_combinatorials(prime_row)
    #    tetrachords = combinatoriality.find_tetrachordal_combinatorials(prime_row)
    #    hexachords = combinatoriality.find_hexachordal_combinatorials(prime_row)
    #    
    #    #creates a .musicxml report of a random tone row that that has 1 hexachordal,
    #    #trichordal and tetrachordal combinatorial. 
    #    if len(trichords) > 0 and len(tetrachords) > 0 and len(hexachords) > 0:
    #        print("Row with trichordal combinatoriality has been found!")
    #        print(prime_row)
    #        print(trichords)
    #        music_xml_writer.write_twelvetone_report(prime_row, "test_file")
    #        found_single_combinatorials = True
    #print(combinatoriality.find_tetrachordal_combinatorials(list(range(12))))