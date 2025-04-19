import datetime

from src.config.manager import settings

class JWTGenerator:
    def __init__(self):
        pass
    
    def _generate_jwt_token(
        self,
        *,
        jwt_data: dict[str, str],
        expires_delta: datetime.timedelta | None = None,
    ) -> str:
        to_encode = jwt_data.copy()
        
        if expires_delta:
            expire = datetime.datetime.now() + expires_delta
        else:
            expire = datetime.datetime.now() + datetime.timedelta(minutes=settings.JWT_MIN)