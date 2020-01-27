from flakon import JsonBlueprint
from flask import request
from kbsbot.intents_managment.knowledge_graph import KGHandler
import os

intents = JsonBlueprint("intents", __name__)


if os.environ.get("DEBUG"):
    base_url = "http://127.0.0.1"
    path = "C:\\Users\\andre\\Documents\\PythonTutos\\cb-intents-management-ms\\kbsbot\\intents_managment\\kg.rdf"
else:
    base_url = os.environ.get("BASE_URL")
    path = os.environ.get("KG_URL")

kg = KGHandler(base_url, path)


@intents.route("/intent/requires", methods=["GET"])
def intent_requires():
    """
    This view encapsulates the method get_intent_requirement
    It requires an Intent.

    :return: A dict containing the different entities required for an Intent
    """

    data = request.get_json()
    if "intent" in data:
        return kg.get_intent_requirements(data["intent"])
    else:
        return {"message": "Must provide an intent name", "status": 404}


@intents.route("/intent/answer", methods=["GET"])
def intent_answer():
    """
    This view encapsulates the method get_intent_answer
    It requires an Intent.

    :return: a dict containing the answer template and the different parts of the answer

    .. todo:: inform admin when response is None
    """

    data = request.get_json()
    if "intent" in data and "entities" in data:
        response = kg.get_intent_answer(data["intent"], data["entities"])
        if response is not None:
            return response
        else:
            return {"message": "Answer not configured correctly",
                    "status": 404}
    else:
        return {"message": "Must provide an Intent and entities",
                "status": 404}


@intents.route("/intent/options", methods=["GET"])
def intent_options():
    """
    This view encapsulates the method get_intent_options.
    It requires an Intent.

    :return: A dict containing the different options to complete an Intent
    """

    data = request.get_json()
    result = kg.get_intent_options(data["intent"])
    if result is not None:
        return result
    else:
        return {"message": "Intent not valid", "status": 404}


@intents.route("/entity/options", methods=["GET"])
def entity_options():
    """
    This method encapsulates the method get_entity_options
    It requires an Entity.

    :return: a dict containing the different options to complete an Entity type.

    .. todo:: handle emtpy dicts
    """

    data = request.get_json()
    if "entity" in data:
        return kg.get_entity_options(data["entity"])
    elif "entities" in data:
        entities = []
        for entity in data["entities"]:
            entities.append(kg.get_entity_options(entity))
        return entities
    else:
        return {"message": "Entity not valid", "status": 404}
