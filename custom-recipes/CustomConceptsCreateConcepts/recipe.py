from dataiku.customrecipe import get_recipe_config
from utils import apply_func

id_column = get_recipe_config().get("id_column")
properties_prefix = get_recipe_config().get("properties_prefix")
model_id = get_recipe_config().get("model_id")
model_owner = get_recipe_config().get("model_owner")


def call_api(client, row):
    properties = {k[len(properties_prefix):]: v for k, v in row.items() if k.startswith(properties_prefix)}
    return client.concepts.create_concepts(model_id, model_owner=model_owner,
                                           concepts=[{"id": row.get(id_column), "properties": properties}]).dict()


apply_func(call_api)
