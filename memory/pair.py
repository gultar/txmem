import os
from difflib import SequenceMatcher
from docx_extractor import extract_text_from_docx
import lxml.etree as ET
import json
from files_classifier import is_french_filename
# This here is to create a list of words, but it's optional
from make_keywords import extract_keywords


memory = {}

dir_to_build = "./files"

root_path = ""

# Function to calculate similarity ratio between two strings
def calculate_similarity_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Function to group similar filenames together
def group_filenames(path, folder_name):
    
    grouped_files = []
    for root, dirs, files in os.walk(path):
        pair = {
            "English":"",
            "French":""
        }
        for filename in files:
            filepath = os.path.join(root, filename)
            
            if folder_name in filename:
                pair["English"] = filepath
            else:
                pair["French"] = filepath

        grouped_files.append(pair)
    return grouped_files


# Function to pair filenames
def pair_filenames(english_filenames, french_filenames):
    pairs = []
    for english_filename in english_filenames:
        max_similarity = 0
        best_match = None
        english_language = is_french_filename(english_filename)
        
        for french_filename in french_filenames:
            french_language = is_french_filename(french_filename)
            
            if english_filename != french_filename:
                similarity = calculate_similarity_ratio(english_filename, french_filename)
                
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_match = french_filename
        
        pairs.append((english_filename, best_match))
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

import win32com.client

def extract_text_from_doc(doc_file_path):
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False  # Prevents the Word application window from opening

        doc = word.Documents.Open(doc_file_path)
        if doc.has_key("Content"):
            content = doc.Content.Text
        else:
            return ""

        doc.Close()
        word.Quit()

        return content
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    
def extract_text(doc_file_path, is_docx=True):
    if is_docx:
        return extract_text_from_docx(doc_file_path)
    else:
        return extract_text_from_doc(doc_file_path)


def save_memory():
    # Write the extracted text to a JSON file
    with open('memory.json', 'w', encoding="utf-8") as outfile:
        json.dump(memory, outfile)

def cycle_through_dirs(path):
    errors = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            grouped_pairs = group_filenames(dir_path, dir)
            

            for pair in grouped_pairs:
                en_filename = pair["English"]
                fr_filename = pair["French"]

                try:
                    is_docx_en = ".docx" in en_filename
                    is_docx_fr = ".docx" in fr_filename

                    en_text = extract_text(en_filename, is_docx_en)

                    fr_text = extract_text(fr_filename, is_docx_fr)

                    if len(en_text) != 0 and len(fr_text) != 0:
                        add_pair_of_texts_to_memory(en_text, fr_text, en_filename, fr_filename)

                        print("English : ",en_filename)
                        print("French : ",fr_filename)
                    else:
                        print("Could not load TX pair for : ",en_filename)
                        errors.append(en_filename)

                except Exception as e:
                    print(e)
                                
                
                
                print()


    save_memory()
    print("Encountered an error with the following TX pairs:")
    for e in errors: print("=>",e)
    print("=============================================")
    print("FINISHED CREATING MEMORY")
    print("=============================================")

# Test the function
cycle_through_dirs(dir_to_build)
print("FINISHED CREATING MEMORY")
