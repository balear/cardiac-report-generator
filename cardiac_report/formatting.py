"""Utility helpers for formatting values in reports and the UI."""


def color_status_html(label: str) -> str:
    """Return HTML span with color coding for dilatation status."""
    try:
        if label is None:
            return ""
        text = str(label).strip()
        low = text.lower()
        # Map common severity labels to colors:
        # normal/none -> green, mild -> yellow, moderate -> orange, severe/ernstig -> red
        if any(x in low for x in ('geen', 'niet', 'norm', 'normal')):
            color = 'green'
        elif any(x in low for x in ('mild', 'milde')):
            color = 'goldenrod'
        elif any(x in low for x in ('matig', 'matig', 'moderate')):
            color = 'orange'
        elif any(x in low for x in ('ernstig', 'ernstige', 'severe')):
            color = 'red'
        elif 'gedilateerd' in low:
            color = 'red'
        else:
            color = 'black'
        return f"<span style='color:{color}; font-weight:600'>{text}</span>"
    except Exception:
        return str(label)
