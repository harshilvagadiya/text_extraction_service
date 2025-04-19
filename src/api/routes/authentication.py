from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from src.repository.crud.account import AccountCRUDRepository
from src.utilities.exceptions.exceptions import EntityAlreadyExistsException, EntityDoesNotExistException
import fastapi
from src.api.dependencies.repository import get_repository

router = APIRouter(prefix="/auth", tags=["Authentication"])

class RegisterRequestPayload(BaseModel):
    email: str
    password: str

class AccountInLogin(BaseModel):
    email: str
    password: str

class RegisterApiResponse(BaseModel):
    email: str
    message: str

class LoginApiResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    email: str

@router.post(
    "/signup",
    name="account:signup",
    response_model=RegisterApiResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def signup(
    request: RegisterRequestPayload,
    account_repo: AccountCRUDRepository = Depends(get_repository(repo_type=AccountCRUDRepository)),
) -> RegisterApiResponse:
    try:
        existing_user = await account_repo.find_one(filters={"email": request.email})
        if existing_user:
            raise EntityAlreadyExistsException(f"User with email {request.email} already exists.")

        new_user = await account_repo.create_account(request.email, request.password)

        response_data = {
            "email": new_user.email,
            "message": "Account successfully created.",
        }

        return RegisterApiResponse(**response_data)

    except EntityAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post(
    "/signin",
    name="Login Api",
    response_model=LoginApiResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def signin(
    request: AccountInLogin,
    account_repo: AccountCRUDRepository = Depends(get_repository(repo_type=AccountCRUDRepository)),
) -> LoginApiResponse:
    try:
        user, access_token, refresh_token = await account_repo.authenticate_and_generate_token(
            request.email, request.password
        )

        response_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "email": user.email,
        }

        return LoginApiResponse(**response_data)

    except EntityDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email or password.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
