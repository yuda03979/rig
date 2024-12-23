def prompt_json_gemma_v6(free_text, type_name, schema, description, examples=None):
    if not examples:
        examples = {
            "example_1": {
                "free_text": "Please generate a Weather Alert - other for area code 2001. Alert type is Thunderstorm. Intensity: severe. Urgency: high. Ignore the forecast source for now. The duration of this case, I'd say, is around two. severity is empty or unclear",
                "schema": str({"alertType": "string", "areaCode": "int", "intensity": "string", "urgency": "string", "forecastSource": "string", "duration": "int", "ruleInstanceName": "string", "severity": "int"}),
                "description": str({}),
                "response": str({"alertType": "Thunderstorm", "areaCode": 2001, "intensity": "severe", "urgency": "high", "forecastSource": "null", "duration": 2, "ruleInstanceName": "Weather Alert - other", "severity": "null"})
            },
            "example_2": {
                "free_text": "Add a report for 'Shell Delay'. Equipment Malfunction case. Type: shell. Site is not important. Malfunction at level five, urgency four. Desc: Detonation delayed in poland Severity i think 3",
                "schema": str({"type": "string", "site": "string", "malfunctionLevel": "int", "urgency": "int", "description": " string", "ruleInstanceName": "string", "severity": "int"}),
                "description": str({}),
                "response": str({"type": "shell", "site": "empty", "malfunctionLevel": 5, "urgency": 4, "description": "Detonation delayed in poland", "ruleInstanceName": "Equipment Malfunction - Shell Delay", "severity": 3}),
            }
        }

    use_examples = f"""
    ### Example 1 (Similar Style Example):
    Schema:
    {examples["example_1"]["schema"]}
    Free text:
    {examples["example_1"]["free_text"]}
    Output:
    {examples["example_1"]["response"]}
    
    ### Example 2 (Closest Task Match) :
    Schema:
    {examples["example_2"]["schema"]}
    Free text:
    {examples["example_2"]["free_text"]}
    Output:
    {examples["example_2"]["response"]}
        """

    prompt = f"""
    Extract information from the provided text and format it according to the given JSON schema. Follow these strict guidelines:
    1. *Only use fields explicitly listed in the schema below.* Ignore any fields mentioned in the text or context that are not in the schema.
    2. *Do not add or infer fields.* If a field is not mentioned in the schema, it must be excluded from the output.
    3. *For missing fields in the schema, set their value to "null" (with quotes).*
    {use_examples}

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
    return prompt