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
import copy

class Node(object):
    """
    Node in a directed graph
    """
    def __init__(self, name=""):
        """
        Construct a new node, and initialize the list of parents and children.
        Each parent/child is represented by a (key, value) pair in dictionary, 
        where key is the parent/child's name, and value is an Node object.

        Args:
            name: a unique string identifier.
        """
        self.name = name
        self.parents = dict()
        self.children = dict()

    def add_parent(self, parent):
        """
        Args:
            parent: an Node object.
        """
        if not isinstance(parent, Node):
            raise ValueError("Parent must be an instance of Node class.")
        pname = parent.name
        self.parents[pname] = parent

    def add_child(self, child):
        """
        Args:
            child: an Node object.
        """
        if not isinstance(child, Node):
            raise ValueError("Parent must be an instance of Node class.")
        cname = child.name
        self.children[cname] = child


class BN(object):
    """
    Bayesian Network
    """
    def __init__(self):
        """
        Initialize the list of nodes in the graph.
        Each node is represented by a (key, value) pair in dictionary, 
        where key is the node's name, and value is an Node object
        """
        self.nodes = dict()

    def add_edge(self, edge):
        """
        Add a directed edge to the graph.
        
        Args:
            edge: a tuple (A, B) representing a directed edge A-->B,
                where A, B are two strings representing the nodes' names
        """
        (pname, cname) = edge

        ## construct a new node if it doesn't exist
        if pname not in self.nodes:
            self.nodes[pname] = Node(name=pname)
        if cname not in self.nodes:
            self.nodes[cname] = Node(name=cname)

        ## add edge
        parent = self.nodes.get(pname)
        child = self.nodes.get(cname) 
        parent.add_child(child)
        child.add_parent(parent)

    def print_graph(self):
        """
        Visualize the current graph.
        """
        print "Bayes Network:"
        for nname, node in self.nodes.iteritems():
            print "\tNode " + nname
            print "\t\tParents: " + str(node.parents.keys())
            print "\t\tChildren: " + str(node.children.keys())

    def find_obs_anc(self, observed):
        """
        Traverse the graph, find all nodes that have observed descendants.

        Args:
            observed: a list of strings, names of the observed nodes. 

        Returns:
            a list of strings for the nodes' names for all nodes 
            with observed descendants.
        """
        visit_nodes = copy.copy(observed) ## nodes to visit
        obs_anc = set() ## observed nodes and their ancestors

        ## repeatedly visit the nodes' parents
        while len(visit_nodes) > 0:
            next_node = self.nodes[visit_nodes.pop()]
            ## add its' parents
            for parent in next_node.parents:
                obs_anc.add(parent)

        return obs_anc

    def is_dsep(self, start, end, observed):
        """
        Check whether start and end are d-separated given observed.
        This algorithm mainly follows the "Reachable" procedure in 
        Koller and Friedman (2009), 
        "Probabilistic Graphical Models: Principles and Techniques", page 75.

        Args:
            start: a string, name of the first query node
            end: a string, name of the second query node
            observed: a list of strings, names of the observed nodes. 
        """

        ## all nodes having observed descendants.
        obs_anc = self.find_obs_anc(observed)

        ## Try all active paths starting from the node "start".
        ## If any of the paths reaches the node "end", 
        ## then "start" and "end" are *not* d-separated.
        ## In order to deal with v-structures, 
        ## we need to keep track of the direction of traversal:
        ## "up" if traveled from child to parent, and "down" otherwise.
        via_nodes = [(start, "up")]
        visited = set() ## keep track of visited nodes to avoid cyclic paths

        while len(via_nodes) > 0: 
            (nname, direction) = via_nodes.pop()
            node = self.nodes[nname]

            ## skip visited nodes
            if (nname, direction) not in visited:
                visited.add((nname, direction)) 

                ## if reaches the node "end", then it is not d-separated
                if nname not in observed and nname == end:
                    return False

                ## if traversing from children, then it won't be a v-structure
                ## the path is active as long as the current node is unobserved
                if direction == "up" and nname not in observed:
                    for parent in node.parents:
                        via_nodes.append((parent, "up"))
                    for child in node.children:
                        via_nodes.append((child, "down"))
                ## if traversing from parents, then need to check v-structure
                elif direction == "down":
                    ## path to children is always active
                    if nname not in observed: 
                        for child in node.children:
                            via_nodes.append((child, "down"))
                    ## path to parent forms a v-structure
                    if nname in observed or nname in obs_anc: 
                        for parent in node.parents:
                            via_nodes.append((parent, "up"))
        return True


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
        
    ## for debugging: visualize the graph
    # myBN.print_graph()

    ########################
    ## Check D-separation
    ########################
    ## queries
    for (start, end, observed) in queries:
        print myBN.is_dsep(start, end, observed)























