import os
from difflib import SequenceMatcher
from docx_extractor import extract_text_from_docx
import lxml.etree as ET
import json
from files_classifier import classify_filename
# This here is to create a list of words, but it's optional
from make_keywords import extract_keywords


memory = {}

dir_to_build = "./files"

root_path = ""

# Function to calculate similarity ratio between two strings
def calculate_similarity_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Function to group similar filenames together
def group_filenames(path):
    print(path)
    grouped_files = {}
    for root, dirs, files in os.walk(path):
        for filename in files:
            if "~$" not in filename:
                filepath = os.path.join(root, filename)
                language = classify_filename(filename)
                
                if language not in grouped_files:
                    grouped_files[language] = []
                grouped_files[language].append(filepath)
    return grouped_files


# Function to pair filenames
def pair_filenames(english_filenames, french_filenames):
    pairs = []
    for english_filename in english_filenames:
        max_similarity = 0
        best_match = None
        english_language = classify_filename(english_filename)
        
        for french_filename in french_filenames:
            french_language = classify_filename(french_filename)
            
            if english_filename != french_filename:
                similarity = calculate_similarity_ratio(english_filename, french_filename)
                
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_match = french_filename
        
        pairs.append((english_filename, best_match))
    print(pairs)
    return pairs

def add_pair_of_texts_to_memory(en_text, fr_text, en_filename, fr_filename):
    
    if not fr_filename:
        return
    if not en_filename:
        return
    
    memory[en_filename] = {
        'EN':{
            'filename':os.path.basename(en_filename),
            'path':"",
            'text':en_text,
        },
        'FR':{
            'filename':os.path.basename(fr_filename),
            'path':"",
            'text':fr_text
        }
    }



def save_memory():
    # Write the extracted text to a JSON file
    with open('memory.json', 'w') as outfile:
        json.dump(memory, outfile)

def cycle_through_dirs(path):
    
    for root, dirs, files in os.walk(path):
        
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            grouped = group_filenames(dir_path)
            if 'révision' not in dir and 'revision' not in dir and 'référence' not in dir and 'Révision' not in dir and 'révisé' not in dir:

                print('DIR:', dir)

                if 'English' in grouped and 'French' in grouped:
                    pairs = pair_filenames(grouped['English'], grouped['French'])

                    for pair in pairs:
                        en_filename = pair[0]
                        fr_filename = pair[1]
                        en_text = extract_text_from_docx(en_filename)
                        fr_text = extract_text_from_docx(fr_filename)
                        # print('Extracted')
                        add_pair_of_texts_to_memory(en_text, fr_text, en_filename, fr_filename)

                        print("English : ",en_filename)
                        print("French : ",fr_filename)
                        print()


                print()
                print("------------")
    save_memory()

# Test the function
cycle_through_dirs(dir_to_build)

