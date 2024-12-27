from RIG.globals import GLOBALS


def post_processing(type_name: str, model_response: dict) -> dict:
    """
    Perform post-processing on the model response to integrate it into the rule instance.

    This function normalizes empty values, corrects numerical data types based on schema,
    and updates the default rule instance with the processed parameters.

    Parameters:
        type_name (str): The type name of the rule.
        model_response (dict): The model's response containing key-value pairs to process.

    Returns:
        dict: The updated default rule instance with corrected values.
    """
    # Normalize empty values in the model response
    model_response = {
        key: normalize_empty_value(value)
        for key, value in model_response.items()
    }

    # Retrieve schema and correct numerical values
    schema = GLOBALS.db_manager.get_dict_features(
        type_name=type_name, feature="schema"
    )
    model_response = correct_numerical_values(schema, model_response)

    # Retrieve the default rule instance
    default_rule_instance = GLOBALS.db_manager.get_dict_features(
        type_name, 'default_rule_instance'
    )

    # Update params excluding specific keys
    for param in [
        key for key in model_response.keys()
        if key not in ["severity", "ruleInstanceName", "ruleinstancename"]
    ]:
        default_rule_instance['params'][param] = model_response.get(param)

    # Update severity and rule instance name directly
    for param in [
        key for key in model_response.keys()
        if key in ["severity", "ruleInstanceName", "ruleinstancename"]
    ]:
        default_rule_instance[param] = model_response[param]

    return default_rule_instance


def normalize_empty_value(value: str) -> str:
    """
    Normalize empty or undefined values to a common representation ("null").

    This function checks for various forms of empty or invalid data and replaces them
    with the string "null" to ensure consistent data handling.

    Parameters:
        value (str): The input value to normalize.

    Returns:
        str: "null" if the value is empty or invalid, otherwise returns the original value.
    """
    empty_values = [
        None, '', ' ', "null", "None", "none", "empty", "undefined", "nil",
        "NaN", "nan", "n/a", "N/A", "na", "NA", "missing", "unknown", "void",
        "blank", ".", "..", "...", "?", "int", "Int", "String", "string"
    ]

    # Return "null" if the value is in the list of empty representations
    if value in empty_values:
        return "null"

    return value


def correct_numerical_values(schema: dict, model_response: dict) -> dict:
    """
    Correct numerical values in the model response based on the schema.

    This function ensures that values corresponding to keys marked as integers
    in the schema are converted to int or float. If conversion fails, the value
    is set to "null".

    Parameters:
        schema (dict): A dictionary representing the schema with expected data types.
        model_response (dict): A dictionary representing the model's response.

    Returns:
        dict: The corrected model response with numerical values appropriately converted.
    """
    for key, value in model_response.items():
        # Check if the schema defines the key as an integer type
        if str(schema.get(key)).lower() in ['int', 'int32']:
            try:
                # Attempt to convert the value to float first
                model_response[key] = float(value)

                # If the float value has no decimal part, convert to int
                if int(model_response[key]) == model_response[key]:
                    model_response[key] = int(model_response[key])

            except ValueError:
                # If conversion fails, set value to "null"
                model_response[key] = "null"

    return model_response