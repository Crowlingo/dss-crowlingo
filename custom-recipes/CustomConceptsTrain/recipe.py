from PyCrowlingo.Errors import ModelNotFound
from dataiku.customrecipe import get_recipe_config
from utils import apply_func, get_client

model_id = get_recipe_config().get("model_id")

id_concepts_column = get_recipe_config().get("id_concepts_column")
properties_prefix = get_recipe_config().get("properties_prefix")

id_labels_column = get_recipe_config().get("id_labels_column")
text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")
concept_id_column = get_recipe_config().get("concept_id_column")
precision_column = get_recipe_config().get("precision_column")


def init_model(client):
    try:
        client.model.clear(model_id)
    except ModelNotFound:
        client.model.create(model_id, "cpt")


def upload_concepts(client, row):
    properties = {k[len(properties_prefix):]: v for k, v in row.items() if k.startswith(properties_prefix)}
    return client.concepts.create_concepts(model_id,
                                           concepts=[
                                               {"id": row.get(id_concepts_column), "properties": properties}]).dict()


def upload_labels(client, row):
    return client.concepts.create_labels(model_id,
                                         labels=[{"id": row.get(id_labels_column), "text": row.get(text_column),
                                                  "lang": row.get(lang_column),
                                                  "concept_id": row.get(concept_id_column),
                                                  "precision": row.get(precision_column)}]).dict()


def train_model(client):
    client.model.train(model_id)
    return str(client.model.wait_training(model_id))


cl_client = get_client(get_recipe_config())

init_model(cl_client)
apply_func(upload_concepts, client=cl_client, input_dataset="concepts_input_dataset",
           output_dataset="concepts_output_dataset")
apply_func(upload_labels, client=cl_client, input_dataset="labels_input_dataset",
           output_dataset="labels_output_dataset")
train_model(cl_client)
