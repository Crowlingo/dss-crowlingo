from dataiku.customrecipe import get_recipe_config
from utils import apply_func

text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")
phrase = get_recipe_config().get("phrase")
phrase_lang = get_recipe_config().get("phrase_lang")
precision = get_recipe_config().get("precision")
visualize = get_recipe_config().get("visualize")


def call_api(client, row):
    return client.phrases.match(row.get(text_column), lang=row.get(lang_column),
                                phrase=phrase, phrase_lang=phrase_lang, precision=precision,
                                visualize=visualize).dict()


apply_func(call_api)
