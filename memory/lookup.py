import nltk
import re
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz
import regex

    


def tokenize(corpus):
    regex_pattern = r'(?<!^M\. [A-Z])(?<!\w\.\w.)(?<!\b(?:Mme|Mlle|Mr|Mrs|Ms|Dr)\.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\;|\:)(?!\s*»)(?!\.[A-Z]\.)(\s|(?<=^|\s)M\.\s[A-Z]\..*)'
    sentences = regex.split(regex_pattern, corpus)
    return sentences

def is_enclosed_in_double_quotes(input_string):
    pattern = r'^"([^"]*)"$'
    return bool(regex.match(pattern, input_string))

def find_matching_sentences(corpus, target_string, similarity_threshold=0.6):
    lemmatizer = WordNetLemmatizer()
    print('Type of corpus', type(corpus))
    if isinstance(corpus, str):
        sentences = tokenize(corpus)
        target_words = nltk.word_tokenize(target_string.lower())
        target_lemmas = [lemmatizer.lemmatize(word) for word in target_words]
        matching_sentences = []

        # Check if the target string is enclosed in double quotes
        if is_enclosed_in_double_quotes(target_string):
            target_string = target_string.strip('"')
            # Exact match when the target string is in quotes
            for sentence in sentences:
                if target_string in sentence:
                    matching_sentences.append(sentence)
                    
        else:
            # Fuzzy matching when the target string is not in quotes
            for sentence in sentences:
                sentence_words = nltk.word_tokenize(sentence.lower())
                sentence_lemmas = [lemmatizer.lemmatize(word) for word in sentence_words]

                if set(target_lemmas).issubset(set(sentence_lemmas)):
                    matching_sentences.append(sentence)
                else:
                    sentence_string = " ".join(sentence_lemmas)
                    if fuzzy_match(target_string, sentence_string) >= similarity_threshold:
                        matching_sentences.append(sentence)

        return matching_sentences
    else:
        return []



def fuzzy_match(str1, str2):
    return fuzz.ratio(str1, str2) / 100

   



   


