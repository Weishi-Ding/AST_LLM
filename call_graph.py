import networkx as nx
import matplotlib.pyplot as plt

# Assuming 'data' is the dictionary you obtained from AST parsing
data = {'functions': {'login_required': {'calls': set(), 'defined_in_class': None}, 'decorated_function': {'calls': {'flash', 'wraps', 'jsonify', 'f'}, 'defined_in_class': None}, 'index': {'calls': {'render_template', 'db.session.query'}, 'defined_in_class': None}, 'add_entry': {'calls': {'url_for', 'abort', 'db.session.commit', 'flash', 'redirect', 'db.session.add'}, 'defined_in_class': None}, 'login': {'calls': {'flash', 'render_template', 'redirect', 'url_for'}, 'defined_in_class': None}, 'logout': {'calls': {'flash', 'redirect', 'url_for'}, 'defined_in_class': None}, 'delete_entry': {'calls': {'db.session.query(models.Post).filter_by(id=new_id).delete', 'db.session.query', 'repr', 'db.session.commit', 'jsonify', 'flash', 'db.session.query(models.Post).filter_by'}, 'defined_in_class': None}, 'search': {'calls': {'render_template', 'request.args.get', 'db.session.query'}, 'defined_in_class': None}}, 'classes': {}, 'imports': ['os', 'functools', 'pathlib', 'flask', 'flask_sqlalchemy', 'project']}

G = nx.DiGraph()

# Add nodes for each function
for func in data['functions']:
    G.add_node(func)

# Add edges for function calls
for func, details in data['functions'].items():
    for called_func in details['calls']:
        if called_func in data['functions']:  # Internal call
            G.add_edge(func, called_func)
        else:  # External call (to a library or untracked function)
            G.add_node(called_func, style='dashed')  # Dashed style for external nodes
            G.add_edge(func, called_func)

# Draw the graph
nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
plt.show()


class Animal():
    def bark(self):
        print("hi")