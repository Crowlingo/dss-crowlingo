from dataiku.customrecipe import get_recipe_config
from utils import apply_func

text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")
model_id = get_recipe_config().get("model_id")
variations = get_recipe_config().get("variations")
limit = get_recipe_config().get("limit")
prod_version = get_recipe_config().get("prod_version")
model_owner = get_recipe_config().get("model_owner")


def call_api(client, row):
    return client.faq.search(model_id, row.get(text_column), lang=row.get(lang_column), variations=variations,
                             limit=limit, prod_version=prod_version, model_owner=model_owner).dict()


apply_func(call_api)
