def prompt_for_gemma(query, type_name1: dict, type_name2: dict):
    prompt = f"""
            Analyze the following query:  
    {query} <END>

    Based on the query, choose which type is a better match from the two options provided. Use the schema and description as context for your decision.  

    Option 1:  
    - Name: {type_name1["type_name"]}  
    - Schema: {type_name1["schema"]}  
    - Description: {type_name1["description"]}  

    Option 2:  
    - Name: {type_name2["type_name"]}  
    - Schema: {type_name2["schema"]}  
    - Description: {type_name2["description"]} 

    You must return ONLY ONE: either {{"type_name": {type_name1["type_name"]}}} or {{"type_name": {type_name1["type_name"]}}}.  

    Note: it must be in json form!
    Example of expected output:  
    {{"type_name": "Hay_field"}}  

    Actual output:
            """
    return prompt


prefix_document = "classification: \n"
prefix_query = "classification: \n"
