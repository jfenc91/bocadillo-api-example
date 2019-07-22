from databases import Database
from bocadillo import provider
from api.settings import SQL_URL, AUTO_CREATE
from asyncio import sleep


# Good place to check sql http://sqlfiddle.com
@provider(scope="app")
async def db() -> Database:
    async with Database("sqlite:///example.db") as db:
        yield db
