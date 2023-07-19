from enum import Enum

class Settings(str, Enum):
    authjwt_secret_key = "4a7f3f4426b8be157b6b105aa1ae543a3a303b4497d7ffaa5a5b0c2a6465058e"
    #authjwt_refresh_secret_key: str = "c4aa0840ddcb425ab5bd6ca58d1a98da9da9d5c7d59435386f004a218ccf6569"
    authjwt_algorithm = "HS256"
    #authjwt_access_token_expires = 15
    #authjwt_refresh_token_expires: int = 60 * 2