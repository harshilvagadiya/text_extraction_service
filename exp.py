import fitz  # PyMuPDF for PDF extraction
import docx  # python-docx for DOCX extraction
import os
import requests
from typing import Union

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    Args:
        file_path (str): Path to the PDF file (local file or URL).
    Returns:
        str: Extracted text.
    """
    text = ""
    try:
        # Open the PDF file
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text("text")  # Extract text from each page
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
    return text


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file.
    Args:
        file_path (str): Path to the DOCX file (local file or URL).
    Returns:
        str: Extracted text.
    """
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"  # Append each paragraph's text
    except Exception as e:
        print(f"Error extracting DOCX text: {e}")
    return text


def extract_text_from_doc(file_path: str) -> str:
    """
    Extract text from a DOC file (using pywin32 or unoconv).
    Args:
        file_path (str): Path to the DOC file (local file or URL).
    Returns:
        str: Extracted text.
    """
    import win32com.client  # pywin32 (only for Windows)
    text = ""
    try:
        # Open the Word application
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(file_path)
        text = doc.Content.Text  # Extract text from the DOC file
        doc.Close()
        word.Quit()
    except Exception as e:
        print(f"Error extracting DOC text: {e}")
    return text


def download_file(url: str, download_path: str) -> str:
    """
    Download a file from a URL to the local file system.
    Args:
        url (str): URL of the file to download.
        download_path (str): The local path to save the file.
    Returns:
        str: Local path to the downloaded file.
    """
    try:
        response = requests.get(url, stream=True)
        with open(download_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception as e:
        print(f"Error downloading file: {e}")
    return download_path


def extract_text_from_file(file: Union[str, dict]) -> str:
    """
    Extract text from PDF, DOC, or DOCX file.
    Args:
        file (Union[str, dict]): Path to the file or URL to be downloaded.
    Returns:
        str: Extracted text.
    """
    text = ""
    
    if isinstance(file, dict) and file.get('url'):
        # Download the file from the URL
        local_file = "downloaded_file" + os.path.splitext(file['url'])[1]
        download_file(file['url'], local_file)
        file = local_file

    if file.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file)
    elif file.lower().endswith('.docx'):
        text = extract_text_from_docx(file)
    elif file.lower().endswith('.doc'):
        text = extract_text_from_doc(file)
    else:
        print("Unsupported file format.")
    
    return text




# Example usage for extracting text from local files
# file_path_pdf = "C:/Users/hppat/Downloads/harshil_vagadiya_python_developer.pdf"
# file_path_docx = "C:/Users/hppat/Downloads/file-sample_100kB.docx"
# file_path_doc = "path/to/file.doc"

# pdf_text = extract_text_from_file(file_path_pdf)
# docx_text = extract_text_from_file(file_path_docx)
# doc_text = extract_text_from_file(file_path_doc)

# print(pdf_text)
# print(docx_text)
# print(doc_text)

# Example usage for extracting text from a URL
# url_pdf = {"url": "http://example.com/file.pdf"}
# url_docx = {"url": "http://example.com/file.docx"}
# url_doc = {"url": "http://example.com/file.doc"}

# pdf_text_url = extract_text_from_file(url_pdf)
# docx_text_url = extract_text_from_file(url_docx)
# doc_text_url = extract_text_from_file(url_doc)

