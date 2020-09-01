from dataiku.customrecipe import get_recipe_config
from utils import apply_func

id_column = get_recipe_config().get("id_column")
text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")
concept_id_column = get_recipe_config().get("concept_id_column")
precision_column = get_recipe_config().get("precision_column")
model_id = get_recipe_config().get("model_id")
model_owner = get_recipe_config().get("model_owner")


def call_api(client, row):
    return client.concepts.create_labels(model_id, model_owner=model_owner,
                                         labels=[{"id": row.get(id_column), "text": row.get(text_column),
                                                  "lang": row.get(lang_column),
                                                  "concept_id": row.get(concept_id_column),
                                                  "precision_column": row.get(precision_column)}]).dict()


apply_func(call_api)
