import json
import os
import heapq
from openai import OpenAI

client = OpenAI(api_key="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")
from parse import python_files
root_path = "/Users/weishiding/Desktop/Capstone/Spring/llmyacc/llmyacc_supplemental/sample_flask_web_app/flaskr/"

depend_dic = {}
for idx, file in enumerate(python_files):
    # Check if the file ends with .py
    # Split the file name and the extension
    with open(file + '.json', 'r') as cur:
        ele = json.load(cur)
        file_name, _ = os.path.splitext(file)
        # print(ele.values)
        depend_dic[file_name] = [len(ele['imports']), ele['imports'], idx]
    # Append the full path to the list
    # python_files.append(file_name_without_extension)

# print(depend_dic)

description_dic = {file_name : None for file_name in depend_dic.keys()}
print(depend_dic)
heap_ele = list(depend_dic.values())
heapq.heapify(heap_ele)

def generate_documentation_prompt(code):
    return f"Please generate detailed documentation for the following Python code:\n\n{code}\n\nInclude:\n- A brief overview of the code's purpose.\n- Docstrings for each function.\n- Any additional notes that could be helpful."

def get_code_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

#model_35 = "gpt-3.5-turbo"
def get_response(code, model="gpt-3.5-turbo"):
    prompt = generate_documentation_prompt(code)
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=1)
    #print(response.choices[0].message.content)
    return response.choices[0].message.content



while heap_ele:
    chosen = heap_ele[0]
    # print(f"idx is {chosen[-1]}")
    # print(f"keys are: {depend_dic.keys()}")
    file_name = list(depend_dic.keys())[chosen[-1]]
    print(file_name)
    
    code = get_code_from_file(root_path + list(depend_dic.keys())[chosen[-1]] + '.py')   
    description = get_response(code)
    # print(description)
    description_dic[file_name] = description



    for idx, ele in enumerate(heap_ele):
        if file_name in ele[-2]:
            heap_ele[idx][0] -= 1
            # print(list(heap_ele[idx]))
    heapq.heappop(heap_ele)
    heapq.heapify(heap_ele)
    # print(heap_ele)
# # # counts = depend_dic.values
# # index_to_check =
print(description_dic)



