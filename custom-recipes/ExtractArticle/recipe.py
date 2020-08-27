from dataiku.customrecipe import get_recipe_config
from utils import apply_func

url_column = get_recipe_config().get("url_column")


def call_api(client, row):
    return client.html.extract_article(row.get(url_column)).dict()


apply_func(call_api)
