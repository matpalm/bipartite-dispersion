
consider a bipartite user/item graph

<img src="http://github.com/matpalm/bipartite-dispersion/raw/master/fig1.png"/>

# taking 2 steps

starting at i1 with variable P=1.0 
take one step; split P across two users; u1 P=0.5 and u2 P=0.5
take another step; split P further; all of u1's P goes back to i1 whereas u2's P is spread evenly between i1, i2, i3 
results in i1 P=0.5+0.16=0.66, i2=0.16 i3=0.16

this dispersion of P calculates the following... 

starting at i1, talking two random steps what is the probability we end up at itemN?  P(i1) = 0.66, P(i2) = 0.16, P(i3) = 0.16

note how these are different depending on the starting point..

starting at i2, talking two random steps what is the probability we end up at itemN?  P(i1) = 0.33, P(i2) = 0.33, P(i3) = 0.33

starting at i3, talking two random steps what is the probability we end up at itemN?  P(i1) = 0.16, P(i2) = 0.16, P(i3) = 0.66

## taking 2N steps (large N)

if we walk forever we get to a steady state; P(i1) = 0.4, P(i2) = 0.2, P(i3) = 0.4 (and because this is in the limit we get this no matter where we start)

## somewhere in between

we saw how 2-steps gives a large difference between items, but doesnt walk the graph very far...

and 2N-steps gives no difference between items but provides a better representation of the spread over the graph...

as an inbetween we introduce a form of "trace" where we deposit some fraction (BETA) of our "probability" at each item we visit (ie every 2 steps)

for BETA=1.0 (ie deposit everything) the trace amounts calculating the 2-step probabilities. ie start with P=1.0; move to user; move to item; deposit 100%; stop
 
    cat eg_graph.tsv | ./dispersion.py 1.0
    20  {"20": 0.666, "21": 0.166, "22": 0.166}
    21  {"20": 0.333, "21": 0.333, "22": 0.333}
    22  {"20": 0.166, "21": 0.166, "22": 0.666}
    
for BETA=0.001 (ie deposit a small amount) the trace amounts are approximating the probability of where we would end up after after a walk of 2N steps (for large N)

    cat eg_graph.tsv | ./dispersion.py 0.0001
    20  {"20": 0.25344, "21": 0.12642, "22": 0.25244}
    21  {"20": 0.25284, "21": 0.12662, "22": 0.25284}
    22  {"20": 0.25244, "21": 0.12642, "22": 0.25344}

a more interesting examples lies somewhere in between, say BETA=0.5, where we deposit some probability at "near" items but allow some other fraction to disperse further

    cat eg_graph.tsv | ./dispersion.py 0.5
    20  {"20": 0.57575, "21": 0.18181, "22": 0.24241}
    21  {"20": 0.36363, "21": 0.27272, "22": 0.36363}
    22  {"20": 0.24241, "21": 0.18181, "22": 0.57575}

these traces can then used as features for an item/item comparison matrix where, say, sim(i1,i2) = some f(of their rows)

       20    21    22
    20 0.666 0.166 0.166
    21 0.333 0.333 0.333
    22 0.166 0.166 0.666


