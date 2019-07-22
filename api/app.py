from bocadillo import App, configure
import typesystem
from bocadillo import discover_providers
from databases import Database
from api.settings import SQL_URL, AUTO_CREATE


class NumberRequest(typesystem.Schema):
    number = typesystem.Integer()


class UserRequest(typesystem.Schema):
    name = typesystem.String()


discover_providers("api.providerconf")
app = App()
configure(app)


@app.route("/health")
class Health:
    async def get(self, req, res):
        res.json = {"status": 200}
        res.status_code = 200


@app.route("/number_echo")
class NumberEcho:
    async def post(self, req, res):
        number_request = NumberRequest.validate(await req.json())
        res.json = {"number": number_request.number}
        res.status_code = 200


\

@app.route("/user")
class User:
    async def put(self, req, res, db):
        user_request = UserRequest.validate(await req.json())
        query = "INSERT INTO Users (name) VALUES (:name)"
        values = {"name": user_request.name}

        db_res = await db.execute(query=query, values=values)
        res.json = {"users_count": str(db_res)}
        res.status_code = 200

    async def get(self, req, res, db):
        query = "SELECT * FROM Users"
        db_res = await db.fetch_all(query=query)
        res.json = {"users":  [i.name for i in db_res]}
        res.status_code = 200


@app.on("startup")
async def setup():
    if AUTO_CREATE:
        primary_table_check = """CREATE TABLE IF NOT EXISTS Users (name Text)"""
        print("started table")
        async with Database(SQL_URL) as db:
            await db.execute(query=primary_table_check)
        print("created table")
