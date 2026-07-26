# Copyright (c) 2026, ProgressOS Contributors and contributors
# For license information, please see license.txt

"""Event service layer.

All Progress Event business logic lives here so every client — the Frappe Desk
UI, the whitelisted API in ``progress_os/api.py``, and the future standalone /
mobile app — reuses the same behavior instead of re-implementing it. Keep these
functions transport-agnostic: no request/response objects, just data in and
plain dicts out.
"""

from __future__ import annotations

import frappe

VALID_STATUSES = ("Open", "In Progress", "Done", "Needs Attention")


def create_event(
	event_type: str,
	description: str,
	title: str | None = None,
	related_documents: list[dict] | None = None,
	outcome: str | None = None,
	status: str | None = None,
	next_action: str | None = None,
	due_date: str | None = None,
	visibility: str | None = None,
	event_datetime: str | None = None,
) -> dict:
	"""Create and persist a Progress Event.

	``related_documents`` is a list of dicts shaped like
	``{"link_doctype": ..., "link_name": ..., "relationship": "Related"}``.
	Returns the created event as a serialized dict.
	"""
	if not event_type:
		frappe.throw(frappe._("Event Type is required."))
	if not (description or "").strip():
		frappe.throw(frappe._("Description is required."))
	if status and status not in VALID_STATUSES:
		frappe.throw(frappe._("Invalid status: {0}").format(status))

	doc = frappe.new_doc("Progress Event")
	doc.event_type = event_type
	doc.description = description
	doc.title = title
	doc.outcome = outcome
	doc.status = status or "Open"
	doc.next_action = next_action
	doc.due_date = due_date
	doc.visibility = visibility or _default_visibility(event_type)
	if event_datetime:
		doc.event_datetime = event_datetime

	for row in related_documents or []:
		doc.append(
			"related_documents",
			{
				"link_doctype": row.get("link_doctype"),
				"link_name": row.get("link_name"),
				"relationship": row.get("relationship") or "Related",
			},
		)

	doc.insert()
	return serialize_event(doc)


def get_event(name: str) -> dict:
	"""Return a single event (including related documents) as a dict."""
	doc = frappe.get_doc("Progress Event", name)
	doc.check_permission("read")
	return serialize_event(doc)


def set_status(name: str, status: str) -> dict:
	"""Update an event's progress status."""
	if status not in VALID_STATUSES:
		frappe.throw(frappe._("Invalid status: {0}").format(status))
	doc = frappe.get_doc("Progress Event", name)
	doc.status = status
	doc.save()
	return serialize_event(doc)


def archive_event(name: str, archived: bool = True) -> dict:
	"""Archive (or unarchive) an event without deleting it."""
	doc = frappe.get_doc("Progress Event", name)
	doc.is_archived = 1 if archived else 0
	doc.save()
	return serialize_event(doc)


def get_feed(
	event_type: str | None = None,
	status: str | None = None,
	owner: str | None = None,
	include_archived: bool = False,
	start: int = 0,
	page_length: int = 20,
) -> list[dict]:
	"""Return recent events, newest first, honoring the caller's read permission."""
	filters: dict = {}
	if event_type:
		filters["event_type"] = event_type
	if status:
		filters["status"] = status
	if owner:
		filters["owner"] = owner
	if not include_archived:
		filters["is_archived"] = 0

	names = frappe.get_list(
		"Progress Event",
		filters=filters,
		order_by="event_datetime desc, creation desc",
		limit_start=start,
		limit_page_length=page_length,
		pluck="name",
	)
	return [serialize_event(frappe.get_doc("Progress Event", name)) for name in names]


def get_document_timeline(
	doctype: str,
	name: str,
	include_archived: bool = False,
	start: int = 0,
	page_length: int = 20,
) -> list[dict]:
	"""Return events linked to a specific document, newest first.

	Powers the "Progress" timeline panel on any linked document. Matches against
	the generic Related Documents child table, so it works for any DocType.
	"""
	child_filters = {"link_doctype": doctype, "link_name": name}
	parent_names = frappe.get_all(
		"Progress Event Related Document",
		filters=child_filters,
		pluck="parent",
		distinct=True,
	)
	if not parent_names:
		return []

	filters: dict = {"name": ["in", parent_names]}
	if not include_archived:
		filters["is_archived"] = 0

	names = frappe.get_list(
		"Progress Event",
		filters=filters,
		order_by="event_datetime desc, creation desc",
		limit_start=start,
		limit_page_length=page_length,
		pluck="name",
	)
	return [serialize_event(frappe.get_doc("Progress Event", name)) for name in names]


def serialize_event(doc) -> dict:
	"""Serialize a Progress Event into a stable, client-friendly dict.

	This is the shape the timeline renderer and future non-Frappe clients consume,
	so it is intentionally explicit rather than a raw ``as_dict()``.
	"""
	return {
		"name": doc.name,
		"event_type": doc.event_type,
		"event_datetime": doc.event_datetime,
		"title": doc.title,
		"description": doc.description,
		"description_html": frappe.utils.md_to_html(doc.description or ""),
		"outcome": doc.outcome,
		"status": doc.status,
		"next_action": doc.next_action,
		"due_date": doc.due_date,
		"visibility": doc.visibility,
		"department": doc.department,
		"location": doc.location,
		"is_archived": bool(doc.is_archived),
		"owner": doc.owner,
		"creation": doc.creation,
		"modified": doc.modified,
		"related_documents": [
			{
				"link_doctype": row.link_doctype,
				"link_name": row.link_name,
				"relationship": row.relationship,
			}
			for row in doc.related_documents
		],
	}
