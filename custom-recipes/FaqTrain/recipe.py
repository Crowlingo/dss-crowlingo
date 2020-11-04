from PyCrowlingo.Errors import ModelNotFound
from dataiku.customrecipe import get_recipe_config
from utils import apply_func, get_client

answers_id_column = get_recipe_config().get("answers_id_column")
variation_prefix = get_recipe_config().get("variation_prefix")

questions_id_column = get_recipe_config().get("questions_id_column")
answer_id_column = get_recipe_config().get("answer_id_column")

model_id = get_recipe_config().get("model_id")


def init_model(client):
    try:
        client.model.clear(model_id)
    except ModelNotFound:
        client.model.create(model_id, "faq")


def upload_answers(client, row):
    variations = {k[len(variation_prefix):]: v for k, v in row.items() if k.startswith(variation_prefix)}
    return client.faq.create_answers(model_id, answers=[{"id": row.get(answers_id_column),
                                                         "variations": variations}]).dict()


def upload_questions(client, row):
    variations = {k[len(variation_prefix):]: v for k, v in row.items() if k.startswith(variation_prefix)}
    return client.faq.create_questions(model_id, questions=[{"id": row.get(questions_id_column),
                                                             "variations": variations,
                                                             "answer_id": row.get(answer_id_column)}]).dict()


def train_model(client):
    client.model.train(model_id)
    return str(client.model.wait_training(model_id))


cl_client = get_client(get_recipe_config())


init_model(cl_client)
apply_func(upload_answers, client=cl_client, input_dataset="answers_input_dataset",
           output_dataset="answers_output_dataset")
apply_func(upload_questions, client=cl_client, input_dataset="questions_input_dataset",
           output_dataset="questions_output_dataset")
train_model(cl_client)


