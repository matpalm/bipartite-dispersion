#!/usr/bin/env python
import sys
from collections import defaultdict
import json

# how much to take each iteration, 0.0001 => run to convergence, 1.0 => run one iteration
BETA = float(sys.argv[1])      
# stopping parameter, all amount values must be over this to continue iterating
EPSILON = 1e-5  


def disperse(from_nodes, to_nodes):
    global edges
    for node, amount in from_nodes.iteritems():
        adjacent_nodes = edges[node]
        disperse_amount = amount / len(adjacent_nodes)
        for adjacent_node in adjacent_nodes:
            to_nodes[adjacent_node] += disperse_amount
    from_nodes.clear()


# read in user -> item edges
edges = defaultdict(list)
items = set()
for line in sys.stdin:
    user, item = map(int, line.strip().split("\t"))
    edges[user].append(item)
    edges[item].append(user)
    items.add(item)

# run for each item
for start in items:
    # keep track of dispersal on either side
    items = defaultdict(float)
    users = defaultdict(float)
    # and the trace
    trace = defaultdict(float)

    # bootstrap
    items[start] = 1.0

    # run to convergence, but at most 1000 iterations
    for i in range(1000):

        # disperse from items to users and back to items again
        disperse(items, users)
        disperse(users, items)

        # keep a percentage of the value
        # and check stopping condition
        at_least_one_value_over_epsilon = False
        for item, amount in items.iteritems():
            to_take = amount * BETA
            trace[item] += to_take
            remaining = amount - to_take
            items[item] = remaining
            at_least_one_value_over_epsilon |= remaining > EPSILON

        # are we done?
        if not at_least_one_value_over_epsilon:
            break

    print "%s\t%s" % (start, json.dumps(trace))
     


