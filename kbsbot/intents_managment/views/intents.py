from flakon import JsonBlueprint
from flask import request
from kbsbot.intents_managment.knowledge_graph import KGHandler

intents = JsonBlueprint("intents", __name__)
kg = KGHandler()


@intents.route("/intent/requires", methods=["GET"])
def intent_requires():
    """
    This view encapsulates the method get_intent_requirement
    It requires an Intent.

    :return: A dict containing the different entities required for an Intent
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
    This view encapsulates the method get_intent_answer
    It requires an Intent.

    :return: a dict containing the answer template and the different parts of the answer

    .. todo:: inform admin when response is None
    """
    if request.method == "GET":
        data = request.get_json()
        response = kg.get_intent_answer(data["intent"], data["entities"])
        if response is not None:
            return response
        else:
            return {"message": "Answer not configured correctly",
                    "status": 404}

    else:
        return {"message": "method not allowed here",
                "status": 405}


@intents.route("/intent/options", methods=["GET"])
def intent_options():
    """
    This view encapsulates the method get_intent_options.
    It requires an Intent.

    :return: A dict containing the different options to complete an Intent
    """
    if request.method == "GET":
        data = request.get_json()
        result = kg.get_intent_options(data["intent"])
        if result is not None:
            return result
        else:
            return {"message": "Intent not valid", "status": 404}
    else:
        return {"message": "method not allowed here",
                "status": 405}


@intents.route("/entity/options", methods=["GET"])
def entity_options():
    """
    This method encapsulates the method get_entity_options
    It requires an Entity.

    :return: a dict containing the different options to complete an Entity type.

    .. todo:: handle emtpy dicts
    """
    if request.method == "GET":
        data = request.get_json()
        return kg.get_entity_options(data["entity"])
    else:
        return {"message": "method not allowed here",
                "status": 405}
