import dataiku
from PyCrowlingo import Client
from dataiku.customrecipe import get_input_names_for_role, get_output_names_for_role, get_recipe_config
import collections


def _add_prefix(prefix, row, res):
    def flatten(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    if prefix:
        res = {f"{prefix}_{k}": v for k, v in res.items()}
    for k, v in flatten(res).items():
        row[k] = v
    return row


def apply_func(func):
    input_dataset_name = get_input_names_for_role("input_dataset")[0]
    input_dataset = dataiku.Dataset(input_dataset_name)
    input_df = input_dataset.get_dataframe()

    output_dataset_name = get_output_names_for_role("output_dataset")[0]
    output_dataset = dataiku.Dataset(output_dataset_name)

    api_configuration_preset = get_recipe_config().get("api_configuration_preset")
    if api_configuration_preset is None or api_configuration_preset == {}:
        raise ValueError("Please specify an API configuration preset")
    api_token = api_configuration_preset.get("crowlingo-api-token")

    client = Client(api_token)

    result_prefix = get_recipe_config().get("result_prefix")

    output_df = input_df.dropna().apply(lambda row: _add_prefix(result_prefix, row, func(client, row)), axis=1)
    output_dataset.write_with_schema(output_df)
