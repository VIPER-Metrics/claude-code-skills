---
name: nui
description: Build UI for Anvil applications using NUI — a framework that lets you write layouts in HTML and convert them to valid Anvil Forms. Use this skill whenever the user wants to create, edit, or convert an Anvil UI using NUI, design.html files, html_to_nui.py, form_template.yaml, or any NUI component. Also trigger when the user asks about NUI attributes (anvil-var, anvil-event-*, anvil-is-container), component mapping, dynamic form embedding, or managing CSS classes in NUI Python code.
---

# NUI Skill

NUI lets you write Anvil UI in HTML, then convert it to a valid `form_template.yaml`. All logic stays in Python; no JavaScript is allowed.

## Workflow

1. Write `design.html` inside the form folder
2. Run the converter: `python html_to_nui.py /path/to/design.html`
3. This generates `form_template.yaml` — ready for Anvil
4. Write all UI logic in `__init__.py` (Python only)

> ⚠️ If the user has `html_to_nui.py` or an `example_app` in their skill directory, read those first with the `view` tool before starting — they may contain project-specific patterns or overrides.

---

## Special NUI Attributes

These attributes are **removed automatically** during conversion. They are instructions to the converter, not final component properties.

| Attribute | Purpose |
|---|---|
| `anvil-var="name"` | Exposes component as `self.name` in Python |
| `anvil-event-click="handler"` | Binds click → `def handler(self, **event_args)` |
| `anvil-event-<event>="handler"` | Any supported event (see Events table) |
| `anvil-is-container` | Forces element to become a Container even if empty |

### Example HTML

```html
<div anvil-var="card_wrapper" anvil-is-container>
  <button
    anvil-var="save_btn"
    anvil-event-click="save_clicked">
    Save
  </button>
  <input anvil-var="email_input" placeholder="Email" />
</div>
```

### Resulting Python access

```python
self.card_wrapper          # Container
self.save_btn              # Button
self.email_input.text      # TextBox value

def save_clicked(self, **event_args):
    print(self.email_input.text)
```

---

## Component Mapping

| HTML Tag | NUI Component |
|---|---|
| `label`, `p`, `span`, `h1`–`h6` | Label |
| `button` | Button |
| `textarea` | TextArea |
| `input` | TextBox |
| `a` | Link |
| `img` | Image |
| Any element with children | Container |
| `anvil-is-container` present | Container (forced) |
| Unknown fallback | Label |

---

## Component Properties

Virtually every component supports flexible properties.

| Property          | Type          | Description           |
| ----------------- | ------------- | --------------------- |
| `html_tag`        | string        | Original HTML tag     |
| `preset`          | list          | CSS classes           |
| `text`            | string        | Displayed text        |
| `text_type`       | string        | `"text"` or `"html"`  |
| `text_align`      | string        | Alignment             |
| `font_size`       | string/number | Font size             |
| `font`            | string        | Font family           |
| `font_weight`     | string        | Font weight           |
| `foreground`      | string        | Text color            |
| `background`      | string        | Background color      |
| `width`           | string/number | Width                 |
| `height`          | string/number | Height                |
| `visible`         | boolean       | Show/hide             |
| `enabled`         | boolean       | Enable/disable        |
| `border_radius`   | string/number | Corner rounding       |
| `border_size`     | string        | Border thickness      |
| `border_style`    | string        | Border style          |
| `border_color`    | string        | Border color          |
| `margin`          | string        | Outer spacing         |
| `padding`         | string        | Inner spacing         |
| `icon`            | string        | Icon name             |
| `icon_align`      | string        | Icon alignment        |
| `icon_size`       | string        | Icon size             |
| `css`             | string        | Custom CSS            |
| `hover_css`       | string        | Hover CSS             |
| `active_css`      | string        | Active CSS            |
| `disabled_css`    | string        | Disabled CSS          |
| `focus_css`       | string        | Focus CSS             |
| `placeholder_css` | string        | Placeholder style     |
| `attributes`      | dict          | Extra HTML attributes |
| `type`            | string        | Input type            |
| `placeholder`     | string        | Placeholder text      |

---

## Events

| Event           | Applies To              |
| --------------- | ----------------------- |
| `click`         | Button, Container, Link |
| `input`         | Inputs                  |
| `change`        | Inputs                  |
| `pressed_enter` | TextBox                 |
| `focus`         | Inputs                  |
| `lost_focus`    | Inputs                  |
| `hover`         | Interactive components  |
| `hover_out`     | Interactive components  |

Example:

```python

def label_1_click(self, **event_args):
    print(event_args['sender']) #The sender of the event
    print(event_args['event']) #JS event info
```

Bind declaratively with `anvil-event-<event>="handler_name"` in HTML. Only bind manually in Python for dynamically created components.

For additional js events, you can declare them in code

```python
self.label_1.add_event("my_js_event", self.label_1_click)
```

---

## DOM Access

Every component exposes its raw DOM element for properties not covered by NUI:

```python
self.my_component.dom  # Raw DOM element
```

---

## Managing CSS Classes in Python

```python
self.my_component.add_preset("active")
self.my_component.remove_preset("active")
self.my_component.toggle_preset("active")
```

---

## Creating Components Dynamically in Python

```python
from NUI import components as NUI

btn = NUI.Button(text="Click Me")
self.content_panel.add_component(btn)
```

---

## Embedding Other Forms

Import and mount other forms dynamically for modular UIs:

```python
from ..UserProfile import UserProfile

def show_profile(self):
    profile = UserProfile()
    self.content_container.clear()
    self.content_container.add_component(profile)
```

> **Rule**: Whenever a component needs to be reused or have multiple instances, create a dedicated form for it and add it to a container dynamically.

---

## Best Practices

- ✅ Keep all logic in Python — no JavaScript in `design.html`
- ✅ Use `anvil-var` only when you need Python access to the component
- ✅ Use `anvil-event-*` for declarative event binding
- ✅ Use `anvil-is-container` on elements that will receive dynamic children
- ✅ Create separate forms for reusable components
- ✅ Use `<style>` blocks in `design.html` for layout-specific CSS
- ❌ Do not write `<script>` tags in `design.html`

---

## Reference Files

- `example_app/` — Working example app; read this first if present in the skill directory
- `html_to_nui.py` — The converter script; read this if conversion behavior is unclear or unexpected
