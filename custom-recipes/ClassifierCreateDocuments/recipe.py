from dataiku.customrecipe import get_recipe_config
from utils import apply_func

text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")
class_id_column = get_recipe_config().get("class_id_column")
id_column = get_recipe_config().get("id_column")

model_id = get_recipe_config().get("model_id")
model_owner = get_recipe_config().get("model_owner")


def call_api(client, row):
    return client.classifier.create_documents(model_id, documents=[{"text": row.get(text_column),
                                                                    "lang": row.get(lang_column),
                                                                    "class_id": row.get(class_id_column),
                                                                    "id": row.get(id_column)}],
                                              model_owner=model_owner).dict()


apply_func(call_api)
