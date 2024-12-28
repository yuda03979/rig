# getting started

### this is NOT for the docker - see README.Docker

----------------------
# Installation

ollama:
- for linux:
```angular2html
curl -fsSL https://ollama.com/install.sh | sh
```
- for other os check ollama website.
-------------
-------------
lfs:
```angular2html
git lfs install
```
- or:
```angular2html
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt install git-lfs
```

if using the package and not the docker:
## - downlads (if using internet):
gemma:
```
curl -L -O https://huggingface.co/lmstudio-community/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q8_0.gguf
```
rag:
```
git clone https://huggingface.co/BAAI/bge-m3
```


## how to use:
on the terminal run
```angular2html
ollama serve
```

now lets load our gguf models into ollama using dockerfile:
- download the rig_modelfile directory
```angular2html
link
```
now, since i assume your 'models directory' in ollama set properly, you should run:
```
import subprocess
import os

def create_models_from_gguf_NOT_docker():
    """
        create the models on your computer
        IMPORTANT!!! if you using windows, you should change in the modelfile the FROM section into a correct path.
    """
    modelfile_location = "/Users/yuda/PycharmProjects/RIG_v2/rig_modelfiles"

    commands = [
        f"ollama create gemma-2-2b-it-Q8_0:rig -f {os.path.join(modelfile_location, 'gemma-2-2b-it-Q8_0')}",
        f"ollama create snowflake-arctic-embed-137m:rig -f {os.path.join(modelfile_location, 'snowflake-arctic-embed-m-long-F16')}"
    ]
    

    for command in commands:
        try:
            print(f"Running: {command}")
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error running {command}: {e.stderr}")

create_models_from_gguf_NOT_docker()
```
- and you finished.

-----------
# how to use
```python
from RIG.rule_instance_generator import RuleInstanceGenerator
```


```python
# (required means that you can chnge it in globlas.py and it will not be required.)

rig = RuleInstanceGenerator()
```

```
rig.add_rule_types_from_folder()
```
```python
# get list of existing rule types:
rig.get_rule_types_names()
```
 ['missile malfunction',
  'tactical error',
  'missile failure',
  'launch failure',
  'platoon report',
  'moral failure',
  'encryption flaw',
  'espionage suspect',
  'corruption scandal',
  'betrayal risk',
  'leadership breakdown',
  'radar error monitoring',
  'personnel sabotage',
  'satellite disruption',
  'bomb failure',
  'defection threat',
  'attack overview',
  'fire control',
  'disloyal soldier',
  'equipment malfunction',
  'command incompetence',
  'supply shortage',
  'system failure',
  'covert agent',
  'suspected person']



## get rule instance from free text


```python
free_text = "Alright, let's dive in. We're looking at 'Exploitation Scenario 789'. The crux of the matter is, there's this individual, going by the ID 'XYZ789', who's been involved in an exploitation failure. The level of seriousness? I'd estimate about three. The breach? Fairness. Not good, not good at all. When did we spot this? Well, the detection time isn't clear. And the context? Personal. Yes, it's a pretty serious situation"

response = rig.get_rule_instance(free_text) # return dictionary
```


```python
response.keys()
```

dict_keys(['rule_instance', 'error', 'error_message', 'free_text', 'type_name', 'rag_score', 'model_response', 'schema', 'time', 'inference_time'])




```python
response["rule_instance"] # the package response
```


output:

    {'_id': '00000000-0000-0000-0000-000000000000',
     'description': 'string',
     'isActive': True,
     'lastUpdateTime': '00/00/0000 00:00:00',
     'params': {'individualID': 'XYZ789',
      'failureType': 'Fairness',
      'detectionTime': 'null',
      'ethicalViolation': 'null',
      'context': 'Personal'},
     'ruleInstanceName': 'Exploitation Scenario 789',
     'severity': 3,
     'ruleType': 'structured',
     'ruleOwner': '',
     'ruleTypeId': '7a2f6c94-2b4f-4d9d-8a77-d11f7c7cc8fc',
     'eventDetails': [{'objectName': 'Moral',
       'objectDescription': None,
       'timeWindowInMilliseconds': 0,
       'useLatest': False}],
     'additionalInformation': {},
     'presetId': '00000000-0000-0000-0000-000000000000'}




```python
# giving us feedback on the response. it will help us to improve the project. it stores in .logs file, without internet connection.
rig.feedback(rig_response=response, good=True)
  # or 0.8, or what ever you can  
```
thank you :)


## run evaluation:
```
rig.evaluate(
    start_point=0,
    end_point=2,  # -1 or None - all the data
    sleep_time_each_10_iter=5,
    batch_size=250
)
```
