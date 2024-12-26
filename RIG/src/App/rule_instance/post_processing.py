from RIG.globals import GLOBALS


def post_processing(type_name, model_response):

    # correct the model_response
    model_response = {k: normalize_empty_value(v) for k, v in model_response.items()}
    schema = GLOBALS.db_manager.get_dict_features(type_name=type_name, feature="schema")
    model_response = correct_numerical_values(schema, model_response)

    # inserting into the rule instance
    default_rule_instance = GLOBALS.db_manager.get_dict_features(type_name, 'default_rule_instance')
    for param in [k for k in default_rule_instance['params'].keys() if  # or: model_response.keys()
                  k not in ["severity", "ruleInstanceName", "ruleInstanceName".lower()]]:
        default_rule_instance['params'][param] = model_response.get(param)
    for param in [k for k in default_rule_instance['params'].keys()if  # or: model_response.keys()
                  k in ["severity", "ruleInstanceName", "ruleInstanceName".lower()]]:
        default_rule_instance[param] = model_response.get(param)
    return default_rule_instance


def normalize_empty_value(value):
    """Normalize empty values to a common representation."""
    if value in [None, '', ' ', " ", "", "null", "None", "none", "empty", "undefined", "nil", "NaN", "nan", "n/a", "N/A", "na", "NA", "missing", "unknown", "void", "blank", ".", "..", "...", "?", "nil"] + ["int", "Int", "String", "string"]:
        return "null"  # Choose a common representation for empty values
    return value


def correct_numerical_values(schema, model_response):
    for k, v in model_response.items():
        if str(schema.get(k)).lower() in ['int', 'int32']:
            try:
                model_response[k] = float(v)
                if int(model_response[k]) == model_response[k]:
                    model_response[k] = int(model_response[k])
            except ValueError:
                model_response[k] = "null"
    return model_response
