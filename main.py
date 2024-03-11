import json
import os
import heapq
from openai import OpenAI
from parse import all
python_files = all() #python_files is a list of all .py files in the curent folder
client = OpenAI(api_key= "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")

# client = OpenAI(api_key="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")
# root_path = "/Users/weishiding/Desktop/Capstone/Spring/llmyacc/llmyacc_supplemental/sample_flask_web_app/flaskr/"
root_path = "/Users/weishiding/Desktop/prev/cs138/project138/"

## build the depend_dic
def build_depend_dic(depend_dic):
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

def build_heap_ele(depend_dic, documentation_dic):
    documentation_dic = {file_name : None for file_name in depend_dic.keys()}
    # print(depend_dic)
    heap_ele = list(depend_dic.values())
    heapq.heapify(heap_ele)
    
    return heap_ele


def generate_documentation_prompt(code, count, summary, skills = False, curated_info = None):
    if count == 0: # this is the first file for us to generate
        if skills == False:
            return f'''We are in the process of documenting a Python code repository, examining one code file at a time. \n Now, we are looking at the first code file; here is the code of the current file \n ``` {code} ``` \n Since you have not seen any other code files in this repo yet, you SHOULD NOT make assumptions for unseen code. \n Your current generation will be used as a running summary when seeing further code files.\n Your task involves generating a code summary specific to the current code, as well as generating the running summary with insights from the current code file. Please adhere to the following structured approach:

                        **Step 1: Analyze the Current Code File**
                        Begin by thoroughly analyzing the content of the current code file. Your analysis should cover:

                        a) **Code File Overview**: Provide a concise summary of the code file's purpose.

                        b) **Function Documentation**: Detail the documentation for each function found within the code file, including docstrings.

                        c) **Additional Insights**: Note any further observations or remarks that might shed light on the code file's role within the broader project scope.

                        **Step 2: Integrate Your Analysis into a Running Summary**
                        Following your analysis in Step 1, integrate your findings into a running summary. Your running summary should contribute to a comprehensive and evolving overview of the code repository. Ensure your running summary can be seamlessly merge with future gathered information, preserving and building upon the foundation without omitting any critical details.

                        To structure your response, please use the following format:

                        - - - - - - - - - - - - - - - - - - Specific Code Summary - - - - - - - - - - - - - - - - - -
                        [Insert your analysis from Step 1 here]
                        - - - - - - - - - - - - - - - - - - Running Summary for the Code - - - - - - - - - - - - - - - - - - -
                        [Insert your analysis from Step 2 here]

                        Ensure that your generation accurately reflects the structure requested, with clear and organized content under each key. This format will facilitate a structured and accessible documentation process.
                    '''
        else:
            return f'''We are in the process of documenting a Python code repository, examining one code file at a time. As part of our documentation strategy, we have prepared a curated list of technology stack information, including domains, sub-domains, and specific technology tags, to guide the analysis towards a controlled granularity of technical details.
                       Now, we are looking at the first code file; here is the code of the current file:
                       ``` {code} ```
                       Since you have not seen any other code files in this repo yet, you SHOULD NOT make assumptions for unseen code. 
                       Your current generation will be used as a running summary when seeing further code files.

                       Your task involves generating a code summary specific to the current code, as well as generating the running summary with insights from the current code file, including an initial consideration of the technology stack based on the curated information provided.

                       Here is curated information regarding the relevant the domain of the code repo we are looking at:
                       ``` {curated_info} ```
                       Please note that the curated information, while being the same domain as the code repo, may not be comprehensive enough or direcly related to the repo. 
                       The curated info is just to give you a sense of granulaity of technical details in your generation, please utilize your knowledge and not be limited to our curated information.

                       Please adhere to the following structured approach:
                       
                       **Step 1: Analyze the Current Code File**
                       Begin by thoroughly analyzing the content of the current code file. Your analysis should cover:

                       a) **Code File Overview**: Provide a concise summary of the code file's purpose.

                       b) **Function Documentation**: Detail the documentation for each function found within the code file, including docstrings.

                       c) **Additional Insights**: Note any further observations or remarks that might shed light on the code file's role within the broader project scope.

                       d) **Initial Observations on Technology Stack and Design/Engineering Highlights**: Discuss any immediate observations related to the technology stack or design/engineering highlights, inspired by the curated technology stack information. Remember, the curated technology stack information is there to help you understand the granularity of technical details but you should not be restricted to use your own knowledge.

                       **Step 2: Integrate Your Analysis into a Running Summary**
                       Following your analysis in Step 1, integrate your findings into a running summary. Your running summary should contribute to a comprehensive and evolving overview of the code repository. Ensure your running summary can be seamlessly merge with future gathered information, preserving and building upon the foundation without omitting any critical details.
                       In the running summary, you must include information regaring technology stack used, at the granularity recommended by our curated info.
                       To structure your response, please use the following format:

                       - - - - - - - - - - - - - - - - - - Specific Code Summary - - - - - - - - - - - - - - - - - -
                       [Insert your analysis from Step 1 here]
                       - - - - - - - - - - - - - - - - - - Running Summary for the Code - - - - - - - - - - - - - - - - - - -
                       [Insert your analysis from Step 2 here]

                       Ensure that your generation accurately reflects the structure requested, with clear and organized content under each key. This format will facilitate a structured and accessible documentation process.
                    '''
    else:
        if skills == False:
            return f'''We are in the process of documenting a Python code repository, examining one code file at a time. 
                        Up to this point, we've compiled a running summary based on previously reviewed code files. 
                        Below is the current state of our running summary:
                        
                        ```{summary}```
                        
                        We are now moving on to analyze a new, previously unseen code file. 
                        Here is the content of this file: 
                        
                        ``` {code} ```
                        
                        As we have not yet reviewed the entire codebase, it's crucial to avoid making assumptions about any code files that have not been examined. 
                        
                        Your task involves generating a code summary specific to the current code, as well as updating the running summary with insights from a newly examined code file. 
                        
                        Please adhere to the following approach:

                            **Step 1: Analyze the Current Code File**
                            Begin by thoroughly analyzing the content of the current code file. Your analysis should cover:

                            a) **Code File Overview**: Provide a concise summary of the code file's purpose, reflecting on the context outlined in the existing running summary.

                            b) **Function Documentation**: Detail the documentation for each function found within the code file, including docstrings.

                            c) **Additional Insights**: Note any further observations or remarks that might shed light on the code file's role within the broader project scope.

                            **Step 2: Integrate Your Analysis into the Running Summary**
                            Following your analysis in Step 1, integrate your findings into the provided running summary. Your update should enhance the existing documentation, contributing to a comprehensive and evolving overview of the code repository. Ensure your additions seamlessly merge with previously gathered information, preserving and building upon the foundation without omitting any critical details.
                            
                            To structure your response, please use the following specific format:
                            - - - - - - - - - - - - - - - - - - Specific Code Summary - - - - - - - - - - - - - - - - - -
                            [Insert your analysis from Step 1 here]
                            - - - - - - - - - - - - - - - - - - Running Summary for the Code - - - - - - - - - - - - - - - - - - -
                            [Insert your analysis from Step 2 here]

                            Ensure that your generation accurately reflects the structure requested, with clear and organized content under each key. This format will facilitate a structured and accessible documentation process.
                    '''
        else:
            return f''' We are in the process of documenting a Python code repository, examining one code file at a time. As part of our documentation strategy, we have prepared a curated list of technology stack information, including domains, sub-domains, and specific technology tags, to guide the analysis towards a controlled granularity of technical details.
                
                        Up to this point, we've compiled a running summary based on previously reviewed code files. 
                        Below is the current state of our running summary:
                        
                        ```{summary}```
                        
                        We are now moving on to analyze a new, previously unseen code file. 
                        Here is the content of this file: 
                        
                        ``` {code} ```
                        
                        As we have not yet reviewed the entire codebase, it's crucial to avoid making assumptions about any code files that have not been examined. 
                        
                        Your task involves generating a code summary specific to the current code, as well as generating the running summary with insights from the current code file, including an initial consideration of the technology stack based on the curated information provided.

                        Here is curated information regarding the relevant the domain of the code repo we are looking at:
                        ``` {curated_info} ```
                        Please note that the curated information, while being the same domain as the code repo, may not be comprehensive enough or direcly related to the repo. 
                        The curated info is just to give you a sense of granulaity of technical details in your generation, please utilize your knowledge and not be limited to our curated information.
                        
                        Please adhere to the following approach:

                        **Step 1: Analyze the Current Code File**
                        Begin by thoroughly analyzing the content of the current code file. Your analysis should cover:

                        a) **Code File Overview**: Provide a concise summary of the code file's purpose, reflecting on the context outlined in the existing running summary.

                        b) **Function Documentation**: Detail the documentation for each function found within the code file, including docstrings.

                        c) **Additional Insights**: Note any further observations or remarks that might shed light on the code file's role within the broader project scope.

                        d) **Initial Observations on Technology Stack and Design/Engineering Highlights**: Discuss any immediate observations related to the technology stack or design/engineering highlights, inspired by the curated technology stack information. Remember, the curated technology stack information is there to help you understand the granularity of technical details but you should not be restricted to use your own knowledge.

                        **Step 2: Integrate Your Analysis into the Running Summary**
                        Following your analysis in Step 1, integrate your findings into the provided running summary. Your update should enhance the existing documentation, contributing to a comprehensive and evolving overview of the code repository. Ensure your additions seamlessly merge with previously gathered information, preserving and building upon the foundation without omitting any critical details.
                        In the running summary, you must include information regaring technology stack used, at the granularity recommended by our curated info.
                        To structure your response, please use the following specific format:
                        - - - - - - - - - - - - - - - - - - Specific Code Summary - - - - - - - - - - - - - - - - - -
                        [Insert your analysis from Step 1 here]
                        - - - - - - - - - - - - - - - - - - Running Summary for the Code - - - - - - - - - - - - - - - - - - -
                        [Insert your analysis from Step 2 here]

                        Ensure that your generation accurately reflects the structure requested, with clear and organized content under each key. This format will facilitate a structured and accessible documentation process.
                    '''

def generate_finaldoc_prompt(summary, skills = False, curated_info = None):
    if skills == False:
        return f'''
            We are generating documentation for a Python code repo. 
            We already have a summary for the whole code repo, here's the summary:
            ```{summary}```
            Now, we aim to make this summary more professional and suitable for being a README.md file. Below is the structure of the README.md file, and your task is to integrate the summary I just provided into this structure, ensuring the documentation is comprehensive and professional. Please use a confident and determined tone throughout the documentation, avoiding words like "maybe" to eliminate uncertainty. The outputs should sound definitive. For ‘Contribution’, ‘Licensing’ and ‘Contact Info’ parts. 

            ### README.md Structure

            1. **Project Title**
            - Provide a clear, concise title that reflects the essence of the code repository.
            -  If there's no information, you should fill in with “N/A” rather than make it up.

            2. **Introduction or Summary**
            - Expand on the provided summary to give readers an overview of the project's purpose, scope, and functionality.
            -  If there's no information, you should fill in with “N/A” rather than make it up.

            3. **Installation Instructions**
            - Offer detailed, step-by-step instructions on how to set up the development environment, including any prerequisites and dependencies necessary for the project.
            - If there's no information, you should fill in with “N/A” rather than make it up.

            4. **Usage**
            - Include examples of how to use the project, showcasing code snippets and command-line instructions to help users get started quickly.
            - If there's no information, you should fill in with “N/A” rather than make it up.

            5. **Features**
            - List the key features and functionalities of the project, highlighting what sets it apart from other projects.
            - If there's no information, you should fill in with “N/A” rather than make it up.

            6. **Contributing**
            - Outline guidelines for contributions, including coding standards, branch naming conventions, and the process for submitting pull requests.
            - If there's no information, you should fill in with “N/A” rather than make it up.
            7. **License**
            - Provide information on the project's licensing, directing users to the LICENSE file for more details.
            - If there's no information, you should fill in with “N/A” rather than make it up.
            8. **Contact Information**
            - Share contact information or links to community platforms where users and contributors can reach out for support or to engage with the project community.
            - If there's no information, you should fill in with “N/A” rather than make it up.

            Remember to weave the provided summary seamlessly into the structure, ensuring each section is aligned with the overarching narrative and goals of the code repository.
            '''
    else:
        return f'''
                We are generating documentation for a Python code repo. 
                We already have a summary for the whole code repo, here's the summary:
                ```{summary}```
                Now, our aim is to refine this summary into a more professional and comprehensive README.md file. This README should not only serve as an introduction to the project but also highlight the technology stack used and the engineering achievements. 
                Please use a confident and determined tone throughout the documentation, avoiding words like "maybe" to ensure certainty. 
                The outputs should sound definitive.

                ### README.md Structure

                1. **Project Title**
                - Provide a clear, concise title that reflects the essence of the code repository.

                2. **Introduction or Summary**
                - Expand on the provided summary to give readers an overview of the project's purpose, scope, and functionality.

                3. **Technology Stack**
                - Detail the technology stack used in this project, including programming languages, frameworks, libraries, and any other tools. Highlight how these choices contribute to the project's goals.

                4. **Engineering Highlights**
                - Describe key engineering decisions and achievements in the project. Include innovative solutions to problems, optimizations made for performance or scalability, and any challenges overcome during development.

                5. **Features**
                - List the key features and functionalities of the project, highlighting what sets it apart from other projects.

                6. **Usage**
                - Showcase examples of how to use the project, including code snippets and command-line instructions for getting started.

                Remember to weave the provided summary seamlessly into the structure, ensuring each section is aligned with the overarching narrative and goals of the code repository.
                This documentation should serve as a professional, engaging, and informative introduction to the project, highlighting its technical sophistication and the ingenuity of its development.
                '''

def get_code_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def get_response(prompt, model="gpt-4"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=1)
    #print(response.choices[0].message.content)
    return response.choices[0].message.content




# print(description_dic)

def main():
    # depend_dic is a dictionary that stores the dependcy of each files
    # The value storeed in this dictionary is the following:
    # {file_name: [#imports, [imports names], index in python_files]}
    # #imports will decreased by one if one of its dependency file's documentation
    # has been generated
    depend_dic = {} 

    # heap_ele is a heap whoes elementes are the values in the depend_dic
    # It's heapified according to the #imports of each value
    heap_ele = []

    # documentation_dic is used to store the documentation of each file
    # sample: {file_name: vector_embedding}
    documentation_dic = {}

    build_depend_dic(depend_dic)
    heap_ele = build_heap_ele(depend_dic, documentation_dic)

    
    count = 0 # number of code files processed so far
    summary = None # running summary so far
    curated_info = None
    with open('/Users/weishiding/Desktop/Capstone/Spring/llmyacc/yacc_code/curated.json', 'r') as file:
        curated_info = file.read()
    while heap_ele:
        chosen = heap_ele[0]
        # print(f"idx is {chosen[-1]}")
        # print(f"keys are: {depend_dic.keys()}")
        file_name = list(depend_dic.keys())[chosen[-1]]
        # print(file_name)
        
        code = get_code_from_file(root_path + list(depend_dic.keys())[chosen[-1]] + '.py') 
        # generate_documentation_prompt(code, count, summary, skills = False, curated_info = None)  
        prompt = generate_documentation_prompt(code, count, summary, True, curated_info)
        description = get_response(prompt)
        summary = description
        print(f"----This is the generation for {file_name}----")
        print(description)
        documentation_dic[file_name] = description
        count += 1

        for idx, ele in enumerate(heap_ele):
            if file_name in ele[-2]:
                heap_ele[idx][0] -= 1
                # print(list(heap_ele[idx]))
        heapq.heappop(heap_ele)
        heapq.heapify(heap_ele)

        print(heap_ele)
    print("-----------------------------------This is the final README.md-------------------------------------")
    # generate_finaldoc_prompt(summary, skills = False, curated_info = None)
    prompt = generate_finaldoc_prompt(summary, True, curated_info)
    readme = get_response(prompt)
    print(readme)
    # print(documentation_dic)
# # counts = depend_dic.values
# index_to_check =

if __name__ == "__main__":
    main()
    
