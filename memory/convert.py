from glob import glob
import re
import os
import win32com.client as win32
from win32com.client import constants
import os
path = os.path.join(os.path.dirname(__file__), 'convert\\**\*.doc')
# Create list of paths to .doc files
doc_paths = glob(path, recursive=True)

def save_as_docx(doc_path):
    # Check if corresponding .docx file already exists
    docx_path = re.sub(r'\.\w+$', '.docx', doc_path)
    if os.path.exists(docx_path):
        print(f"Skipping conversion for {doc_path} (already exists: {docx_path})")
        return
    else:
        print('Converting',doc_path)

    # Opening MS Word
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(doc_path)
    doc.Activate()

    # Rename path with .docx
    new_file_abs = os.path.abspath(doc_path)
    new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)

    # Save and Close
    word.ActiveDocument.SaveAs(
        new_file_abs, FileFormat=constants.wdFormatXMLDocument
    )
    
    doc.Close(False)

for doc_path in doc_paths:
    
    save_as_docx(doc_path)
