import dataiku
from PyCrowlingo import Client
from dataiku.customrecipe import get_input_names_for_role, get_output_names_for_role, get_recipe_config

input_dataset_name = get_input_names_for_role("input_dataset")[0]
input_dataset = dataiku.Dataset(input_dataset_name)
input_df = input_dataset.get_dataframe()

output_dataset_name = get_output_names_for_role("output_dataset")[0]
output_dataset = dataiku.Dataset(output_dataset_name)

text_column = get_recipe_config().get("text_column")
lang_column = get_recipe_config().get("lang_column")


api_configuration_preset = get_recipe_config().get("api_configuration_preset")
if api_configuration_preset is None or api_configuration_preset == {}:
    raise ValueError("Please specify an API configuration preset")
api_token = api_configuration_preset.get("crowlingo-api-token")

client = Client(api_token)


def call_api(row):
    print(row)
    row["entities"] = client.entities.extract(text=row.get(text_column), lang=row.get(lang_column))
    return row


output_df = input_df.apply(call_api, axis=1)

output_dataset.write_with_schema(output_df)
