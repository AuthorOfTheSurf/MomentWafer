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
            resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_400


class ActivityResource:

    def __init__(self, graph):
        self.graph = WaferService(graph)

    def on_post(self, req, resp):
        userid = req.params.get("userid", None)
        name = req.params.get("name", None)
        description = req.params.get("description", "")

        if userid != None and name != None:
            self.graph.add_activity(userid, name, description)
            resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_400

class MomentResource:

    def __init__(self, graph):
        self.graph = WaferService(graph)

    def on_post(self, req, resp):
        userid = req.params.get("userid", None)
        name = req.params.get("name", None)
        timestamp = req.params.get("timestamp", None)
        annotations = req.params.get("annotations", "{}")

        if any(p is None for p in [userid, name, timestamp, annotations]):
            self.graph.add_moment(userid, name, timestamp, annotations)
            resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_400


def build_app(graph):
    app = falcon.API()
    graph = graph

    app.add_route('/users', UserResource(graph))
    app.add_route('/activities', ActivityResource(graph))
    app.add_route('/moments', MomentResource(graph))

    return app


def start(env, startResp):
    app = build_app(app, Graph())
    return app(env, startResp)


def test_mode(env, startResp):
    app = build_app(Graph("http://localhost:8484/db/data"))
    return app(env, startResp)
