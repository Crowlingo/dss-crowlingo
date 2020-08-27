from dataiku.customrecipe import get_recipe_config
from utils import apply_func

text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")
visualize = get_recipe_config().get("visualize")


def call_api(client, row):
    return client.syntax.extract(row.get(text_column), lang=row.get(lang_column), visualize=visualize).dict()


apply_func(call_api)
