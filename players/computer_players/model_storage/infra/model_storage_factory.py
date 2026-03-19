

from players.computer_players.model_storage.infra.local_model_storage import LocalModelStorage
from players.computer_players.model_storage.infra.s3_model_storage import S3ModelStorage


class ModelStorageFactory:

    @staticmethod
    def create(config):

        model_storage_type = config.model_storage_backend

        if model_storage_type == "local":
            return LocalModelStorage()

        elif model_storage_type == "s3":
            return S3ModelStorage()

        elif model_storage_type is None:
            return None

        else:
            raise ValueError(f"Unknown storage backend: {model_storage_type}")