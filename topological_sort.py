def topological_sort(dependencies):
    visited = set()  # Keep track of visited nodes
    stack = []  # Use a stack to keep track of the topological order
    cycle_detected = set()  # Keep track of nodes involved in cycles
    
    # Helper function for DFS
    def dfs(node):
        if node in cycle_detected:
            return False  # Cycle detected, no need to continue down this path
        if node in visited:
            return True  # Already visited this node, skip
        visited.add(node)
        
        # Recur for all the dependencies of node
        for neighbour in dependencies.get(node, [])[1]:
            if not dfs(neighbour):
                cycle_detected.add(node)  # Mark this node as part of a cycle
        
        stack.insert(0, node)  # Add this node to the topological order
        return True
    
    # Perform DFS from each node
    for node in dependencies:
        if node not in visited and node not in cycle_detected:
            dfs(node)
    
    # Return the topological order, excluding nodes marked as part of cycles
    return [node for node in stack if node not in cycle_detected]

# Example usage
dependencies = {'one': [2, ['two', 'three'], 0], 'two': [1, ['one'], 1], 'three': [2, ['four', 'five'], 2], 'four': [1, ['two'], 3], 'five' : [0, [], 4]}
print(topological_sort(dependencies))