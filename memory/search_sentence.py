import nltk
from nltk.tokenize import sent_tokenize
from lookup import find_matching_sentences
import json
import multiprocessing
import time
import regex

def split_text_into_sentences(text):
    regex_pattern = r'(?<!^M\. [A-Z])(?<!\w\.\w.)(?<!\b(?:Mme|Mlle|Mr|Mrs|Ms|Dr)\.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\;|\☒|\☐)(?!\s*»)(?!\.[A-Z]\.)(\s|(?<=^|\s)M\.\s[A-Z]\..*)'
    sentences = regex.split(regex_pattern, text)
    return sentences

def process_document(document, expression):
    filename, entry = document
    en_text = entry['EN']['text']
    fr_text = entry['FR']['text']
    
    if isinstance(en_text, str) and isinstance(fr_text, str):
        en_sentences = split_text_into_sentences(en_text)
        fr_sentences = split_text_into_sentences(fr_text)
        
        matching_sentences = []
        fr_matching_sentences = []
        
        for en_sentence, fr_sentence in zip(en_sentences, fr_sentences):
            en_matching_sentences = find_matching_sentences(en_sentence, expression)
            if en_matching_sentences:
                matching_sentences += en_matching_sentences
                fr_matching_sentences.append(fr_sentence)
    
    
        return matching_sentences, fr_matching_sentences
    else:
        return [],[]

def search_expression(expression):
    st = time.time()
    with open('memory.json', 'r') as file:
        dictionary = json.load(file)
    
    documents = list(dictionary.items())
    pool = multiprocessing.Pool()
    results = pool.starmap(process_document, [(doc, expression) for doc in documents])
    pool.close()
    pool.join()
    
    matching_sentences = []
    fr_matching_sentences = []
    
    for result in results:
        matching_sentences.extend(result[0])
        fr_matching_sentences.extend(result[1])
    
    et = time.time()
    elapsed_time = et - st
    
    print('Execution time:', elapsed_time, 'seconds')
    return matching_sentences, fr_matching_sentences

if __name__ == '__main__':
    nltk.download('punkt')
    expression = input('Enter the expression you want to search: ')
    print('Searching...')
    results, fr_results = search_expression(expression)
    
    if results:
        print(f'Matching sentences for expression "{expression}":')
        for en_sentence, fr_sentence in zip(results, fr_results):
            print(f'English Sentence: {en_sentence}')
            print(f'French Sentence: {fr_sentence}')
            print('---')
    else:
        print(f'No matching sentences found for expression "{expression}".')
