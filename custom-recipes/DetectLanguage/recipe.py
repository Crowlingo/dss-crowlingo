from dataiku.customrecipe import get_recipe_config
from utils import apply_func

text_column = get_recipe_config().get("text_column")


def call_api(client, row):
    return client.languages.detect(row.get(text_column)).dict()


apply_func(call_api)
