'''
This file is used for driving the running summary geneartion within a repo
For each folder immediately under "root" of a git repo, it would genearte a 
running summary for the immediate folder ; it will then concatenate the running
summaries from each immediate folder, together with the running summary for files
immediately under "root".
'''
from git_repo_relation import generate_structure_json

url = "https://api.github.com/repos/Weishi-Ding/AST_LLM/contents/"
folder_struct = generate_structure_json(url)
processed_folder = {}
cur = "root"

running_summary = []

def generate_summary_for_one_folder(path, running_summary):
    files = folder_struct[path]['files']
    dirs = folder_struct[path]['dirs']
    
    #parse files relation in folder
    for file in files:
        #generate summaries
        running_summary.append(file)

    for dir in dirs:
        running_summary = generate_summary_for_one_folder(dir, running_summary)  
    #running summary here
    return running_summary

res = generate_summary_for_one_folder(cur, running_summary)
print(res)


# {
#   "root": {
#     "files": [
#       "README.md",
#       "Zichen.md"
#     ],
#     "dirs": [
#       "sample_repo"
#     ]
#   },
#   "sample_repo": {
#     "files": [
#       ".DS_Store",
#       "DQN.py",
#       "agent.py",
#       "env.py",
#       "main.py",
#       "portfolio.py",
#       "utils.py"
#     ],
#     "dirs": [
#       "data_processing"
#     ]
#   },
#   "sample_repo/data_processing": {
#     "files": [
#       "backtest.py",
#       "data_process.py"
#     ],
#     "dirs": []
#   }
# }
