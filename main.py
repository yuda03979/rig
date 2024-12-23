from src.main import RIG
from fastapi import FastAPI
import os
import ast

app = FastAPI()
rig = RIG()


@app.get("/is_llama_running")
def is_llama_running():
    return rig.is_ollamamia_running()


@app.post("/stop")
def stop():
    return rig.stop()


@app.post("/get_rule_instance")
def get_rule_instance(free_text):
    return rig.predict(free_text)


@app.get("/get_rule_types_names")
def get_rule_types_names():
    return rig.get_rule_types_names()


@app.post("/tweak_rag_parameters")
def tweak_rag_parameters(
        rag_difference=os.getenv("RAG_DIFFERENCE"),
        rag_threshold=os.getenv("RAG_THRESHOLD")
):
    return rig.tweak_rag_parameters(float(rag_threshold), float(rag_difference))


@app.post("/feedback")
def feedback(fb):
    return rig.feedback(fb)
