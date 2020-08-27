from dataiku.customrecipe import get_recipe_config
from utils import apply_func

text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")
properties = get_recipe_config().get("properties")
split = get_recipe_config().get("split")
precision = get_recipe_config().get("precision")


def call_api(client, row):
    return client.concepts.extract(row.get(text_column), lang=row.get(lang_column),
                                   precision=row.get(precision), properties=row.get(properties),
                                   split=row.get(split)).dict()


apply_func(call_api)
