import inspect
import nodes  # ComfyUI's core nodes module

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Dynamically create Icy versions of *concrete node* classes only
for name, obj in inspect.getmembers(nodes, inspect.isclass):
    # Skip private/internal classes
    if name.startswith("_"):
        continue

    # Only wrap real, concrete Comfy node classes:
    # - Must have INPUT_TYPES (so it's a node)
    # - Must have RETURN_TYPES (so server.node_info won't crash)
    if not hasattr(obj, "INPUT_TYPES") or not hasattr(obj, "RETURN_TYPES"):
        continue

    icy_class_name = f"Icy{name}"

    try:
        icy_class = type(icy_class_name, (obj,), {"CATEGORY": "IcyHider"})
    except Exception as e:
        # Don't break ComfyUI if some exotic class misbehaves
        print(f"[ComfyUI-IcyHider] Skipping {name}: {e}")
        continue

    NODE_CLASS_MAPPINGS[icy_class_name] = icy_class
    NODE_DISPLAY_NAME_MAPPINGS[icy_class_name] = f"Icy {name}"
