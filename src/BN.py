####################################################
## Bayesian Networks
## Lingxue Zhu
## 2017/02/05
####################################################

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

    def get_skeleton(self):
        """
        Find the skeleton of the Bayesian Network.
        Returns: 
            a set of undirected edges (represented by tuples) in the skeleton. 
        """
        skeleton = set()
        for (nname, node) in self.nodes.iteritems():
            ## add edges to skeleton
            for parent in node.parents:
                if (nname, parent) not in skeleton and (parent, nname) not in skeleton:
                    skeleton.add((nname, parent))
            for child in node.parents:
                if (nname, child) not in skeleton and (child, nname) not in skeleton:
                    skeleton.add((nname, child))

        return skeleton

    def get_skeleton_immor(self):
        """
        Find the skeleton and immoralities in the graph.
        Returns:
            a tuple, the first element is a set of edges in the skeleton,
            and the second element is a set of parent-pairs that have common child(ren)
            but are not connected.
        """
        ## skeleton: a list of edges (undirected)
        skeleton = self.get_skeleton()
        ## find immoralities
        immoral = set()
        for (nname, node) in self.nodes.iteritems():
            ## check each pair of parents
            if len(node.parents) > 1:
                parents = node.parents.keys()
                for i1 in xrange(len(parents)-1):
                    for i2 in xrange(i1+1, len(parents)):
                        p1, p2 = parents[i1], parents[i2]
                        ## parents are immoral if they are not connected
                        if ((p1, p2) not in skeleton and (p2, p1) not in skeleton 
                            and (p1, p2) not in immoral and (p2, p1) not in immoral):
                            immoral.add((p1, p2))

        return (skeleton, immoral)
