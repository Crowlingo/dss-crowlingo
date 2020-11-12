from PyCrowlingo.Errors import ModelNotFound
from dataiku.customrecipe import get_recipe_config
from utils import apply_func, get_client

text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")
class_id_column = get_recipe_config().get("class_id_column")
id_column = get_recipe_config().get("id_column")

model_id = get_recipe_config().get("model_id")

model_type = get_recipe_config().get("model_type")
train_ratio = get_recipe_config().get("train_ratio")


def init_model(client):
    try:
        client.model.clear(model_id)
    except ModelNotFound:
        client.model.create(model_id, "clf")


def call_api(client, row):
    return client.classifier.create_documents(model_id, documents=[{"text": row.get(text_column),
                                                                    "lang": row.get(lang_column),
                                                                    "class_id": row.get(class_id_column),
                                                                    "id": row.get(id_column)}]).dict()


def train_model(client):
    client.model.train(model_id, model_type=model_type,
                       model_config={"train_ratio": train_ratio})
    return str(cl_client.model.wait_training(model_id))


cl_client = get_client(get_recipe_config())

init_model(cl_client)
apply_func(call_api, client=cl_client)
train_model(cl_client)
