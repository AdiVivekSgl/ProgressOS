# Copyright (c) 2026, ProgressOS Contributors and contributors
# For license information, please see license.txt

"""Controller for the Event Type DocType.

Event Types are administrator-configured categories (Customer Visit, Phone Call,
Recognition, ...). Keeping them as data — not code — is what makes ProgressOS
ERP-agnostic and lets teams shape their own vocabulary without a deployment.
"""

from frappe.model.document import Document


class EventType(Document):
	pass
