from bocadillo import App, configure
import typesystem


class NumberRequest(typesystem.Schema):
    number = typesystem.Integer()


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
