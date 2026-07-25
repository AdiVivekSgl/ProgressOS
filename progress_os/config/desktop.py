"""Desktop module declaration for ProgressOS."""

from frappe import _


def get_data():
    """Return desktop module metadata for Frappe."""
    return [
        {
            "module_name": "ProgressOS",
            "category": "Modules",
            "label": _("ProgressOS"),
            "color": "blue",
            "icon": "octicon octicon-pulse",
            "type": "module",
            "description": _("Organizational memory and activity timeline."),
        }
    ]
