import os
import json

from players.computer_players.model_storage.infra.base_model_storage import BaseModelStorage

class LocalModelStorage(BaseModelStorage):

    def save_model(self, path: str, data: bytes) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)

    def load_model(self, path: str) -> bytes:
        with open(path, "rb") as f:
            return f.read()

    def save_metadata(self, path: str, metadata: dict) -> None:
        with open(path, "w") as f:
            json.dump(metadata, f, indent=2)

    def load_metadata(self, path: str) -> dict:
        with open(path, "r") as f:
            return json.load(f)