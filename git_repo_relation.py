import requests
import json
import base64

def getGitSourceCode(api_url):
    # Send GET request
    response = requests.get(api_url)
    # print(api_url)
    # Check if the request was successful
    if response.status_code == 200:
        # Decode the file content from base64
        file_content = base64.b64decode(response.json()['content'])
        # print(file_content.decode('utf-8'))
        return file_content
    else:
        print("Failed to fetch file content")

def get_files_structure(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        return content
    else:
        print(f"Error: {response.status_code}")

def parse_file_structure_json(url_init, headers, folder_structure, source_code_dict, path = "root"):
    if path != "root":
        url_query = url_init + path + "/"
    else:
        url_query = url_init
    print(url_query)
    content = get_files_structure(url_query, headers)
    for item in content:
        path = path.split('/')[-1]
        if path not in folder_structure:
            folder_structure[path] = {"files": [], "dirs": []}
        if item['type'] == 'file':
            folder_structure[path]["files"].append(item['name'])
            cur_url = url_query + item['name']
            if cur_url.endswith('.py'): #only collecting py file
                cur_code_file = getGitSourceCode(cur_url).decode('utf-8')
                source_code_dict[cur_url.replace(url_init, "")] = cur_code_file
            else:
                pass
        elif item['type'] == 'dir':
            # print(item['name'].split('/'))
            folder_structure[path]["dirs"].append(item['name'])
            parse_file_structure_json(url_init, headers, folder_structure, source_code_dict, item['path'])
            
    return
        
def generate_structure_json(url):
    github_token = "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"
    # url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    # url = "https://api.github.com/repos/Kathalyst/TaskManager/contents/"
    headers = {'Authorization': f'token {github_token}'}
    folder_structure = {} # root is the default parent level folder
    source_code_dict = {}
    parse_file_structure_json(url, headers, folder_structure, source_code_dict, path = "root")
    return (folder_structure, source_code_dict)
    

# getGitSourceCode(f"https://api.github.com/repos/Weishi-Ding/AST_LLM/contents/sample_repo/DQN.py")
# generate_structure_json("https://api.github.com/repos/Weishi-Ding/AST_LLM/contents/")


# print(a)
# get_files_structure("https://api.github.com/repos/Weishi-Ding/AST_LLM/contents/sample_repo/", headers)
# get_files_structure("https://api.github.com/repos/Weishi-Ding/AST_LLM/contents/sample_repo/data_processing/", headers)
# print(json.dumps(folder_structure, indent=2))

