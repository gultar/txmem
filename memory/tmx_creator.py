import lxml.etree as ET
import codecs
import nltk
import xml.sax.saxutils as saxutils

# 
# WARNING: It seems like this script doesn't manage to create SDL Trados-ready .tmx files. 
# Importing the tmx in Trados often failes because of issues with obscure XML rules.
# 

nltk.download('punkt')

def segment_text(text, lang):
    # Segment the text into sentences
    sentences = nltk.sent_tokenize(text, language=lang)
    return sentences

def create_tmx_entry(en_sentences, fr_sentences):
    # Create a new TMX entry for a pair of English and French sentences
    tu = ET.Element('tu')

    # Add English sentences
    tuv_en = ET.SubElement(tu, 'tuv')
    tuv_en.attrib['lang'] = 'en'
    for sentence in en_sentences:
        seg_en = ET.SubElement(tuv_en, 'seg')
        seg_en.text = saxutils.escape(sentence)  # Escape XML special characters

    # Add French sentences
    tuv_fr = ET.SubElement(tu, 'tuv')
    tuv_fr.attrib['lang'] = 'fr'
    for sentence in fr_sentences:
        seg_fr = ET.SubElement(tuv_fr, 'seg')
        seg_fr.text = saxutils.escape(sentence)  # Escape XML special characters

    return tu

def create_tmx():
    # Create a new TMX document
    tm = ET.Element('tmx', version='1.4')
    header = ET.SubElement(tm, 'header', creationtool='Python')
    body = ET.SubElement(tm, 'body')
    return tm, body

def add_tmx_entry(tm, body, en_text, fr_text, filename, filename_fr):
    # Segment English and French texts into sentences
    en_sentences = segment_text(en_text, 'english')
    fr_sentences = segment_text(fr_text, 'french')

    # Add a new TMX entry to the document
    tu = create_tmx_entry(en_sentences, fr_sentences)
    body.append(tu)

def save_tmx(tmx, tmx_file):
    # Write the TMX document to a file
    with codecs.open(tmx_file, 'w', encoding='utf-8') as f:
        f.write(ET.tostring(tmx, pretty_print=True, encoding='unicode'))
