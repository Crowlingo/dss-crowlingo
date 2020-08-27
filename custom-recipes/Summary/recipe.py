from dataiku.customrecipe import get_recipe_config
from utils import apply_func

text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")

ratio = get_recipe_config().get("ratio")
nb_sentences = get_recipe_config().get("nb_sentences")


def call_api(client, row):
    return client.summary.extract(row.get(text_column), lang=row.get(lang_column),
                                  ratio=ratio, nb_sentences=nb_sentences).dict()


apply_func(call_api)
