from dataiku.customrecipe import get_recipe_config
from utils import apply_func

text_column = get_recipe_config().get("text_column")
text2_column = get_recipe_config().get("text2_column")
lang_column = get_recipe_config().get("text2_column")
lang2_column = get_recipe_config().get("lang2_column")


def call_api(client, row):
    return client.texts.similarity(row.get(text_column), row.get(text2_column),
                                   lang=row.get(lang_column), lang2=row.get(lang2_column)).dict()


apply_func(call_api)
