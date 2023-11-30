from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os
from dotenv import load_dotenv
from openai import OpenAI
import json



images = convert_from_path('olevel4048mathsyllabus.pdf')

for i, image in enumerate(images):
    text = pytesseract.image_to_string(image)
    print(f"===== Page {i+1} =====")
    print(text)






load_dotenv()

api_key= os.getenv("OPENAI_APIKEY")
client = OpenAI(api_key=api_key)


extract_function = [
    {
        "name": "extract_info",
        "description": "extract parameters and summarise content",
        "parameters": {
            "type":"object",
            "properties":{
                "Topics":{
                    "type":"string",
                    "description": "topic of syllabus",},
                "content":{
                    "type":"string",
                    "description": "in point form, what is required",
                },
               
                }

            },
            "required": ["Topics","content"]
        }


    
]





prompt = f"please extract the important information from this json{text}, and teach the topics"
messages = [{"role":"user","content":prompt}]

# response = client.chat.completions.create(
#     model = "gpt-3.5-turbo-0613",
#     messages=messages,
#     functions=extract_function,
#     function_call="auto"
# )

# print(response)



#extracting json output of function call👇
# choices = response.choices

# # Assuming there's at least one choice and it contains a function call
# if choices and choices[0].message and choices[0].message.function_call:
#     function_call = choices[0].message.function_call

#     # Now you have the FunctionCall object
#     function_name = function_call.name
#     function_arguments = function_call.arguments
#     print(function_arguments)
