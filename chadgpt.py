def extract_data(text):
    import os
    from dotenv import load_dotenv
    from openai import OpenAI


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
                        "description": "name of topic",},
                    "content":{
                        "type":"string",
                        "description": "subtopics of topic.",
                    },
                
                    }

                },
                "required": ["Topics","content"]
            }
    ]

    prompt = f"please extract the important information from this json{text}, and teach the topics"
    messages = [{"role":"user","content":prompt}]
    response = client.chat.completions.create(model = "gpt-3.5-turbo-0613",
                                              messages=messages,
                                              functions=extract_function,
                                              function_call="auto",
                                              choices = response.choices)
    
    choices = response.choices

    if choices and choices[0].message and choices[0].message.function_call:
        function_call = choices[0].message.function_call
        function_name = function_call.name
        function_arguments = function_call.arguments
        print(function_arguments)
        return(function_arguments)
    
    