from RIG import rule_instance_generator
from fastapi import FastAPI
from dotenv import find_dotenv, load_dotenv
import os
import ast
load_dotenv(find_dotenv())


app = FastAPI()


rig = rule_instance_generator.RuleInstanceGenerator()

@app.post("/get_rule_instance")
def get_rule_instance(free_text):
    return rig.get_rule_instance(free_text)


@app.get("/get_rule_types_names")
def get_rule_types_names():
    return rig.get_rule_types_names()


@app.post("/set_rule_types")
def set_rule_types():
    return rig.add_rule_types_from_folder()


@app.post("/tweak_rag_parameters")
def tweak_rag_parameters(
        rag_difference=os.getenv("RAG_DIFFERENCE"),
        rag_threshold=os.getenv("RAG_THRESHOLD")
):
    return rig.tweak_rag_parameters(float(rag_threshold), float(rag_difference))

@app.post("/feedback")
def feedback(fb):
    return rig.feedback(fb)


@app.post("/evaluate")
def evaluate(
        start_point=0,
        end_point=2,  # None - all the data
        sleep_time_each_10_iter=30,
        batch_size=250
):
    print("evaluate")
    try:
        end_point = int(end_point)
    except:
        pass
    return rig.evaluate(
        start_point=int(start_point),
        end_point=end_point,  # None - all the data
        sleep_time_each_10_iter=int(sleep_time_each_10_iter),
        batch_size=int(batch_size)
    )


