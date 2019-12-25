from flakon import JsonBlueprint


intents = JsonBlueprint('intents', __name__)


@intents.route('/')
def index():
    """Home view.

    This view will return an empty JSON mapping.
    """
    return {}
