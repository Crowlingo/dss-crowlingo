from dataiku.customrecipe import get_recipe_config
from utils import apply_func

model_id = get_recipe_config().get("model_id")
model_owner = get_recipe_config().get("model_owner")
prod_version = get_recipe_config().get("prod_version")
text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")
properties = get_recipe_config().get("properties")


def call_api(client, row):
    return client.concepts.extract_custom(model_id, row.get(text_column), lang=row.get(lang_column),
                                          properties=row.get(properties), prod_version=prod_version,
                                          model_owner=model_owner).dict()


apply_func(call_api)
