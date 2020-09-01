from dataiku.customrecipe import get_recipe_config
from utils import apply_func

text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")
model_id = get_recipe_config().get("model_id")
prod_version = get_recipe_config().get("prod_version")
model_owner = get_recipe_config().get("model_owner")


def call_api(client, row):
    res = client.classifier.classify(model_id, row.get(text_column), lang=row.get(lang_column),
                                      prod_version=prod_version, model_owner=model_owner).dict()
    print(res)
    return res


apply_func(call_api)
