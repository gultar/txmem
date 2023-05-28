import nltk
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_matching_sentences(corpus, target_string, similarity_threshold=0.7):
    lemmatizer = WordNetLemmatizer()
    sentences = sent_tokenize(corpus)
    target_words = nltk.word_tokenize(target_string.lower())
    target_lemmas = [lemmatizer.lemmatize(word) for word in target_words]
    matching_sentences = []

    for sentence in sentences:
        sentence_words = nltk.word_tokenize(sentence.lower())
        sentence_lemmas = [lemmatizer.lemmatize(word) for word in sentence_words]

        if set(target_lemmas).issubset(set(sentence_lemmas)):
            matching_sentences.append(sentence)
        else:
            similarity = calculate_similarity(target_lemmas, sentence_lemmas)
            if similarity >= similarity_threshold:
                matching_sentences.append(sentence)

    return matching_sentences

def calculate_similarity(target_lemmas, sentence_lemmas):
    # Convert lemmas to strings
    target_string = " ".join(target_lemmas)
    sentence_string = " ".join(sentence_lemmas)

    # Vectorize the target string and the sentence
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([target_string, sentence_string])

    # Calculate the cosine similarity between the vectors
    cosine_sim = cosine_similarity(vectors[0], vectors[1])[0][0]
    
    return cosine_sim

