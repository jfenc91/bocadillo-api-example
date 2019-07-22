from starlette.config import Config

config = Config(".env")

PROVIDER_MODULES = ["api.providerconf"]
SQL_URL = config("SQL_URL", default="sqlite:///example.db")

AUTO_CREATE = config("AUTO_CREATE", default=True)