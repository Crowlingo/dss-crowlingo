from dataiku.customrecipe import get_recipe_config
from utils import apply_func

text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")
id_column = get_recipe_config().get("id_column")
variation_prefix = get_recipe_config().get("variation_prefix")

model_id = get_recipe_config().get("model_id")
model_owner = get_recipe_config().get("model_owner")


def call_api(client, row):
    variations = {k[len(variation_prefix):]: v for k, v in row.items() if k.startswith(variation_prefix)}
    return client.faq.create_answers(model_id, answers=[{"id": row.get(id_column), "variations": variations}],
                                     model_owner=model_owner).dict()


apply_func(call_api)
