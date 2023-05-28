import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
import string

NUM_KEYWORDS = 100

def is_punctuation(word):
    return all(char in string.punctuation for char in word)



def extract_keywords(corpus, language='english'):
    # Tokenize the corpus into sentences
    sentences = sent_tokenize(corpus)

    # Tokenize each sentence into words and perform lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word.lower()) for sentence in sentences
             for word in word_tokenize(sentence)]

    # Filter out stopwords and non-nouns
    stop_words = set(stopwords.words(language))
    tagged_words = nltk.pos_tag(words)

    if language == 'french':
        nouns = [word for word, tag in tagged_words if tag.startswith('N') and word not in stop_words
                 and not is_punctuation(word) and "’" not in word]
    else:
        nouns = [word for word, tag in tagged_words if tag.startswith('NN') and word not in stop_words
                 and not is_punctuation(word)]

    # Calculate noun frequency distribution
    fdist = FreqDist(nouns)

    # Get the 50 most common nouns
    keywords = [noun for noun, frequency in fdist.most_common(NUM_KEYWORDS) if noun]

    return keywords
