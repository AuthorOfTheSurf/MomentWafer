import datetime
import json
from py2neo import Graph
from py2neo import Node, Relationship

graph = Graph()
try:
    graph.schema.create_uniqueness_constraint("User", "userid")
except:
    pass

activity_of_user = """
    MATCH   (u:User)-[:DOES]->(a:Activity)
    WHERE   u.userid = {userid}
    AND     a.name = {activity_name}
    RETURN  a
"""


def add_user(userid):
    return graph.merge_one("User", "userid", userid)


def add_activity(user, name, description):
    activity = get_activity(user, name)
    if activity == None:
        activity = Node("Activity", name=name, description=description)
        r = Relationship(user, "DOES", activity)
        graph.create(r)
    return activity


def get_activity(user, activityName):
    query = activity_of_user
    params = {
        'userid': user.properties[u'userid'],
        'activity_name': activityName
    }
    return graph.cypher.execute_one(query, params)


def add_instance(activity, timestamp, jsonAnnotations):
    instance = Node("Instance", timestamp=timestamp)
    r = Relationship(instance, "INSTANCE_OF", activity)
    graph.create(r)
    add_annotations(instance, jsonAnnotations)
    return instance


def add_annotations(instance, jsonAnnotations):
    annotation = Node("Annotation", **jsonAnnotations)
    r = Relationship(annotation, "ANNOTATION_OF", instance)
    graph.create_unique(r)
    return annotation


user = add_user("Boat")
activity = add_activity(
    user, "Free-Throw shooting", "Standard free-throws after a short warm-up.")
i1 = add_instance(activity, datetime.datetime.now().isoformat(), {
    "goal": True, "swish": True, "felt-good": True})
i2 = add_instance(activity, datetime.datetime.now().isoformat(), {
    "goal": False, "swish": False, "comm": "Went off off-hand"})
