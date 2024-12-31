import json

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
            # print("1" + example_schema_1)

        example_output_1 = str(examples["example_1"]["response"])

        example_free_text_2 = examples["example_2"]["free_text"]
        try:
            example_schema_2 = df.loc[
                df["type_name"].apply(clean_text) == clean_text(examples["example_2"]["type_name"]), "schema"
            ].values[0]
        except IndexError:
            # Handle the case where no matching value is found
            example_schema_2 = "***schema extraction failed***"  # Replace with your desired default value
            # print("2" + example_schema_2)

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
5. Output must match the schema exactly.

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
    # print("prompt = " + prompt)
    return prompt


def validation_prompt(free_text, response_dict):
    prompt = f"""You are a tough test taker, you give a score on a structured response deduced from a given free text, strictly according to the following rules:

    1. Award 100 points by default
    2. Deduct points ONLY if:
       - There is a direct contradiction between values in the response and the free text
       - A value is present in the response that cannot be directly found in the free text (except for 'null')
    3. If information cannot be found in the free text, 'null' is the CORRECT response
    4. Do not interpret, analyze, or make assumptions - check only for exact matches
    5. If the information in the free text has the word 'zero', and the extracted text has the word 'null', don't deduct points for it, that's fine
    6. Wherever a word or sentence appears in the free text that can indicate a lack of information such as 
    None, '', ' ', " ", "","unknown", "null","NULL", "None","no", "none ", "empty","EMPTY",0,'0', "not in use", and the like, The expectation that the extracted parameters will appear 'null' for this parameter.
    7.Ignore the RuleInstanceName parameter if present, do not deduct a score for an error or mismatch in this parameter.
    Free Text:
    {free_text}

    Structured Response:
    {json.dumps(response_dict, indent=2)}

    Here are examples to clarify:

    Example 1:
    Free Text:
    An instance of eagle assessment needs to be created, dealing with the type of assessment eagle. The scavenging efficiency of the eagle was around, um, eighty. However, the beak sharpness was much more severe, let's say something like seven. The flight altitude of the eagle is high, and the severity of the event is four. The vision acuity of the eagle is excellent, with a wingspan of about two hundred. The thermal riding skill of the eagle is expert, and the bone digestion is ninety. We don't have information on the feather maintenance.

    Structured Response:
    {{
        "ruleInstanceName": "eagle assessment",
        "severity": "4",
        "Scavenging efficiency": "80",
        "Flight altitude": "high",
        "Beak sharpness": "7",
        "Vision acuity": "excellent",
        "Wing span": "200",
        "Thermal riding skill": "expert",
        "Bone digestion": "90",
        "Feather maintenance": "null"
    }}

    Final Score: 100

    Example 2:
    Free Text:
    We need to generate an instance for Eagle Assessment. Our eagle is quite the scavenger, with an efficiency of about eighty. The flight altitude of this bird? High. Its beak sharpness is a solid seven. And you won't believe this, but the vision acuity is excellent! With a wingspan of, um, two hundred, and thermal riding skill of an expert, this bird is a pro. It has a bone digestion of ninety, but the feather maintenance is, well, just not available. The severity of this evaluation, let's say, is four.

    Structured Response:
    {{
        "ruleInstanceName": "null",
        "severity": "null",
        "Scavenging efficiency": "80",
        "Flight altitude": "high",
        "Beak sharpness": "7",
        "Vision acuity": "excellent",
        "Wing span": "200",
        "Thermal riding skill": "expert",
        "Bone digestion": "90",
        "Feather maintenance": "null"
    }}

    Final Score: 90

    Example 3:
    Free Text:
    We need to set up an instance of Viking Axe Analysis. This is related to the weapon type Viking Axe. The blade resilience of the axe is, well, unbreakable. The guard width is pretty broad. The grip of the axe is a bit rugged. However, the tip precision is just, um, low. The blade straightness is about, let's say something like eighty-five. The severity of the axe design is seven.

    Structured Response:
    {{
        "ruleInstanceName": "viking axe analysis",
        "severity": "7",
        "Blade sharpness": "null",
        "Handle grip": "null",
        "Weight distribution": "blade-heavy",
        "Chopping power": "null",
        "Throwing capability": "null",
        "Material durability": "null",
        "Combat effectiveness": "null",
        "Ornamentation": "null"
    }}

    Final Score: 70

    Example 4:
    Free Text:
    We need to analyze a new battle axe. The axe weight is unknown. The blade sharpness is zero. The handle length appears empty.

    Structured Response:
    {{
        "ruleInstanceName": "battle axe analysis",
        "Weight": "null",
        "Blade sharpness": "null",
        "Handle length": "null"
    }}

    Final Score: 100

    Example 5:
    Free Text:
    We need to analyze a new battle axe. The axe weight is unknown. The blade sharpness is zero. The handle length appears empty.

    Structured Response:
    {{
        "ruleInstanceName": "battle axe analysis",
        "Weight": "0",
        "Blade sharpness": "empty",
        "Handle length": "none"
    }}

    Final Score: 85

    Example 6:
    Free Text:
    A new sword was found. The blade length is 90 centimeters. The grip is leather. The weight is 2 kilos.

    Structured Response:
    {{
        "ruleInstanceName": "sword analysis",
        "Blade length": "90",
        "Grip material": "leather",
        "Weight": "2",
        "Blade material": "steel"
    }}

    Final Score: 80

    In fact, a score will be deducted for every parameter that exists and fulfills one of two things, or it contradicts what is written in the free text, or it cannot be deduced unequivocally from the text, so also a score is lowered for a parameter that can be deduced from the free text, but it appears null in this parameter.

    The final score is:"""
    return prompt


def validation_prompt_v2(free_text, response_dict):
    prompt = f"""
    your job is to classify if some `structure response` is the output of `free text`. your response should be in json.
    
    Example 1:
    Free Text:
    An instance of eagle assessment needs to be created, dealing with the type of assessment eagle. The scavenging efficiency of the eagle was around, um, eighty. However, the beak sharpness was much more severe, let's say something like seven. The flight altitude of the eagle is high, and the severity of the event is four. The vision acuity of the eagle is excellent, with a wingspan of about two hundred. The thermal riding skill of the eagle is expert, and the bone digestion is ninety. We don't have information on the feather maintenance.

    Structured Response:
    {{
        "ruleInstanceName": "eagle assessment",
        "severity": "4",
        "Scavenging efficiency": "80",
        "Flight altitude": "high",
        "Beak sharpness": "7",
        "Vision acuity": "excellent",
        "Wing span": "200",
        "Thermal riding skill": "expert",
        "Bone digestion": "90",
        "Feather maintenance": "null"
    }}

    Output:{{'score': 1}}

    Example 3:
    Free Text:
    We need to set up an instance of Viking Axe Analysis. This is related to the weapon type Viking Axe. The blade resilience of the axe is, well, unbreakable. The guard width is pretty broad. The grip of the axe is a bit rugged. However, the tip precision is just, um, low. The blade straightness is about, let's say something like eighty-five. The severity of the axe design is seven.

    Structured Response:
    {{
        "ruleInstanceName": "viking axe analysis",
        "severity": "7",
        "Blade sharpness": "null",
        "Handle grip": "null",
        "Weight distribution": "blade-heavy",
        "Chopping power": "null",
        "Throwing capability": "null",
        "Material durability": "null",
        "Combat effectiveness": "null",
        "Ornamentation": "null"
    }}

    Output:{{'score': 0}}

    Example 4:
    Free Text:
    We need to analyze a new battle axe. The axe weight is unknown. The blade sharpness is zero. The handle length appears empty.

    Structured Response:
    {{
        "ruleInstanceName": "battle axe analysis",
        "Weight": "null",
        "Blade sharpness": "null",
        "Handle length": "null"
    }}

    Output:{{'score': 1}}

    Example 5:
    Free Text:
    We need to analyze a new battle axe. The axe weight is unknown. The blade sharpness is zero. The handle length appears empty.

    Structured Response:
    {{
        "ruleInstanceName": "battle axe analysis",
        "Weight": "0",
        "Blade sharpness": "empty",
        "Handle length": "none"
    }}

    Output:{{'score': 0}}

    Example 6:
    Free Text:
    A new sword was found. The blade length is 90 centimeters. The grip is leather. The weight is 2 kilos.

    Structured Response:
    {{
        "ruleInstanceName": "sword analysis",
        "Blade length": "90",
        "Grip material": "leather",
        "Weight": "2",
        "Blade material": "steel"
    }}

    Output:{{'score': 0}}

    REMEMBER!! YOUR ANSWER SHOULD BE {{'score': int}} AND THAT IT!
    the defult score is 1. only if you sure it wrong set it to 0.
    
    Our case:
    Free Text:
    {free_text}

    Structured Response:
    {json.dumps(response_dict, indent=2)}
    Output:"""
    return prompt


def validation_prompt_v3(free_text, response_dict):
    prompt = f"""generate only in this shape: {{'score': int}}, where int is 1 for yes, 0 for not.
     your job: is {response_dict} is output of: {free_text}?
     ask yourself: are the `structure output` fields related to the `free text` topics? 
     are the values inside the `structure output` values (not the fields) inside the `free text`?
     only if you absolutely sure they're not the score is 0. otherwise its 1.
     mostly notice the numerical values if they are correct.
     your response:
"""
    return prompt
