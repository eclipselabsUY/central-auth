from pydantic_settings import BaseSettings
from pydantic import Field, AnyHttpUrl
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    
    # JWT
    jwt_algorithm: str = Field("RS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(15, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_refresh_token_expire_days: int = Field(7, env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    jwt_issuer: str = Field("egos-auth", env="JWT_ISSUER")
    jwt_audience: str = Field("ego-services.com", env="JWT_AUDIENCE")
    
    # RSA Keys
    jwt_private_key_path: str = Field("./keys/private.pem", env="JWT_PRIVATE_KEY_PATH")
    jwt_public_key_path: str = Field("./keys/public.pem", env="JWT_PUBLIC_KEY_PATH")
    
    # CORS
    allowed_origins: List[AnyHttpUrl] = Field(
        default=["https://ego-services.com", "https://backoffice.ego-services.com"],
        env="ALLOWED_ORIGINS"
    )
    
    # Admin User
    admin_email: str = Field(..., env="ADMIN_EMAIL")
    admin_password: str = Field(..., env="ADMIN_PASSWORD")
    
    # Security
    bcrypt_rounds: int = Field(12, env="BCRYPT_ROUNDS")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

def load_rsa_keys():
    try:
        with open(settings.jwt_private_key_path, "r") as f:
            private_key = f.read()
        with open(settings.jwt_public_key_path, "r") as f:
            public_key = f.read()
        return private_key, public_key
    except FileNotFoundError as e:
        raise Exception(f"RSA key file not found: {e}")