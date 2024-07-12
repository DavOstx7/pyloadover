import typeguard


def is_instance(value, annotation) -> bool:
    try:
        typeguard.check_type(value, annotation)
    except typeguard.TypeCheckError:
        return False
    else:
        return True
