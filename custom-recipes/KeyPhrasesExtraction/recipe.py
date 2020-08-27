from dataiku.customrecipe import get_recipe_config
from utils import apply_func

text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")
limit = get_recipe_config().get("limit")
normalize = get_recipe_config().get("normalize")


def call_api(client, row):
    return client.phrases.extract_keys(row.get(text_column), lang=row.get(lang_column),
                                       limit=limit, normalize=normalize).dict()


apply_func(call_api)
