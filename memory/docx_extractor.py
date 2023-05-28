import docx2txt
import re
import nltk
nltk.download('punkt')

def extract_text_from_docx(file_path):
    try:
        text = docx2txt.process(file_path)
        return text
    except Exception as e:
        print(f"An error occurred while extracting text: {e}")
        return ''
    


def segment_text(text, lang):
    # Segment the text into sentences
    sentences = nltk.sent_tokenize(text, language=lang)
    return sentences
