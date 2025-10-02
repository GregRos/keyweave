def get_attrs_down_to(
    target: object, base: type, *, resolve_descriptors: bool = True
):
    attrs = dict[str, object]()
    for cls in target.__class__.mro():
        if cls is base:
            break
        for key, value in cls.__dict__.items():
            if key not in attrs:
                attrs[key] = (
                    getattr(target, key) if resolve_descriptors else value
                )

    return attrs
