import aiofiles
import asyncio
import PyPDF2
from docx import Document

async def read_txt(file_path: str) -> str:
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
        return await f.read()


def read_pdf_sync(file_path: str) -> str:
    text = []
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return '\n'.join(text)
    except:
        return ""


def read_docx_sync(file_path: str) -> str:
    try:
        doc = Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    except:
        return ""


async def get_text_from_file(file_path: str, file_ext: str) -> str:
    if file_ext == '.txt':
        return await read_txt(file_path)
    elif file_ext == '.pdf':
        return await asyncio.to_thread(read_pdf_sync, file_path)
    elif file_ext in ['.docx', '.doc']:
        return await asyncio.to_thread(read_docx_sync, file_path)
    return ""