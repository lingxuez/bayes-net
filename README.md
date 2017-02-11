# bayes-net
A python implemention for checking D-separation and I-equivalence in Bayesian Networks (BN). 

## D-separation
Given a Bayesian Network, and several queries in the form of `X Y | Z`
where `X`, `Y` are two query nodes and `Z` is a set of observed nodes,
`src/dsep.py` checks whether `X` and `Y` are d-separated given `Z` and prints `True` or `False`.

This mainly follows the `"Reachable"` procedure in 
> Koller and Friedman (2009), "Probabilistic Graphical Models: Principles and Techniques" (page 75)

To run the code, try
```
cd src
python dsep.py < ../tests/dsep/test1.in
```


### Input and Output
`dsep.py` takes input from `stdin` as follows:

1. First line: 
    ```
N M Q
    ```
  where `N` and `M` are the number of nodes and edges in the BN, respectively,
  `Q` is the number of D-separation queries that will follow.
  
2. Next `M` lines: 
  ```
  A B
  ```
  Each line denotes a directed edge `A -> B` in the BN graph.
  
3. Next `Q` lines: 
  ```
  A B | C D E ...
  ```
  Each line denotes a query: whether `A` and `B` are d-separated given nodes `C D E ...`
  
The output to `stdout` has `Q` lines, one line per query, 
which is `True` if the two nodes are d-separated or `False` otherwise.

### Example
Run
```
python dsep.py 
```
and provides input from `stdin` as follows:
```
3 2 2
A B
B C
A C | B
C A |
```
This constructs a BN with 3 nodes and 2 edges:
```
A -> B -> C
```
and asks 2 queries:

  (1) Are A and C d-separated given B? (True)
  
  (2) Are C and A d-separated? (False)

So the algorithm will print to `stdout` as
```
True
False
```

## I-equivalence
Given two Bayesian Networks (BNs), `src/iequiv.py` tests whether they are I-equivalent.
Following *Koller and Friedman (2009)*, two BNs are I-equivalent if and only if they have the same skeletons and immoralities.

To run the code, try
```
cd src
python iequv.py < ../tests/iequiv/test1.in
```

### Input and Output

`iequiv.py` takes input from `stdin` as follows:

1. First line: 
  ```
  N1 M1
  ```
  where `N1` and `M1` are the number of nodes and edges, respectively, in the first Bayesian network.

2. Next `M1` lines: 
  ```
  A B
  ```
  Each line denotes a directed edge `A -> B` in the BN graph.

3. Next line: 
  ```
  N2 M2
  ```
   where `N2` and `M2` are the number of nodes and edges, respectively, in the second Bayesian network.

4. Next M2 lines: 
  ```
  A B
  ```
  Each line denotes a directed edge `A -> B` in the BN graph.

The output is printed to `stdout`: `True` if two graphs are I-equivalent or `False` otherwise.


### Example
Run
```
python iequiv.py 
```
and provides input from `stdin` as follows:
```
3 2
A B
B C
3 2
C B
A B
```
This constructs and compares two BNs:
```
A -> B -> C
A -> B <- C
```
and the algorithm prints `False` to `stdout` since they are not I-equivalent.

## Tests
Several simple test cases are provided in `tests/dsep` and `tests/iequiv`. Special thanks to the TAs in [CMU 10-708](http://www.cs.cmu.edu/~epxing/Class/10708-17/) for the test cases. To run the tests:
```
cd src
python dsep.py < ../tests/dsep/test1.in
python iequv.py < ../tests/iequiv/test1.in
```
