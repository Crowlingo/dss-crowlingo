from dataiku.customrecipe import get_recipe_config
from utils import apply_func

text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")
id_column = get_recipe_config().get("id_column")
answer_id_column = get_recipe_config().get("answer_id_column")
variation_prefix = get_recipe_config().get("variation_prefix")

model_id = get_recipe_config().get("model_id")
model_owner = get_recipe_config().get("model_owner")


def call_api(client, row):
    variations = {k[len(variation_prefix):]: v for k, v in row.items() if k.startswith(variation_prefix)}
    return client.faq.create_questions(model_id, questions=[{"id": row.get(id_column), "variations": variations,
                                                             "answer_id": row.get(answer_id_column)}],
                                       model_owner=model_owner).dict()


apply_func(call_api)
