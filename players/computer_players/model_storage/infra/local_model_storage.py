import os
import json

from players.computer_players.model_storage.infra.base_model_storage import BaseModelStorage

class LocalModelStorage(BaseModelStorage):

    def __init__(self, path: str):
        self.pre_base_path = path

    def _build_local_path(self, path: str):
        return os.path.join(self.pre_base_path, path)

    def save_model(self, path: str, data: bytes) -> None:
        full_path = self._build_local_path(path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(data)

    def load_model(self, path: str) -> bytes:
        full_path = self._build_local_path(path)
        if not os.path.exists(full_path):
            return None
        with open(full_path, "rb") as f:
            return f.read()

    def save_metadata(self, path: str, metadata: dict) -> None:
        full_path = self._build_local_path(path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            json.dump(metadata, f, indent=2)

    def load_metadata(self, path: str) -> dict:
        full_path = self._build_local_path(path)
        if not os.path.exists(full_path):
            return None
        with open(full_path, "r") as f:
            return json.load(f)