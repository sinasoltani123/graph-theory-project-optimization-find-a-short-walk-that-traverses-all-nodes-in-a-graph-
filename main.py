import random

adjacency_matrix = {}

with open("graph-dataset.edges", "r") as file:
    for line in file:
        u, v = map(int, line.strip().split(","))
        if u != v:
            if u not in adjacency_matrix:
                adjacency_matrix[u] = []
            if v not in adjacency_matrix:
                adjacency_matrix[v] = []
            adjacency_matrix[u].append(v)
            adjacency_matrix[v].append(u)

#first we have not seen any node.initialize False
seen = dict.fromkeys(range(14113), False)

#check if we have seen all nodes or not
def finished():
    return not any(value == False for value in seen.values())

#check if if the walk is valid or not
def check_walk(sw):
    if not finished():
        return False
    for i in range(len(sw)-1):
        vertex1 = sw[i]
        vertex2 = sw[i+1]
        adjacent_vertices = adjacency_matrix[vertex1]
        if vertex2 not in adjacent_vertices:
            print("Error!")
            return False
    return True

#iterative dfs
def new_dfs(G, start, seen):
    stack = [start]
    walk = [start]
    seen[start] =True

    while stack:

        node = stack[-1]

        new_node = None

        random.Random(1).shuffle(G[node])  #pick a random neighbor that we have not seen yet

        for x in G[node]:
            if not seen[x]:
                new_node = x
                break

        if new_node == None:
            if finished():  #if all nodes have been seen return
                return walk
            # go up in the search tree(parent)
            stack.pop()
            if len(stack) != 0:
                walk.append(stack[-1])
        else:
            walk.append(new_node)
            stack.append(new_node)
            seen[new_node] = True
    return walk


#finding a shorter walk with a different starting node
#5929 below is gained by experienting(yet found) but you can change it and change the loop to see a different result
best = new_dfs(adjacency_matrix,5929,seen)
min = len(best)
for i in range(20):
    random_start = random.randrange(0,14113)
    seen = dict.fromkeys(range(14113), False)
    walk = new_dfs(adjacency_matrix,random_start,seen)
    if len(walk)< min:
        best = walk
        min = len(best)

    a= (len(walk))
    print(f"random starting point = {random_start} : len(best) = {len(best)} , len(walk) = {len(walk)}")


print(best)
#validate the new walk
print("\nIs the new walk with a different start node valid?",check_walk(best), "\nthe size of this walk is = " , len(best))

#write to file
with open('output.txt', 'w') as fp:
    for item in best:
        fp.write("%s " % item)
