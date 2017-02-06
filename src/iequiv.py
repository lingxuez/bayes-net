####################################################
## I-equivalence of Bayesian Networks
## Lingxue Zhu
## 2017/02/05
####################################################
##
## Description:
##
## Given two Bayesian Networks, the algorithm tests whether
## they are I-equivalent.
##
## Reference: Koller and Friedman (2009), 
## Probabilistic Graphical Models: Principles and Techniques
##
####################################################
##
## Input from stdin:
##
## 1. First line: N1 M1
##    where N1 and M1 are the number of nodes and edges, respectively,
##    in the first Bayesian network.
## 2. Next M1 lines: A B
##    Each line denotes a directed edge A --> B in the BN graph.
## 3. Next line: N2 M2
##    where N2 and M2 are the number of nodes and edges, respectively,
##    in the second Bayesian network.
## 4. Next M2 lines: A B
##    Each line denotes a directed edge A --> B in the BN graph.
##
####################################################
##
## Output to stdout:
##
## Prints "True" if two graphs are I-equivalent or "False" otherwise.
##
####################################################
##
## Example:
##
## Input from stdin:
## 3 2
## A B
## B C
## 3 2
## C B
## A B
##
## Output to stdout:
## False
##
## This compares two BNs:
## (1) A --> B --> C
## (2) A --> B <-- C
## and prints "False" since they are not I-equivalent.
##
## See ../tests/iequiv/* for more examples. To run the tests:
##
## $ python dsep.py < ../tests/iequiv/test1.in
## 
####################################################

import sys
from BN import *

def check_iequv(bn1, bn2):
    """
    Check whether two Bayesian Networks are I-equivalent.
    Two BNs are I-equivalent if and only if they have the same
    skeletons and immoralities

    Args:
        bn1: an instance of BN class, the first BN.
        bn2: an instance of BN class, the second BN.

    Returns:
        True if bn1 and bn2 are I-equivalent, and False otherwise.
    """
    ## skeletons and immoralities
    (ske1, immor1) = bn1.get_skeleton_immor()
    (ske2, immor2) = bn2.get_skeleton_immor()

    ## comparison. 
    if len(ske1) != len(ske2) or len(immor1) != len(immor2):
        return False

    ## Note that the edges are undirected so we need to check both ordering
    for (n1, n2) in immor1:
        if (n1, n2) not in immor2 and (n2, n1) not in immor2:
            return False
    for (n1, n2) in ske1:
        if (n1, n2) not in ske2 and (n2, n1) not in ske2:
            return False
    return True


if __name__ == "__main__":
    ########################
    ## Read from stdin
    ########################
    ## First BN
    ## header line: number of nodes and edges for the first BN. 
    header1 = sys.stdin.readline().rstrip().split(" ")
    (nnode1, nedge1) = map(int, header1)
    ## edges
    edges1 = []
    for line in xrange(nedge1):
        edge = sys.stdin.readline().rstrip().split(" ")
        edges1 += [edge]

    ## Second BN
    ## header line: number of nodes and edges for the second BN. 
    header2 = sys.stdin.readline().rstrip().split(" ")
    (nnode2, nedge2) = map(int, header2)
    ## edges
    edges2 = []
    for line in xrange(nedge2):
        edge = sys.stdin.readline().rstrip().split(" ")
        edges2 += [edge]

    ########################
    ## Build Graph
    ########################
    firstBN = BN()
    for edge in edges1:
        firstBN.add_edge(edge)

    secondBN = BN()
    for edge in edges2:
        secondBN.add_edge(edge)

    ########################
    ## Check I-equivalence
    ########################
    print check_iequv (firstBN, secondBN)
