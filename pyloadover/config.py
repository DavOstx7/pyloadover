CONFIG = {
    "use_full_path_as_namespace": True
}


def is_use_full_path_as_namespace() -> bool:
    return CONFIG["use_full_path_as_namespace"]


def set_use_full_path_as_namespace(use_full_path_namespace: bool):
    CONFIG["use_full_path_as_namespace"] = use_full_path_namespace
