
# Project Setup and Deployment Guide

## important!!!
- it will run slow on windows and mac, since docker is on vm
- linux its ok and fast.

### Installation Requirements
- lfs (for large file handling)
- Docker
- Docker Compose

## Setup Steps

-----------------
### 1. gguf files and modelfiles download:
(for making ollama-models)

download the rig_modelfiles folder from drive. 
```angular2html
https://drive.google.com/drive/folders/1Jm97UnsVPvk_QpjnZi7ItNHHuqXsPhGq
```
- its important that the gguf and the modelfiles will be on the same directory.


###### place this on the .env as GGUF_AND_MODELFILE_LOCATION

----------------
### 2. Configuration

#### Environment Configuration
1. edit the `.env` file
2. Update paths and settings as required
3. Ensure all necessary environment variables are set correctly

## Running the Application

install docker
```
sudo snap install docker  
```

install docker compose
```
sudo apt-get install docker-compose-plugin
```
or:
```angular2html
sudo curl -L "https://github.com/docker/compose/releases/download/v2.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```
output: ```Docker Compose version v2.29.1```
### Local Development
Navigate to the project directory and run:
```bash
docker compose build
```
```angular2html
docker compose up
```

The application will be accessible at: http://localhost:8000/docs

## Additional Resources
- [Docker's Python Guide](https://docs.docker.com/language/python/)
- [Docker Getting Started - Sharing](https://docs.docker.com/go/get-started-sharing/)


## the models:
after the project is up on docker, 
you can load the gguf models into ollama form using modelfiles
```angular2html
import subprocess
import os

def create_models_from_gguf_docker():
    """
        create from gguf and modelfile an ollama-model. (see more on ollama website)
        the names of the models match the name in the globals. so dont change that.
    """
    container_name = "ollama_rig"  # if theres 2 ollama containers (possible because they dont on the same networks) put here the container id.
    modelfile_location = "/root/rig_models"  # do not change! its suitable also for windows. its the path in the ollama docker container

    # Paths inside the ollama container (use mounted paths)
    commands = [
        f"docker exec {container_name} ollama create gemma-2-2b-it-Q8_0:rig -f {os.path.join(modelfile_location, 'gemma-2-2b-it-Q8_0')}",
        f"docker exec {container_name} ollama create snowflake-arctic-embed-137m:rig -f {os.path.join(modelfile_location, 'snowflake-arctic-embed-m-long-F16')}"
    ]
    

    for command in commands:
        try:
            print(f"Running: {command}")
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error running {command}: {e.stderr}")

create_models_from_gguf_docker()
```

- IMPORTANT!! you should do it only one time. you dont need to do it every time.

# how to use:
(you also have how_to_docker.ipynb for python functions.)
- functions:
1. get_rule_instance
```
  curl -X 'POST' \
  'http://0.0.0.0:8000/get_rule_instance?free_text=system%20failure%20severity%205' \
  -H 'accept: application/json' \
  -d ''
```
output:
{"rule_instance":{"_id":"00000000-0000-0000-0000-000000000000","description":"string","isActive":true,"lastUpdateTime":"00/00/0000 00:00:00","params":{"speed":"null","type":"null","weight":"null","fuel":"null","altitute":"null","wheels":"null","engine":"null"},"ruleInstanceName":"system failure - system failure","severity":5,"ruleType":"structured","ruleOwner":"","ruleTypeId":"fb8e8ef1-e382-43b5-b896-70d254878751","eventDetails":[{"objectName":"Airplan","objectDescription":null,"timeWindowInMilliseconds":0,"useLatest":false}],"additionalInformation":{},"presetId":"00000000-0000-0000-0000-000000000000"},"is_error":false,"error_message":"","free_text":"system failure severity 5","type_name":"system failure","rag_score":0.6298588514328003,"model_response":"```json\n    {\"speed\": null, \"type\": \"null\", \"weight\": null, \"fuel\": null, \"altitute\": null, \"wheels\": null, \"engine\": null, \"ruleInstanceName\": \"system failure - system failure\", \"severity\": 5}","schema":{"speed":"Int","type":"String","weight":"Int","fuel":"Int","altitute":"Int","wheels":"Int","engine":"Int","ruleInstanceName":"string","severity":"int"},"time":"2024-12-08|11:12:02","inference_time":15.802719354629517}%

3. get_rule_types_names
```angular2html
  curl -X 'GET' \
  'http://0.0.0.0:8000/get_rule_types_names' \
  -H 'accept: application/json'
```
output:
["missile malfunction","missile failure","launch failure","platoon report","encryption flaw","corruption scandal","betrayal risk","leadership breakdown","satellite disruption","bomb failure","defection threat","attack overview","fire control","disloyal soldier","command incompetence","supply shortage","system failure","covert agent","suspected person","radar error monitoring","api throttling","temperature overload","disk space warning","memory usage alert","equipment malfunction","password expiry","temperature threshold exceeded"]%

4. tweak_rag_parameters
```angular2html
curl -X 'POST' \
  'http://0.0.0.0:8000/tweak_rag_parameters?rag_difference=0.002&rag_threshold=0.5' \
  -H 'accept: application/json' \
  -d ''
```
output:
true

5. set_rule_types 
```
curl -X POST "http://0.0.0.0:8000/set_rule_types" \
-H "accept: application/json"
```

6. feedback:
```angular2html
curl -X 'POST' \
  'http://0.0.0.0:8000/feedback?rig_response={}&good=True \
  -H 'accept: application/json' \
  -d ''
```
output:
thank you :)
7. evaluate:
```
curl -X 'POST' \
  'http://0.0.0.0:8000/evaluate?start_point=0&end_point=2&sleep_time_each_10_iter=30&batch_size=250' \
  -H 'accept: application/json' \
  -d ''
```

