"""GPU backend shell. Importing this file does not load torch or any model."""
class HFQwenBackend:
    def __init__(self, model_path, adapter_path=None):
        raise NotImplementedError("Complete after inspecting the installed Qwen3-VL processor and available GPU memory.")
