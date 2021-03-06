"""
The :mod:`app.core.config` module contains dataclasses 
containing settings information for the api application.
"""
# Author: Chris Dare
# License:
import logging
import os
import secrets
from typing import List, Union

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, validator

log = logging.getLogger(__name__)
load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = os.environ["SERVER_NAME"]
    SERVER_HOST: AnyHttpUrl = os.environ["SERVER_HOST"]
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000",]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = os.environ["BACKEND_CORS_ORIGINS"]
    ZOHO_REDIRECT_URI = os.environ["ZOHO_REDIRECT_URI"]
    ZOHO_CLIENT_ID = os.environ["ZOHO_CLIENT_ID"]
    ZOHO_CLIENT_SECRET = os.environ["ZOHO_CLIENT_SECRET"]
    ZOHO_AUTHORIZATION_CODE = os.environ["ZOHO_AUTHORIZATION_CODE"]
    # ZOHO_OAUTH_SCOPES:str = os.environ["ZOHO_OAUTH_SCOPES"]
    ZOHO_OAUTH_SCOPES:str = "Desk.tickets.ALL,Desk.settings.ALL,Desk.basic.READ,Desk.basic.CREATE"
    ZOHO_ACCESS_TOKEN = os.environ["ZOHO_ACCESS_TOKEN"]
    ZOHO_REFRESH_TOKEN = os.environ["ZOHO_REFRESH_TOKEN"]
    ZOHO_DEFAULT_DEPARTMENT = os.environ["ZOHO_DEFAULT_DEPARTMENT"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[AnyHttpUrl]]) -> Union[List[AnyHttpUrl], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [AnyHttpUrl(i.strip()) for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str

    class Config:
        case_sensitive = True


settings = Settings()