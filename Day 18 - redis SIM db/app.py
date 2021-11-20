#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource

from parsim import get_all_data

app = Flask(__name__)
api = Api(app)


class Sim(Resource):
    def get(self):
        return get_all_data(), 200  # return data and 200 OK code


# endpoint = str(os.system("echo sim | md5sum | cut -d' ' -f1 | xargs echo -n"))
endpoint = "f1e192b277bc7309d5cf2268f31148600"

api.add_resource(Sim, f"/{endpoint}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=31011)
    # serve(app, host='0.0.0.0', port=31011)
