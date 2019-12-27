from flakon import JsonBlueprint
from flask import request
from kbsbot.intents_managment.knowldege_graph import KGHandler

intents = JsonBlueprint("intents", __name__)
kg = KGHandler()


@intents.route("/intent/requires", methods=["GET"])
def intent_requires():
    """
    intent
    """
    if request.method == "GET":
        data = request.get_json()
        if "intent" not in data:
            return {"message": "Must provide an intent name", "status": 404}
        return kg.get_intent_requirements(data["intent"])
    else:
        return {"message": "method not allowed here",
                "status": 405}


@intents.route("/intent/answer", methods=["GET"])
def intent_answer():
    """
    intent
    """
    if request.method == "GET":
        data = request.get_json()
        response = kg.get_intent_answer(data["intent"], data["entities"])
        if response is not None:
            return response
        else:
            #         TODO inform admin
            return {"message": "Answer not configured correctly",
                    "status": 404}

    else:
        return {"message": "method not allowed here",
                "status": 405}


@intents.route("/entity/options", methods=["GET"])
def entity_options():
    """
    Entity
    """
    if request.method == "GET":
        data = request.get_json()
        return {"type": "Curso", "options": ["Option1", "Option1", "Option1"]}
    else:
        return {"message": "method not allowed here",
                "status": 405}


@intents.route("/entity/", methods=["GET"])
def get_entity():
    """
    Entity isntance
    """
    if request.method == "GET":
        data = request.get_json()
        return {"entity": "entity", "property": "value"}
    else:
        return {"message": "method not allowed here",
                "status": 405}
