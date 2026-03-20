


class ModelPathBuilder:

    @staticmethod
    def build_paths(config, player_id: int, checkpoint: str | None = None) -> dict:

        agent_name = config.agent_type[player_id]
        version = config.model_version[player_id]

        base = f"{agent_name}/{version}"

        if checkpoint:
            base = f"{base}/checkpoints/{checkpoint}"

        return {
            "model": f"{base}/model.pt",
            "metadata": f"{base}/metadata.json"
        }