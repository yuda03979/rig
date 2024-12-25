from RIG.globals import GLOBALS
import pandas as pd

def clean_text(text):
    """Remove all non-alphanumeric characters and convert to lowercase."""
    return ''.join(char.lower() for char in text if char.isalnum())

def prompt_json_gemma_v1(free_text, type_name, schema, description):
    prompt = f"""
    You are a helpful assistant trained to extract information from free text and format it to match a JSON schema. Your task is to fill out the given JSON schema with the corresponding values from the provided free text. If a field in the schema is not mentioned in the text, use "null". Follow this format strictly.

    Example:
    Free text:

    "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. Add short desc: Heavy winds and lightning expected. Duration in hours: 6."
    Schema:
    {{
    "alertType": "string",
    "areaCode": "int",
    "intensity": "string",
    "urgency": "string",
    "forecastSource": "string",
    "description": "string",
    "duration": "int"
    "ruleInstanceName": "str"
    "severity": "int"
    }}

    Output:
    {{
    "alertType": "Thunderstorm",
    "areaCode": 2001,
    "intensity": "severe",
    "urgency": "high",
    "forecastSource": "null",
    "description": "Heavy winds and lightning expected. ",
    "duration": 6,
    "ruleInstanceName": "Weather Alert - other"
    "severity": "null"
    }}
    Now, perform the task for the following:

    Free text:
    {free_text}

    Schema:
    {schema}

    you also got context for the fields to help you - dont fill that: {description}
    Output:
    """
    return prompt


def prompt_json_gemma_v1_b(free_text, type_name, schema, description):
    prompt = f"""
    You are a helpful assistant trained to extract information from free text and format it to match a JSON schema. Your task is to fill out the given JSON schema with the corresponding values from the provided free text. If a field in the schema is not mentioned in the text, use "null". Follow this format strictly.

    Example 1:
    - Free text: 
    "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. Add short desc: Heavy winds and lightning expected. The duration of this case, I'd say, is around two."
    - Schema:
    {{
        "alertType": "string",
        "areaCode": "int",
        "intensity": "string",
        "urgency": "string",
        "forecastSource": "string",
        "description": "string",
        "duration": "int",
        "ruleInstanceName": "string",
        "severity": "int"
    }}
    - Output:
    {{
        "alertType": "Thunderstorm",
        "areaCode": 2001,
        "intensity": "severe",
        "urgency": "high",
        "forecastSource": "null",
        "description": "Heavy winds and lightning expected.",
        "duration": 2,
        "ruleInstanceName": "Weather Alert - other",
        "severity": "null"
    }}
    Example 2: 
    - Free text: 
     "Add a report for 'Shell Delay'. Equipment Malfunction case. Type: shell. Site is not important. Malfunction at level five, urgency four. Description: Detonation delayed. Severity am i think 3.",
    - Schema:
    {{
        "type": "string",
        "site": "string",
        "malfunctionLevel": "int",
        "urgency": "int",
        "description": " string",
        "ruleInstanceName": "string",
        "severity": "int",
    }}

    - Output:
    {{
        "type": "shell",
        "site": "empty",
        "malfunctionLevel": 5,
        "urgency": 4,
        "description": "Detonation delayed",
        "ruleInstanceName": "Equipment Malfunction - Shell Delay",
        "severity": 3,
    }}
    Now, perform the task for the following:

    Free text:
    {free_text}

    Schema:
    {schema}

    you also got context for the fields to help you - dont fill that: {description}
    Output:
    """
    return prompt


def prompt_yaml_gemma(free_text, type_name, schema, description):
    prompt = f"""
    You are a helpful assistant trained to extract information from free text and format it to match a JSON schema. Your task is to fill out the given JSON schema with the corresponding values from the provided free text. If a field in the schema is not mentioned in the text, use "null". return it as YAML. Follow this format strictly.

    Example:
    Free text:

    "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. Add short desc: Heavy winds and lightning expected. Duration in hours: 6."
    Schema:
    {{
    "alertType": "string",
    "areaCode": "int",
    "intensity": "string",
    "urgency": "string",
    "forecastSource": "string",
    "description": "string",
    "duration": "int"
    "ruleInstanceName": "str"
    }}

    Output:
    ---
alertType: Thunderstorm
areaCode: 2001
intensity: severe
urgency: high
forecastSource: 'null'
description: 'Heavy winds and lightning expected. '
duration: 6
ruleInstanceName: Weather Alert - other

    Now, perform the task for the following:

    Free text:
    {free_text}

    Schema:
    {schema}

    you also got context for the fields to help you - dont fill that: {description}
    Output:
    """
    return prompt


def prompt_json_gemma_v2(free_text, type_name, schema, description):
    prompt = f"""
    You are a helpful assistant trained to extract information from free text and format it to match a JSON schema. Your task is to fill out the given JSON schema with the corresponding values from the provided free text. If a field in the schema is not mentioned in the text, use "null". Follow this format strictly.

    Example:
    - Free text:

    "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. Add short desc: Heavy winds and lightning expected. The duration of this case, I'd say, is around a of two"
    - Schema:
    {{
    "alertType": "string",
    "areaCode": "int",
    "intensity": "string",
    "urgency": "string",
    "forecastSource": "string",
    "description": "string",
    "duration": "int"
    "ruleInstanceName": "str"
    "severity": "int"
    }}

    - Output:
    {{
    "alertType": "Thunderstorm",
    "areaCode": 2001,
    "intensity": "severe",
    "urgency": "high",
    "forecastSource": "null",
    "description": "Heavy winds and lightning expected. ",
    "duration": 6,
    "ruleInstanceName": "Weather Alert - other"
    "severity": "null"
    }}
    Now, perform the task for the following:

    - Free text:
    {free_text}

    - Schema:
    {schema}

    you also got context for the fields to help you - dont fill that: {description}
    - Output:
    """
    return prompt


def prompt_json_gemma_v3(free_text, type_name, schema, description):
    """
    from cloude
    """
    prompt = f"""
    Task: Extract structured information from free text and format it precisely to match the given JSON schema.

    Instructions:
    1. Carefully read the entire free text
    2. Map values exactly to the corresponding schema fields
    3. If a field is not present in the text, use "null"
    4. Ensure type consistency (convert to correct type as specified in schema)
    5. Be precise and concise in value extraction

    Schema Details:
    {schema}

    Additional Context (DO NOT include in output):
    {description}

    Example Conversion:
    - Input Text: "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. Add short desc: Heavy winds and lightning expected. The duration of this case, I'd say, is around a of two"
    - Schema: 
    {{
        "alertType": "string",
        "areaCode": "int",
        "intensity": "string",
        "urgency": "string",
        "forecastSource": "string",
        "description": "string",
        "duration": "int",
        "ruleInstanceName": "str",
        "severity": "int"
    }}
    - Output:
    {{
        "alertType": "Thunderstorm",
        "areaCode": 2001,
        "intensity": "severe",
        "urgency": "high",
        "forecastSource": null,
        "description": "Heavy winds and lightning expected.",
        "duration": 2,
        "ruleInstanceName": "Weather Alert - other",
        "severity": null
    }}

    Current Input Text:
    {free_text}

    Provide the JSON output following the schema precisely:
    """
    return prompt


def prompt_json_gemma_v4(free_text, type_name, schema, description):
    """
    from chat gpt
    """
    prompt = f"""
    Extract information from the provided text and format it according to the given JSON schema. If a field is not mentioned in the text, set its value to "null". Follow the schema exactly.

    Example:
    - Free text: 
    "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. Add short desc: Heavy winds and lightning expected. The duration of this case, I'd say, is around two."
    - Schema:
    {{
        "alertType": "string",
        "areaCode": "int",
        "intensity": "string",
        "urgency": "string",
        "forecastSource": "string",
        "description": "string",
        "duration": "int",
        "ruleInstanceName": "string",
        "severity": "int"
    }}
    - Output:
    {{
        "alertType": "Thunderstorm",
        "areaCode": 2001,
        "intensity": "severe",
        "urgency": "high",
        "forecastSource": "null",
        "description": "Heavy winds and lightning expected.",
        "duration": 2,
        "ruleInstanceName": "Weather Alert - other",
        "severity": "null"
    }}

    Now process this input:
    - Free text: {free_text}
    - Schema: {schema}
    - Context for fields (do not fill): {description}
    - Output:
    """
    return prompt



def prompt_json_gemma_v5(free_text, type_name, schema, description, examples=None):
    example_3 = f"""
### Example 3 (Example for handling empty values):
Free text:
"Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. The duration of this case, I'd say, is around two. severity is empty or unclear"
Schema:
{{
    "alertType": "string",
    "areaCode": "int",
    "intensity": "string",
    "urgency": "string",
    "forecastSource": "string",
    "duration": "int",
    "ruleInstanceName": "string",
    "severity": "int"
}}
Output:
{{
    "alertType": "Thunderstorm",
    "areaCode": 2001,
    "intensity": "severe",
    "urgency": "high",
    "forecastSource": "null",
    "duration": 2,
    "ruleInstanceName": "Weather Alert - other",
    "severity": "null"
}}
"""
    if not examples["example_1"]["free_text"] or not examples["example_2"]["free_text"]:
        examples = f"""

### Example 1 :
Free text:
"Add a report for 'Shell Delay'. Equipment Malfunction case. Type: shell. Site is not important. Malfunction at level five, urgency four. Desc: Detonation delayed in poland Severity i think 3."
Schema:
{{
    "type": "string",
    "site": "string",
    "malfunctionLevel": "int",
    "urgency": "int",
    "description": " string",
    "ruleInstanceName": "string",
    "severity": "int"
}}
Output:
{{
    "type": "shell",
    "site": "empty",
    "malfunctionLevel": 5,
    "urgency": 4,
    "description": "Detonation delayed in poland",
    "ruleInstanceName": "Equipment Malfunction - Shell Delay",
    "severity": 3
}}

{example_3}
        """
    else:
        example_free_text_1 = examples["example_1"]["free_text"]
        df = GLOBALS.db_manager.get_df()

        try:
            example_schema_1 = df.loc[
                df["type_name"].apply(clean_text) == clean_text(examples["example_1"]["type_name"]), "schema"
            ].values[0]
        except IndexError:
            # Handle the case where no matching value is found
            example_schema_1 = "***schema extraction failed***"  # Replace with your desired default value
            print("1" + example_schema_1)

        example_output_1 = str(examples["example_1"]["response"])

        example_free_text_2 = examples["example_2"]["free_text"]
        try:
            example_schema_2 = df.loc[
                df["type_name"].apply(clean_text) == clean_text(examples["example_2"]["type_name"]), "schema"
            ].values[0]
        except IndexError:
            # Handle the case where no matching value is found
            example_schema_2 = "***schema extraction failed***"  # Replace with your desired default value
            print("2" + example_schema_2)

        example_output_2 = str(examples["example_2"]["response"])

        examples = f"""
### Example 1 (Similar Style Example):
Schema:
{example_schema_1}
Free text:
{example_free_text_1}
Output:
{example_output_1}

### Example 2 (Closest Task Match) :
Schema:
{example_schema_2}
Free text:
{example_free_text_2}
Output:
{example_output_2}

{example_3}
        """

    prompt = f"""
    ### Rules:
1. Only use fields explicitly listed in the schema below.
2. Do not add or infer fields. Fields missing in the schema or text should be set to "null".
3. Carefully map field names from the schema to the text, even if the phrasing differs.
4. Treat words like "without", "unknown" as "null", while "standard" "low" etc. will return the value.
5. Output must match the schema exactly - your answer should be without \\n or new line".

        ***Be sure to follow these rules***

    ### Schema:
    {schema}

    ### Examples:
    {examples}
    ---

    ### Context (do not use for filling fields, only as reference for the schema):
    {description}

    ---
    ### Task:
    - Free text: {free_text}
    - Output:
    """
    print("prompt = " + prompt)
    return prompt


def prompt_json_gemma_v51(free_text, type_name, schema, description):
    prompt = f"""
        ### Rules:
    1. Only use fields explicitly listed in the schema below.
    2. Do not add or infer fields. Fields missing in the schema or text should be set to "null".
    3. Carefully map field names from the schema to the text, even if the phrasing differs.
    4. Treat words like "without", "unknown" as "null", while "standard" "low" etc. will return the value.
    5. Output must match the schema exactly.
    6. your answer should be without \\n or new line"

            ***Be sure to follow these rules***

        ### Schema:
        {schema}

        ### Examples:
        
        ### Example 1 :
        Free text:
        "Add a report for 'Shell Delay'. Equipment Malfunction case. Type: shell. Site is not important. Malfunction at level five, urgency four. Desc: Detonation delayed in poland Severity i think 3."
        Schema:
        {{
            "type": "string",
            "site": "string",
            "malfunctionLevel": "int",
            "urgency": "int",
            "description": " string",
            "ruleInstanceName": "string",
            "severity": "int"
        }}
        Output:
        {{
            "type": "shell",
            "site": "null",
            "malfunctionLevel": 5,
            "urgency": 4,
            "description": "Detonation delayed in poland",
            "ruleInstanceName": "Equipment Malfunction - Shell Delay",
            "severity": 3
        }}
        
        ### Example 2
        Free text:
        "Create an instance of a surface skimmer, which is a type of marine species. It has a tentacle length of, um, seven. However, its water filtering ability is low, it's like, really low. The creature's camouflage ability is non-existent, and same goes for its reproduction method. This surface skimmer can tolerate depths up to five hundred. Its nutrient absorption is also low, and it's not that flexible under pressure. The sediment intake for this species is about ten, and the severity of this creature is one."
        Schema:
        {{
            'Tentacle length': 'Int',
            'Water filtering ability': 'String',
            'Camouflage skill': 'string',
            'Reproduction method': 'String',
            'Depth tolerance': 'Int',
            'Nutrient absorption': 'String',
            'Flexibility under pressure': 'String',
            'Sediment intake': 'Int',
            'ruleInstanceName': 'string',
            'severity': 'int'
        }}
        Output:
        {{
            ""ruleInstanceName"": ""surface skimmer"",
            ""severity"": ""1"",
            ""Tentacle length"": ""7"",
            ""Water filtering ability"": ""low"",
            ""Camouflage skill"": ""null"",
            ""Reproduction method"": ""null"",
            ""Depth tolerance"": ""500"",
            ""Nutrient absorption"": ""low"",
            ""Flexibility under pressure"": ""low"",
            ""Sediment intake"": ""10""
        }}
    
    
     
        ### Example 3 (Example for handling empty values):
        Free text:
        "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. The duration of this case, I'd say, is around two. severity is empty or unclear"
        Schema:
        {{
            "alertType": "string",
            "areaCode": "int",
            "intensity": "string",
            "urgency": "string",
            "forecastSource": "string",
            "duration": "int",
            "ruleInstanceName": "string",
            "severity": "int"
        }}
        Output:
        {{
            "alertType": "Thunderstorm",
            "areaCode": 2001,
            "intensity": "severe",
            "urgency": "high",
            "forecastSource": "null",
            "duration": 2,
            "ruleInstanceName": "Weather Alert - other",
            "severity": "null"
        }}
        
          
            ---
    
            ### Context (do not use for filling fields, only as reference for the schema):
            {description}
    
            ---
            ### Task:
            - Free text: {free_text}
            - Output:
            """

    return prompt

