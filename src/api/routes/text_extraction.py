from fastapi import Depends, HTTPException, Request
from jose import JWTError
from src.securities.authorizations.jwt import jwt_generator
from src.models.db.user import User
from src.utilities.exceptions.exceptions import AuthorizationHeaderException
import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.db.user import Document
from src.utilities.common.text_extraction import extract_text_from_pdf, extract_text_from_docx, extract_text_from_doc, download_file_from_url
from fastapi.responses import JSONResponse
from src.api.dependencies.session import get_async_session
from sqlalchemy.future import select
from urllib.parse import urlparse
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from src.utilities.email.mailer import Mailer, get_mailer

router = APIRouter(prefix="/documents", tags=["Documents"])

class FilePathOrUrlRequest(BaseModel):
    file_paths_or_urls: List[str]  


class ExtractionResultResponse(BaseModel):
    task_id: int
    status: str
    extracted_text: str


def get_user_from_token(request: Request) -> User:
    try:
        token = request.headers.get("Authorization")
        if token is None:
            raise HTTPException(status_code=401, detail="Authorization token is missing.")
        
        if token.startswith("Bearer "):
            token = token[7:]

        payload = jwt_generator.retrieve_details_from_token(token)
        if len(payload) < 1:
            raise HTTPException(status_code=401, detail="Invalid token payload.")
        email = payload
        user = User(email=email[0])

        return user

    except JWTError:
        raise AuthorizationHeaderException(detail="Invalid or expired token.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/extract", response_model=List[ExtractionResultResponse])
async def extract_text_from_documents(
    request: FilePathOrUrlRequest,\
    user: User = Depends(get_user_from_token),
    async_session: AsyncSession = Depends(get_async_session),
    mailer: Mailer = Depends(get_mailer),
):
    try:
        user_from_db = await async_session.execute(select(User).filter(User.email == user.email))
        user_record = user_from_db.scalar_one_or_none()
        if not user_record:
            raise HTTPException(status_code=404, detail="User not found.")
        user_id = user_record.id

        extraction_results = []

        for file_path_or_url in request.file_paths_or_urls:
            print(">>>>>>>>>",file_path_or_url)
            file_path = None
            extracted_text = None
            file_format = None

            if file_path_or_url:
                # If it's a URL, we download the file
                if urlparse(file_path_or_url).scheme in ["http", "https", "ftp"]:  # Check if it's a valid URL
                    file_path = download_file_from_url(file_path_or_url, "temp/")
                    file_format = file_path.split('.')[-1].lower()
                # Else, we assume it's a local file path
                elif os.path.exists(file_path_or_url):
                    file_path = file_path_or_url
                    file_format = file_path.split('.')[-1].lower()
                else:
                    raise HTTPException(status_code=400, detail="Invalid file path or URL.")

            if not file_format:
                raise HTTPException(status_code=400, detail="Unable to detect file format.")

            if file_format == "pdf":
                extracted_text = extract_text_from_pdf(file_path)
            elif file_format == "docx":
                extracted_text = extract_text_from_docx(file_path)
            elif file_format == "doc":
                extracted_text = extract_text_from_doc(file_path)
            else:
                print("file_format - ",file_format)
                response = requests.get(file_path_or_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                extracted_text = soup.get_text()

            document = Document(
                file_path=file_path,
                extracted_text=extracted_text,
                extraction_status="completed",
                user_id=user_id,
            )
            async_session.add(document)
            await async_session.commit()
            await async_session.refresh(document)

            extraction_results.append(
                ExtractionResultResponse(
                    task_id=document.id,
                    status="completed",
                    extracted_text=extracted_text,
                )
            )

        subject = "Document Extraction Completed"
        body = f"Dear {user.email},\n\nYour document extraction has been successfully completed.\n\Thanks & regards"
        await mailer.send_email(to_email=user.email, subject=subject, body=body)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=[result.dict() for result in extraction_results]
        )

    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")
