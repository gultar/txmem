import gensim
from gensim.models import Word2Vec
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import multiprocessing

# Load text corpus from a JSON file
with open("./memory.json", "r", encoding="utf-8") as corpus_file:
    corpus = corpus_file.read()

# Tokenize the corpus into sentences
sentences = sent_tokenize(corpus)

# Tokenize each sentence into words
tokenized_sentences = [word_tokenize(sentence.lower()) for sentence in sentences]

# Define and train a Word2Vec model
num_features = 200  # Adjust the number of features (dimensions) as needed
min_word_count = 1  # Minimum word count threshold
context_size = 5   # Context window size
num_workers = multiprocessing.cpu_count()  # Use all available CPU cores

model = Word2Vec(
    tokenized_sentences,
    vector_size=num_features,
    min_count=min_word_count,
    window=context_size,
    workers=num_workers,
)

# Example usage to get a sentence vector for a target word or sentence
target_sentence = "insight"
target_vector = model.wv[target_sentence]

# Define a similarity threshold to filter relevant passages
similarity_threshold = 0.8  # Adjust as needed

# Extract relevant passages and their associated filenames
relevant_passages = []

# Replace this example with your own list of filenames if you have multiple files
filenames = ["memory.json"] * len(sentences)

def sentence_vector(sentence):
    words = word_tokenize(sentence.lower())
    vectors = [model.wv[word] for word in words if word in model.wv]
    if vectors:
        return sum(vectors) / len(vectors)
    else:
        return None

for i, sentence in enumerate(sentences):
    vector = sentence_vector(sentence)
    if vector is not None and model.wv.cosine_similarities(target_vector, [vector])[0] >= similarity_threshold:
        relevant_passages.append((filenames[i], sentence))

# Print relevant passages along with their filenames
for filename, passage in relevant_passages:
    print(f"File: {filename}")
    print(f"Passage: {passage}")
    print("-" * 30)

# Now you have extracted and printed relevant passages along with their filenames.

