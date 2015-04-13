import falcon
import json
from py2neo import Graph
from service import WaferService


class UserResource:

    def __init__(self, graph):
        self.graph = WaferService(graph)

    def on_post(self, req, resp):
        if "userid" in req.params:
            self.graph.add_user(req.params["userid"])
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_400


def start(env, startResp):
    app = falcon.API()
    graph = Graph()
    users = UserResource(graph)

    app.add_route('/users', users)

    return app(env, startResp)


def test_mode(env, startResp):
    app = falcon.API()
    graph = Graph("http://localhost:8484/db/data")
    users = UserResource(graph)
    
    app.add_route('/users', users)

    return app(env, startResp)