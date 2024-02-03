import ast
import os

class DependencyGraphBuilder(ast.NodeVisitor):
    def __init__(self, file_path, file_to_module_map):
        self.file_path = file_path
        self.file_to_module_map = file_to_module_map
        self.dependencies = set()

    def visit_Import(self, node):
        for alias in node.names:
            module_path = self.resolve_module_to_file(alias.name)
            if module_path:
                self.dependencies.add(module_path)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module_path = self.resolve_module_to_file(node.module)
        if module_path:
            self.dependencies.add(module_path)
        self.generic_visit(node)

    def resolve_module_to_file(self, module_name):
        # Simple resolution from module name to file path
        # This needs to be more sophisticated to handle various import scenarios
        file_name = module_name.replace('.', os.sep) + '.py'
        for base_path, module_path in self.file_to_module_map.items():
            if file_name.endswith(module_path):
                return os.path.join(base_path, file_name)
        return None


def build_dependency_graph(directory):
    # Map from file paths to module import paths
    file_to_module_map = {}
    
    # Walk the directory and build a map of file path to module name
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                module_path = os.path.join(root, file)
                module_name = module_path.replace(directory, '').replace(os.sep, '.')
                file_to_module_map[root] = module_name.strip(".")

    # Dictionary to hold the dependency graph
    dependency_graph = {}

    # Parse each file and build the dependency graph
    for root, module_name in file_to_module_map.items():
        for file in os.listdir(root):
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    source_code = f.read()
                tree = ast.parse(source_code)
                visitor = DependencyGraphBuilder(file_path, file_to_module_map)
                visitor.visit(tree)
                dependency_graph[file_path] = visitor.dependencies

    return dependency_graph


# Example usage - Replace 'your_code_directory' with the path to your code repo
dependency_tree = build_dependency_graph('your_code_directory')
