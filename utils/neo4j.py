from collections.abc import Mapping


def node_to_json(node: Mapping[str, object]) -> dict[str, object]:
    out: dict[str, object] = {}
    for key, value in node.items():
        iso = getattr(value, "isoformat", None)
        if callable(iso):
            out[key] = iso()
        else:
            out[key] = value
    return out
