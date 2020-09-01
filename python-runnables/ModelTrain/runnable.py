# This file is the actual code for the Python runnable ClassificationTrain
from dataiku.runnables import Runnable
from utils import get_client


class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config

    @staticmethod
    def get_progress_target():
        """
        If the runnable will return some progress info, have this function return a tuple of
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return None

    def run(self, progress_callback):
        """
        Do stuff here. Can return a string or raise an exception.
        The progress_callback is a function expecting 1 value: current progress
        """
        client = get_client(self.config)
        client.model.train(self.config["model_id"], model_owner=self.config.get("model_owner"),
                           model_type=self.config.get("model_type"))
        return str(client.model.wait_training(self.config["model_id"]))
