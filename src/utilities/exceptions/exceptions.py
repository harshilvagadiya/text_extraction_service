from fastapi import HTTPException, status


class InternalServerErrorException(HTTPException):
    def __init__(
        self,
        detail: str = "There was a problem processing your request. Please try again later.",
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class EntityAlreadyExistsException(HTTPException):
    def __init__(self, entity_name: str = "Entity"):
        detail = f"{entity_name} already exists."
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class EntityDoesNotExistException(HTTPException):
    def __init__(self, detail: str = "Entity does not exist!"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class AuthorizationHeaderException(HTTPException):
    def __init__(self, detail: str = "Authorization Failed!"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
