import fitz  # PyMuPDF
import pandas as pd
import os

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_excel(file_path):
    df_list = pd.read_excel(file_path, sheet_name=None)
    text = ""
    for sheet_name, df in df_list.items():
        text += f"\n\nSheet: {sheet_name}\n"
        text += df.to_string(index=False)
    return text

def extract_text_from_docx(file_path):
    import docx
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_any_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".xlsx", ".xls"]:
        return extract_text_from_excel(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file type. Please use PDF, Excel, or DOCX."

def extract_uploaded_file_content(file):
    file_path = file.name
    with open(file_path, "wb") as f:
        f.write(file.read())
    return extract_text_from_any_file(file_path)

def load_all_files_from_folder(folder_path="data"):
    content = ""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            content += f"\n\n==== {file_name} ====\n"
            content += extract_text_from_any_file(file_path)
    return content
