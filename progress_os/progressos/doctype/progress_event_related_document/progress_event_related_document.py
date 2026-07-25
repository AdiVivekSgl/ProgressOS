# Copyright (c) 2026, ProgressOS Contributors and contributors
# For license information, please see license.txt

"""Child table linking a Progress Event to any Frappe document.

Generic by design: `link_doctype` + `link_name` (a Dynamic Link) let an event
reference any DocType without ProgressOS ever hardcoding a business object.
"""

from frappe.model.document import Document


class ProgressEventRelatedDocument(Document):
	pass
