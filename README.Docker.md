
# Project Setup and Deployment Guide

## important!!!
- it will run slow on windows and mac, since docker is on vm
- linux its ok and fast.

### Installation Requirements
- lfs (for large file handling)
- Docker
- Docker Compose


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

## - downlads (if using internet):
gemma:
```
curl -L -O https://huggingface.co/lmstudio-community/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q8_0.gguf
```
rag:
```
https://huggingface.co/yixuan-chia/snowflake-arctic-embed-m-long-GGUF/resolve/main/snowflake-arctic-embed-m-long-F16.gguf?download=true
```
and place them in the rig_modelfile directory (or change the path inside the modelfile. for docker its better they're together. and you can delete the file after - just keep the directory) 

but you also can download the models from the drive (there is also the modelfiles)
```angular2html
https://drive.google.com/drive/folders/1Jm97UnsVPvk_QpjnZi7ItNHHuqXsPhGq
```

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
make the ollama models. 
in the load_gguf_modelfile.ipynb run the first cell.
- notice that you only need to do it once, and you also can delete the directory after (just keep the directory empty) 

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
  'http://0.0.0.0:8000/feedback?rig_response=rig_response&good=True \
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

