from db import gdb

def postActs(goal, swish, comment):
    a = gdb.nodes.create(goal=goal, swish=swish, comment=comment)
    a.labels.add(":Act")
    b = gdb.nodes.create(goal=not goal, swish=swish, comment=comment)
    b.labels.add(":Act")
    a.relationships.create(":Next", b)

postActs(True, True, "Made it!")
