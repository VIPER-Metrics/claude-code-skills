import os
import sys
import re
import yaml
from bs4 import BeautifulSoup, NavigableString, Tag


# --------------------------------------------
# CONFIG
# --------------------------------------------

NUI_TAG_MAPPINGS = {
    "button": "Button",
    "input": "TextBox",
    "textarea": "TextArea",
    "a": "Link",
    "img": "Image",
}


# --------------------------------------------
# YAML SAFETY
# --------------------------------------------

def make_yaml_safe(obj):
    if isinstance(obj, dict):
        return {str(k): make_yaml_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_yaml_safe(v) for v in obj]
    elif isinstance(obj, tuple):
        return [make_yaml_safe(v) for v in obj]
    elif isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    else:
        return str(obj)


# --------------------------------------------
# CSS PARSING (unchanged)
# --------------------------------------------

def extract_css_blocks(css_content):
    css_content = re.sub(r"/\*.*?\*/", "", css_content, flags=re.DOTALL)
    blocks, stack, current = [], [], ""

    for c in css_content:
        current += c
        if c == "{":
            stack.append("{")
        elif c == "}":
            if stack:
                stack.pop()
            if not stack:
                blocks.append(current.strip())
                current = ""

    if current.strip():
        blocks.append(current.strip())

    return blocks


def process_css_block(block, preset_map, stylesheet):
    block = block.strip()
    if not block:
        return

    if block.startswith("@"):
        stylesheet.append(block)
        return

    m = re.match(r"([^{]+)\s*{(.*)}$", block, flags=re.DOTALL)
    if m:
        selectors = m.group(1).strip().split(",")
        css_rules = m.group(2).strip()

        for sel in selectors:
            sel = sel.strip()
            if sel.startswith("."):
                name = sel[1:].split(":", 1)[0]
                preset_map[name] = css_rules
            else:
                stylesheet.append(f"{sel} {{ {css_rules} }}")


# --------------------------------------------
# HTML PARSING
# --------------------------------------------

def parse_html_element(el):
    if isinstance(el, NavigableString):
        text = str(el).strip()
        if text:
            return {
                "html_tag": "span",
                "text": text,
                "children": []
            }
        return None

    if not isinstance(el, Tag):
        return None

    if el.name in ["script", "style"]:
        return None

    preset = list(el.get("class", [])) if el.get("class") else []

    event_bindings = {}
    raw_attrs = []
    force_container = False
    explicit_name = None

    for k, v in el.attrs.items():

        if k == "class":
            continue

        if k == "style":
            continue

        # ----------------------------------
        # anvil-var
        # ----------------------------------
        if k == "anvil-var":
            explicit_name = str(v)
            continue

        # ----------------------------------
        # anvil-event-click
        # ----------------------------------
        if k.startswith("anvil-event-"):
            event_name = k.replace("anvil-event-", "")
            event_bindings[event_name] = str(v)
            continue

        # ----------------------------------
        # anvil-is-container
        # ----------------------------------
        if k == "anvil-is-container":
            force_container = True
            continue

        # ----------------------------------
        # normal attribute
        # ----------------------------------
        if isinstance(v, list):
            v = " ".join(str(x) for x in v)

        raw_attrs.append(f"{str(k)}: {str(v)}")

    node = {
        "html_tag": str(el.name.lower()),
        "css": str(el.get("style", "")),
        "preset": preset,
        "attributes": raw_attrs,
        "text": "",
        "children": [],
        "_event_bindings": event_bindings,
        "_force_container": force_container,
        "_explicit_name": explicit_name
    }

    for child in el.children:
        parsed = parse_html_element(child)
        if parsed:
            if parsed.get("html_tag") == "span" and parsed.get("text") and not parsed.get("_explicit_name"):
                node["text"] += parsed["text"]
            else:
                node["children"].append(parsed)

    node["text"] = node["text"].strip()
    return node


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    preset_map = {}
    stylesheet = []

    for style_tag in soup.find_all("style"):
        css_content = style_tag.string or ""
        for block in extract_css_blocks(css_content):
            process_css_block(block, preset_map, stylesheet)

    presets = [{"name": str(k), "css": str(v)} for k, v in preset_map.items()]

    components = []
    body = soup.body or soup

    for child in body.children:
        parsed = parse_html_element(child)
        if parsed:
            components.append(parsed)

    return presets, stylesheet, components


# --------------------------------------------
# YAML BUILDER
# --------------------------------------------

class YAMLBuilder:

    def __init__(self):
        self.name_counts = {}

    def generate_name(self, tag, type_name):
        key = f"{type_name.lower()}_{tag}" if type_name.lower() != tag else tag
        self.name_counts[key] = self.name_counts.get(key, 0) + 1
        return f"{key}_{self.name_counts[key]}"

    def build_component(self, comp):

        tag = comp["html_tag"]
        force_container = comp.pop("_force_container", False)
        event_bindings = comp.pop("_event_bindings", {})
        explicit_name = comp.pop("_explicit_name", None)

        # ----------------------------------
        # Determine component type
        # ----------------------------------
        if force_container:
            type_name = "Container"
        elif comp["children"]:
            type_name = "Container"
        else:
            type_name = NUI_TAG_MAPPINGS.get(tag, "Label")

        # ----------------------------------
        # Name resolution
        # ----------------------------------
        if explicit_name:
            name = explicit_name
        else:
            name = self.generate_name(tag, type_name)

        properties = {k: v for k, v in comp.items() if k != "children"}

        comp_dict = {
            "layout_properties": {"slot": "default"},
            "name": name,
            "properties": properties,
            "type": f"form:NUI.{type_name}",
        }

        if event_bindings:
            comp_dict["event_bindings"] = event_bindings

        if comp["children"]:
            comp_dict["components"] = [
                self.build_component(child) for child in comp["children"]
            ]

        return comp_dict


# --------------------------------------------
# FORM STRUCTURE
# --------------------------------------------

def build_form_yaml(html):
    presets, stylesheets, components = parse_html(html)

    builder = YAMLBuilder()

    # ----------------------------------
    # Base Form Structure
    # ----------------------------------

    base_form = {
        "container": {"type": "HtmlTemplate"},
        "is_package": True,
        "components": []
    }

    # ----------------------------------
    # Preset Container (like original converter)
    # ----------------------------------

    preset_container = {
        "layout_properties": {"slot": "default"},
        "name": "NUI_Presets",
        "properties": {
            "visible": False  # hidden container
        },
        "type": "form:NUI.PresetsContainer",
        "components": []
    }

    # Add Preset components
    for props in presets:
        preset_container["components"].append({
            "layout_properties": {"slot": "default"},
            "name": f"preset_{props['name']}",
            "properties": {
                "name": props["name"],
                "css": props["css"],
                "item": props
            },
            "type": "form:NUI.Preset"
        })

    # Add StyleSheet components
    for i, style in enumerate(stylesheets, start=1):
        preset_container["components"].append({
            "layout_properties": {"slot": "default"},
            "name": f"stylesheet_{i}",
            "properties": {
                "css": style,
                "item": {"css": style}
            },
            "type": "form:NUI.StyleSheet"
        })

    # Only add preset container if it has content
    if preset_container["components"]:
        base_form["components"].append(preset_container)

    # ----------------------------------
    # Main UI Container (Base)
    # ----------------------------------

    base_container = {
        "layout_properties": {"slot": "default"},
        "name": "Base",
        "properties": {"true_html_structure": True},
        "type": "form:NUI.Container",
        "components": []
    }

    for comp in components:
        base_container["components"].append(
            builder.build_component(comp)
        )

    base_form["components"].append(base_container)

    # ----------------------------------
    # Final YAML
    # ----------------------------------

    safe_data = make_yaml_safe(base_form)

    return yaml.safe_dump(
        safe_data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False
    )

# --------------------------------------------
# ENTRY POINT
# --------------------------------------------

def main():
    if len(sys.argv) != 2:
        print("Usage: python html_to_form_yaml.py path/to/file.html")
        sys.exit(1)

    html_path = sys.argv[1]

    if not os.path.exists(html_path):
        print("File not found.")
        sys.exit(1)

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    yaml_output = build_form_yaml(html)

    output_path = os.path.join(
        os.path.dirname(html_path),
        "form_template.yaml"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(yaml_output)

    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()