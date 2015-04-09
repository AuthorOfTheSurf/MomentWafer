import datetime
import json
from py2neo import Graph
from py2neo import Node, Relationship

activity_of_user = """
    MATCH   (u:User)-[:DOES]->(a:Activity)
    WHERE   u.userid = {userid}
    AND     a.name = {activity_name}
    RETURN  a
"""


class WaferService:

    """Service layer providing connection to Neo4j"""

    def __init__(self, graph):
        self.graph = graph

    def add_user(self, userid):
        return self.graph.merge_one("User", "userid", userid)

    def add_activity(self, user, name, description):
        activity = self.get_activity(user, name)
        if activity == None:
            activity = Node("Activity", name=name, description=description)
            r = Relationship(user, "DOES", activity)
            self.graph.create(r)
        return activity

    def get_activity(self, user, name):
        query = activity_of_user
        params = {
            'userid': user.properties[u'userid'],
            'activity_name': name
        }
        return self.graph.cypher.execute_one(query, params)

    def add_moment(self, activity, timestamp=None, jsonAnnotations={}):
        moment = Node("Moment", timestamp=timestamp)
        r = Relationship(moment, "MOMENT_IN", activity)
        self.graph.create(r)
        self.add_annotations(moment, jsonAnnotations)
        return moment

    def add_annotations(self, moment, jsonAnnotations):
        annotation = Node("Annotation", **jsonAnnotations)
        r = Relationship(annotation, "ANNOTATION_OF", moment)
        self.graph.create_unique(r)
        return annotation, moment


def now():
    return datetime.datetime.now().isoformat()


if __name__ == "__main__":
    svc = WaferService(Graph())
    user = svc.add_user("Boat")
    activity = svc.add_activity(
        user, "Free-Throw shooting",
        "Standard free-throws after a short warm-up.")
    annotations = {
        "goal": True,
        "swish": True,
        "felt-good": True
    }
    i1 = svc.add_instance(activity, now(), annotations)
    annotations = {
        "goal": False,
        "swish": False,
        "comm": "Went off off-hand"
    }
    i2 = svc.add_instance(activity, now(), annotations)
