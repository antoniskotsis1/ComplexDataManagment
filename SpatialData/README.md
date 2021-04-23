# SECOND PROJECT
***
##Part 1: Rtree throw bulk loading
>### r_tree.py
> usage: r_tree.py [-h] coords_file offset_file
>####positional arguments:
> coords_file  file containing polygon's coordinates
> 
>offset_file  file containing coordinate offsets
>####optional arguments:
>  -h, --help   show this help message and exit


After opening the files given to the command line,
the algorithm calculates all the minimum bounding
rectangles (MRBs) for each polygon. After each MBR is calculated, we transform
it's center and calculate **the z-order curve** in order
to sort the created MBRs in the best possible way.

Having created all the MBRs for each rectangle
in the given collection, it's time to bulk load data in the
R-tree. This was achieved by using recursion. First, all leaf nodes
are built and then all the other levels recursively
until the root. 

**Limitations of Rtree:**

* Minimum node capacity = 8
* Maximum node capacity = 20
* Root is excluded and can have 2 to 20 children

**Rtree structure:**
* Each non leaf node has the form of [id, MBR]
where MBR is the MBR of all records of the node and
  id is the identifier of the node.
    
* Leaf nodes have the form of [id, MBR] where MBR is
the MBR of the object with identifier id.
  
**Output:**
* Rtree.txt is the output file of the program and
contains the generated tree.
  
* Each line has the form
  [isnonleaf, node-id, [[id1, MBR1], [id2, MBR2], …, [idn, MBRn]]]
where isnonleaf = 1 if node is leaf otherwise 0
  
* In each record, id is either node-id (if record points
  to a node) or onject-id if record points to an object.
  