# Copyright (c) 2026, ProgressOS Contributors and contributors
# For license information, please see license.txt

"""Public, whitelisted API for ProgressOS.

Thin transport layer over ``progressos.services.event_service``. These are the
stable method paths (``progress_os.api.*``) that the Desk UI and the future
standalone / mobile clients call. Business logic belongs in the service layer,
not here — keep these wrappers boring on purpose.
"""

import frappe

from progress_os.progressos.services import event_service


@frappe.whitelist()
def create_event(
	event_type,
	description,
	title=None,
	related_documents=None,
	outcome=None,
	status=None,
	next_action=None,
	due_date=None,
	visibility=None,
	event_datetime=None,
):
	"""Create a Progress Event. ``related_documents`` may be a list or JSON string."""
	if isinstance(related_documents, str):
		related_documents = frappe.parse_json(related_documents)

	return event_service.create_event(
		event_type=event_type,
		description=description,
		title=title,
		related_documents=related_documents,
		outcome=outcome,
		status=status,
		next_action=next_action,
		due_date=due_date,
		visibility=visibility,
		event_datetime=event_datetime,
	)


@frappe.whitelist()
def get_event(name):
	"""Return a single event as a dict."""
	return event_service.get_event(name)


@frappe.whitelist()
def get_feed(event_type=None, status=None, owner=None, include_archived=0, start=0, page_length=20):
	"""Return recent events, newest first."""
	return event_service.get_feed(
		event_type=event_type,
		status=status,
		owner=owner,
		include_archived=frappe.utils.cint(include_archived),
		start=frappe.utils.cint(start),
		page_length=frappe.utils.cint(page_length),
	)


@frappe.whitelist()
def get_document_timeline(doctype, name, include_archived=0, start=0, page_length=20):
	"""Return events linked to a given document, newest first."""
	return event_service.get_document_timeline(
		doctype=doctype,
		name=name,
		include_archived=frappe.utils.cint(include_archived),
		start=frappe.utils.cint(start),
		page_length=frappe.utils.cint(page_length),
	)


@frappe.whitelist()
def set_status(name, status):
	"""Update an event's progress status."""
	return event_service.set_status(name=name, status=status)


@frappe.whitelist()
def archive_event(name, archived=1):
	"""Archive or unarchive an event."""
	return event_service.archive_event(name=name, archived=bool(frappe.utils.cint(archived)))
