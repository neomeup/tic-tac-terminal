class BaseModelStorage:

    def save_model(self, path: str, data: bytes) -> None:
        raise NotImplementedError

    def load_model(self, path: str) -> bytes:
        raise NotImplementedError

    def save_metadata(self, path: str, metadata: dict) -> None:
        raise NotImplementedError

    def load_metadata(self, path: str) -> dict:
        raise NotImplementedError