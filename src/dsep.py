####################################################
## D-separation in Bayesian Networks
## Lingxue Zhu
## 2017/02/05
####################################################
##
## Description:
##
## Given a Bayesian Network, and several queries in the form of X Y | Z
## where X, Y are two query nodes, Z is a set of observed nodes,
## the algorithm checks whether X and Y are d-separated given Z.
##
## Reference: Koller and Friedman (2009), 
## Probabilistic Graphical Models: Principles and Techniques
##
####################################################
##
## Input from stdin:
##
## 1. First line contains 3 numbers: N M Q
##    where N and M are the number of nodes and edges in the BN, respectively,
##    Q is the number of D-separation queries that will follow.
## 2. Next M lines: A B
##    Each line denotes a directed edge A --> B in the BN graph.
## 3. Next Q lines: A B | C D E...
##    Each line denotes a query: whether A and B are d-separated given C D E...
##
####################################################
##
## Output to stdout:
##
## Q lines, one line per query, 
## prints "True" if the nodes are d-separated or "False" otherwise.
##
####################################################
##
## Example:
##
## Input from stdin:
## 3 2 2
## A B
## B C
## A C | B
## C A |
##
## Output to stdout:
## True
## False
##
## This constructs a BN with 3 nodes and 2 edges:
##    A --> B --> C
## and answers 2 queries:
## (1) Are A and C d-separated given B? (True)
## (2) Are C and A d-separated? (False)
##
## See ../tests/dsep/* for more examples. To run the tests:
##
## $ python dsep.py < ../tests/dsep/test1.in
## 
####################################################

import sys
from BN import *

if __name__ == "__main__":
    ########################
    ## Read from stdin
    ########################
    ## first line: number of nodes, number of edges, number of queries. 
    header = sys.stdin.readline().rstrip().split(" ")
    if len(header) != 3:
        print("First line must specify number of nodes, edges and queries.")
        sys.exit(1)
    (nnode, nedge, nquery) = map(int, header)

    ## edges
    edges = []
    for line in xrange(nedge):
        edge = sys.stdin.readline().rstrip().split(" ")
        edges += [edge]

    ## queries
    queries = []
    for line in xrange(nquery):
        query = sys.stdin.readline().rstrip().split(" ")
        (start, end, observed) = (query[0], query[1], query[3:])
        queries += [(start, end, observed)]

    ########################
    ## Build Graph
    ########################
    myBN = BN()
    for edge in edges:
        myBN.add_edge(edge)

    ########################
    ## Check D-separation
    ########################
    for (start, end, observed) in queries:
        print myBN.is_dsep(start, end, observed)

