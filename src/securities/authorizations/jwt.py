import datetime

from jose import JWTError as JoseJWTError
from jose import jwt as jose_jwt
from loguru import logger
import pydantic
from src.config.manager import settings
from src.models.db.user import User
from src.utilities.exceptions.exceptions import (
    AuthorizationHeaderException,
    EntityAlreadyExistsException,
    InternalServerErrorException,
)




class JWToken(pydantic.BaseModel):
    exp: datetime.datetime
    sub: str

class JWTAccount(pydantic.BaseModel):
    email: pydantic.EmailStr


class JWTGenerator:
    def __init__(self):
        pass

    def _generate_jwt_token(
        self,
        *,
        jwt_data: dict[str, str],
        expires_delta: datetime.timedelta | None = None,
    ) -> str:
        """
        Internal method to generate a JWT token with the provided payload and expiration.
        """
        try:
            to_encode = jwt_data.copy()

            if expires_delta:
                expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
            else:
                expire = datetime.datetime.now(
                    datetime.timezone.utc
                ) + datetime.timedelta(minutes=settings.JWT_MIN)

            to_encode.update(JWToken(exp=expire, sub=settings.JWT_SUBJECT).model_dump())

            return jose_jwt.encode(
                to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
            )

        except Exception as e:
            logger.error(f"Error generating JWT token | {str(e)}")
            raise InternalServerErrorException(
                "Sorry, we cannot authenticate at this moment!"
            )

    def generate_access_token(self, account: User) -> str:
        """
        Generates an access token for the given account.
        """
        try:
            return self._generate_jwt_token(
                jwt_data=JWTAccount(id=account.id, email=account.email).model_dump(),
                expires_delta=datetime.timedelta(
                    minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION_TIME
                ),
            )
        except Exception as e:
            logger.error(
                f"Error generating access token for account: {account.email} | {str(e)}"
            )
            raise InternalServerErrorException("Failed to generate access token.")

    def generate_refresh_token(self, account: User) -> str:
        """
        Generates a refresh token for the given account.
        """
        try:
            return self._generate_jwt_token(
                jwt_data=JWTAccount(id=account.id, email=account.email).model_dump(),
                expires_delta=datetime.timedelta(
                    days=30
                ),  # 30 days for refresh token expiration
            )
        except Exception as e:
            logger.error(
                f"Error generating refresh token for account: {account.email} | {str(e)}"
            )
            raise InternalServerErrorException("Failed to generate refresh token.")

    def retrieve_details_from_token(self, token: str) -> list[str]:
        """
        Decodes the JWT token and retrieves details (like email) from it.
        """
        try:
            payload = jose_jwt.decode(
                token=token,
                key=settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            jwt_account = JWTAccount(email=payload["email"])
            print("jwt_account>>",jwt_account)
        # except JoseJWTError:
        #     logger.error(f"Invalid JWT token: {token}")
        #     raise AuthorizationHeaderException(detail="Invalid token!")
        except Exception as e:
            logger.error(f"Error decoding token | {str(e)}")
            raise InternalServerErrorException()
        print("--------------------")
        return [jwt_account.email]

    def validate_token_expiration(self, token: str) -> bool:
        """
        Validates if the token has expired.
        """
        try:
            payload = self.retrieve_details_from_token(token)
            expiration = datetime.datetime.fromtimestamp(
                payload.get("exp"), datetime.timezone.utc
            )
            if datetime.datetime.now(datetime.timezone.utc) > expiration:
                logger.error(f"Token has expired: {token}")
                raise AuthorizationHeaderException("Token has expired.")
            return True
        except AuthorizationHeaderException:
            raise
        except Exception as e:
            logger.error(f"Error validating token expiration: {str(e)}")
            raise InternalServerErrorException()

    def refresh_access_token(self, refresh_token: str) -> str:
        """
        Generates a new access token using a valid refresh token.
        """
        try:
            payload = self.retrieve_details_from_token(refresh_token)
            email = payload.get("email")
            if not email:
                logger.error(f"Invalid refresh token payload: {refresh_token}")
                raise AuthorizationHeaderException("Invalid refresh token payload.")

            # Reissue a new access token for the user
            return self.generate_access_token(User(email=email))
        except Exception as e:
            logger.error(f"Error refreshing access token: {str(e)}")
            raise AuthorizationHeaderException("Failed to refresh access token.")


def get_jwt_generator() -> JWTGenerator:
    """
    Returns an instance of the JWTGenerator.
    """
    return JWTGenerator()


jwt_generator: JWTGenerator = get_jwt_generator()
