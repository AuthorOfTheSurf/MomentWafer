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

    def add_activity(self, userid, name, description):
        activity = self.get_activity(userid, name)
        if activity == None:
            activity = Node("Activity", name=name, description=description)
            r = Relationship(self.add_user(userid), "DOES", activity)
            self.graph.create(r)
        return activity

    def get_activity(self, userid, name):
        query = activity_of_user
        params = {
            'userid': userid,
            'activity_name': name
        }
        return self.graph.cypher.execute_one(query, params)

    """
    Annotations look like: ["make:true", "swish:true"]
    """

    def add_moment(self, userid, name, timestamp, annotations):
        moment = Node("Moment", timestamp=timestamp)
        activity = self.get_activity(userid, name)

        if activity != None:
            r = Relationship(moment, "MOMENT_IN", activity)
            self.graph.create(r)
        self.add_annotations(moment, annotations)
        return moment

    def add_annotations(self, moment, annotations):

        d = {}
        for e in annotations:
            e = e.split(":")
            d[e[0]] = e[1]
        annotation = Node("Annotation", **d)
        r = Relationship(annotation, "ANNOTATION_OF", moment)
        self.graph.create_unique(r)
        return annotation, moment


def now():
    return datetime.datetime.now().isoformat()
