import nltk
import re
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz
import regex

    
def tokenize(corpus):
    regex_pattern = r'(?<!^M\. [A-Z])(?<!\w\.\w.)(?<!\b(?:Mme|Mlle|Mr|Mrs|Ms|Dr)\.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\;|\☒|\☐)(?!\s*»)(?!\.[A-Z]\.)(\s|(?<=^|\s)M\.\s[A-Z]\..*)'
    sentences = regex.split(regex_pattern, corpus)
    return sentences


def find_matching_sentences(corpus, target_string, similarity_threshold=0.8):
    lemmatizer = WordNetLemmatizer()
    sentences = tokenize(corpus)
    target_words = nltk.word_tokenize(target_string.lower())
    target_lemmas = [lemmatizer.lemmatize(word) for word in target_words]
    matching_sentences = []

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


def fuzzy_match(str1, str2):
    return fuzz.ratio(str1, str2) / 100


