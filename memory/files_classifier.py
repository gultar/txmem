# Function to extract the language identifier from a filename
def classify_filename(filename):
    # Define the French and revision identifiers
    french_identifiers = ['FR.', 'fra.', 'fr.', 'FR -', '(FR)', '-FR','(french version)', 
                        'Simon', 'f - ','f-', 'fre',' FR ','[FR]',' - FR','FR[1]',"FINAL","final","-f"
                        'French Translation','REV.', 'rev.']
    english_classifiers = ["ENG","English","EN","- en","-en"]

    for identifier in french_identifiers:
        if identifier.lower() in filename.lower():
            return 'French'
    return 'English'