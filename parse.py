'''
This program is used to show the 
'''

import ast
import os
import json
import sys
from git_repo_relation import generate_structure_json
from git_repo_relation import getGitSourceCode
# from cla import db
sys.path
# sys.path.append('/Users/weishiding/Desktop/Capstone/Spring/llmyacc/llmyacc_supplemental/sample_flask_web_app/flaskr/')
sys.path.append('/Users/weishiding/Desktop/prev/cs138/project138/')
# root_path = "/Users/weishiding/Desktop/Capstone/Spring/llmyacc/llmyacc_supplemental/sample_flask_web_app/flaskr/"

class CallGraphBuilder(ast.NodeVisitor):
    
    def __init__(self):
        # initialize a call_graph dictionary to store functions, classes and imports
        # self.call_graph = {"functions": {}, "classes": {}, "imports": []}
        self.call_graph = {"imports": []}
        # current_scope keep track of context: which function and which class we are inside
        self.current_scope = None

    def visit_Import(self, node):
        '''
        handles 'import module' statements
        These methods add imported module names to the call_graph under imports
        '''
        for alias in node.names:
            self.call_graph["imports"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        '''
        handles 'from ... import ...' statements
        These methods add imported module names to the call_graph under imports
        '''
        self.call_graph["imports"].append(node.module)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        '''
        handles function definitions
        Updates current_scope to the name of the function and adds an entry for 
        this function in the call_graph.
        '''
        func_name = node.name
        self.current_scope = func_name
        # self.call_graph["functions"][func_name] = {"calls": set(), "defined_in_class": None}
        self.generic_visit(node)
        self.current_scope = None

    def visit_ClassDef(self, node):
        '''
        Similar to visit_FunctionDef, but for classes.
        Adds an entry for the class, which will include its methods and instances.
        '''
        class_name = node.name
        self.current_scope = class_name
        # self.call_graph["classes"][class_name] = {"methods": set(), "instances": set()}
        self.generic_visit(node)
        self.current_scope = None

    def visit_Call(self, node):
        '''
        Processes function/method calls.
        Depending on the current_scope, it updates the call_graph with 
        information about what functions or methods are called within a function 
        or class.
        '''
        if self.current_scope:
            called_function = ast.unparse(node.func)
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                # Instance method call
                instance_name = node.func.value.id
                method_name = node.func.attr
                # if self.current_scope in self.call_graph["classes"]:
                #     # Call from within a class
                #     # self.call_graph["classes"][self.current_scope]["methods"].add(method_name)
                #     pass
                # else:
                #     # Call from a function or module level
                #     if instance_name in self.call_graph["classes"]:
                #         # self.call_graph["classes"][instance_name]["methods"].add(method_name)
                #         pass
            # elif self.current_scope in self.call_graph["functions"]:
                # Function call
                # self.call_graph["functions"][self.current_scope]["calls"].add(called_function)
                pass
        self.generic_visit(node)

    def visit_Assign(self, node):
        '''
        Identifies instance creations (e.g., obj = MyClass()).
        Records instances of classes being created, which is useful for 
        understanding object usage.
        '''
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
            # Instance creation
            class_name = node.value.func.id
            # if class_name in self.call_graph["classes"]:
                # for target in node.targets:
                #     if isinstance(target, ast.Name):
                #         instance_name = target.id
                #         self.call_graph["classes"][class_name]["instances"].add(instance_name)
        self.generic_visit(node)

def generate_call_graph_git_code(source_code):  
    tree = ast.parse(source_code)
    builder = CallGraphBuilder()
    builder.visit(tree)
    return builder.call_graph

def generate_call_graph(file_path):
    with open(file_path, "r") as source_file:
        source_code = source_file.read()
    tree = ast.parse(source_code)
    builder = CallGraphBuilder()
    builder.visit(tree)
    return builder.call_graph


def collect_python_imports(source_code_dict, import_relation_dict):
    '''
    @source_code_dict: {"file_name_with_folder_info" : "source_code"}
    ----------------------------------------------------------------------------
    return value
    @file_imports: {"fileName":[number_of_imports, list_of_import_name, file_index]}
    '''
    python_files = list(source_code_dict.keys()) 
    python_files_without_folder = [path.split('/')[-1].replace('.py', '') for path in python_files]
    
    for idx, file_name in enumerate(python_files):
        # with open(file_name + '_git_.json', 'w') as file:
        source_code = source_code_dict[file_name]
        call_graph = generate_call_graph_git_code(source_code)
        imports = call_graph['imports']
        # print(imports)
        clean_imports = list(set(python_files_without_folder).intersection(set(imports)))
        import_relation_dict[file_name] = [len(clean_imports), clean_imports, idx] 
    return import_relation_dict
        
    
def all_github(url):
    print("entering all_github function \n")
    _, source_code_dict = generate_structure_json(url)
    import_relation_dict = {}
    collect_python_imports(source_code_dict, import_relation_dict)
    print("leaving all_github function \n")
    return (source_code_dict, import_relation_dict)

def all():
    ################## List to store the paths of .py files
    python_files = []
    root_path = "/Users/weishiding/Desktop/prev/cs138/project138/"
    # Walk through specified directory
    for root, dirs, files in os.walk(root_path): 
        for file in files:
            # Check if the file ends with .py
            if file.endswith('.py') and not file.startswith('.') and '-checkpoint' not in file:
                # Split the file name and the extension
                file_name_without_extension, _ = os.path.splitext(file)
                # Append the full path to the list
                python_files.append(file_name_without_extension)

    # Printing all .py files found
    # for file in python_files:
    #     print(file)
    # print(python_files)
    ################ generate call graph
    # file_path = "example.py" 
    for file_name in python_files:
        with open(file_name + '.json', 'w') as file:
            # Write the dictionary to the file in JSON format
            
            # print(file_name + ".py")
            call_graph = generate_call_graph(root_path + file_name + ".py")
            imports = call_graph['imports']
            clean_imports = list(set(python_files).intersection(set(imports)))
            print(clean_imports)
            call_graph['imports'] = clean_imports
            json.dump(call_graph, file)
            # print("----cur file is " + file_name + "----\n")
            # print(call_graph)
            # print("----end of file " + file_name + "----\n")
    # print(python_files)
    return python_files

if __name__ == "__main__":
    pass
    # all()
    source_code_dic, _ = all_github("https://api.github.com/repos/Weishi-Ding/AST_LLM/contents/")
    # print(source_code_dic)