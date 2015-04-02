import datetime
import json
from py2neo import Graph
from py2neo import Node, Relationship

graph = Graph()
try:
    graph.schema.create_uniqueness_constraint("User", "userid")
except:
	pass

single_activity_of_user = """
    MATCH   (u:User)-[:DOES]->(a:Activity)
    WHERE   u.userid = {userid}
    AND     a.name = {activity_name}
    RETURN  a
"""

def addUser(userid):
	return graph.merge_one("User", "userid", userid)

def addActivity(user, name, description):
	if activitiesWithSameName(user, name) == None:
		activity = Node("Activity", name=name, description=description)
		r = Relationship(user, "DOES", activity)
		graph.create(r)
		return (activity, r)
	else:
		return None

def activitiesWithSameName(user, name):
	(query, params) = single_activity_of_user, {
		'userid': user.properties[u'userid'],
		'activity_name': name
	}
	return graph.cypher.execute_one(query, params)

# TODO: add check for timestamp within activity range when that is available
def addInstance(activity, timestamp, jsonAnnotations):
	instance = Node("Instance", timestamp=timestamp)
	r = Relationship(instance, "INSTANCE_OF", activity)
	graph.create(r)
	return (instance, r, addAnnotations(instance, jsonAnnotations))

def addAnnotations(instance, jsonAnnotations):
	annotation = Node("Annotation", **jsonAnnotations)
	r = Relationship(annotation, "ANNOTATION_OF", instance)
	graph.create_unique(r)
	return (annotation, r)

user = addUser("Boat")
activity = addActivity(user, "Free-Throw shooting", "Standard free-throws after a short warm-up.")[0]
i1 = addInstance(activity, datetime.datetime.now().isoformat(), {"goal": True, "swish": True, "felt-good": True})[0]
i2 = addInstance(activity, datetime.datetime.now().isoformat(), {"goal": False, "swish": False, "comm": "Went off off-hand"})[0]
