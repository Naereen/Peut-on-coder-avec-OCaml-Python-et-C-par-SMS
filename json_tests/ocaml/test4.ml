type 'a btree = Leaf of 'a | Node of ('a btree * 'a btree);;
let rec sum (tree : int btree) = match tree with | Leaf i -> i | Node(left, right) -> (sum left) + (sum right);;
print_int(sum( Node(Leaf 30, Node(Leaf 10, Leaf 2)) ));;
