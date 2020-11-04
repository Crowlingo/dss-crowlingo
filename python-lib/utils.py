import dataiku
from PyCrowlingo import Client
from dataiku.customrecipe import get_input_names_for_role, get_output_names_for_role, get_recipe_config
import collections


def _generate_unique(name, existing_names, prefix="api"):
    """
    Generate a unique name among existing ones by suffixing a number. Can also add an optional prefix.
    """
    if prefix is not None:
        new_name = prefix + "_" + name
    else:
        new_name = name
    for j in range(1, 1001):
        if new_name not in existing_names:
            return new_name
        new_name = name + "_{}".format(j)
    raise Exception("Failed to generated a unique name")


def _add_prefix(row, res):
    def flatten(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    res = {_generate_unique(k, row.keys()): v for k, v in res.items()}
    for k, v in flatten(res).items():
        row[k] = v
    return row


def _safe_call(client, row, func):
    try:
        return _add_prefix(row, func(client, row))
    except Exception as e:
        print(e)
        row["error"] = str(e)
        return row


def apply_func(func, client=None, input_dataset="input_dataset", output_dataset="output_dataset"):
    input_dataset_name = get_input_names_for_role(input_dataset)[0]
    input_dataset = dataiku.Dataset(input_dataset_name)
    input_df = input_dataset.get_dataframe()

    output_dataset_name = get_output_names_for_role(output_dataset)[0]
    output_dataset = dataiku.Dataset(output_dataset_name)
    client = client or get_client(get_recipe_config())

    output_df = input_df.dropna().apply(lambda row: _safe_call(client, row, func), axis=1)
    output_dataset.write_with_schema(output_df)


def get_client(config):
    api_configuration_preset = config.get("api_configuration_preset")
    if api_configuration_preset is None or api_configuration_preset == {}:
        raise ValueError("Please specify an API configuration preset")
    api_token = api_configuration_preset.get("crowlingo-token")
    api_url = api_configuration_preset.get("crowlingo-url")
    return Client(api_token, url=api_url)
