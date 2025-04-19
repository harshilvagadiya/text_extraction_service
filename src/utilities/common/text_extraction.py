import fitz
import docx
import requests
import os
from typing import Optional
from fastapi import HTTPException

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    try:
        doc = fitz.open(file_path)
        text = "\n".join([page.get_text() for page in doc])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting PDF text: {e}")
    return text

def extract_text_from_docx(file_path: str) -> str:
    text = ""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting DOCX text: {e}")
    return text

def extract_text_from_doc(file_path: str) -> str:
    import win32com.client
    text = ""
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(file_path)
        text = doc.Content.Text
        doc.Close()
        word.Quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting DOC text: {e}")
    return text

def download_file_from_url(url: str, download_dir: str) -> str:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        filename = url.split("/")[-1]
        file_path = os.path.join(download_dir, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {e}")

def extract_text_from_file(file_url: Optional[str] = None, file_path: Optional[str] = None, download_dir: str = "temp/") -> str:
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    try:
        if file_url:
            file_path = download_file_from_url(file_url, download_dir)

        if file_path:
            file_format = file_path.split('.')[-1].lower()
        else:
            raise HTTPException(status_code=400, detail="No file provided or file URL provided.")

        if file_format == "pdf":
            return extract_text_from_pdf(file_path)
        elif file_format == "docx":
            return extract_text_from_docx(file_path)
        elif file_format == "doc":
            return extract_text_from_doc(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text from file: {e}")


# file_url = "https://openxcell-development-public.s3.ap-south-1.amazonaws.com/teachbetter/tools/uploaded_files/personalized_report_generator/22_binit_agarwalla_20250321165628_concept_explainer-understanding_cells__the_building_blocks_of_life.pdf"
# text = extract_text_from_file(file_url=file_url)
# print(">>>>>>>>>>",text)
