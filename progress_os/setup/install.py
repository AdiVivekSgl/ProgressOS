# Copyright (c) 2026, ProgressOS Contributors and contributors
# For license information, please see license.txt

"""Install-time setup for ProgressOS.

Runs on ``after_install`` (wired in hooks.py). Everything here is idempotent so
it is safe to re-run via ``bench execute``.
"""

import frappe

APP_ROLES = ("ProgressOS User", "ProgressOS Manager")

# (name, icon, color, requires_outcome, requires_next_action)
DEFAULT_EVENT_TYPES = (
	("Customer Visit", "🤝", "#2490ef", 0, 0),
	("Phone Call", "📞", "#7575ff", 0, 0),
	("Internal Discussion", "💬", "#748094", 0, 0),
	("Sample Dispatch", "📦", "#ff9800", 0, 0),
	("Production Delay", "⏳", "#e03636", 1, 1),
	("Engineering Suggestion", "🛠️", "#00a99d", 0, 0),
	("Customer Complaint", "⚠️", "#cb2929", 1, 1),
	("Competitor Information", "🔍", "#6b46c1", 0, 0),
	("Recognition", "⭐", "#f5c518", 0, 0),
	("AI Insight", "🤖", "#0f9d58", 0, 0),
	("Automated Notification", "🔔", "#95a5a6", 0, 0),
)


def after_install():
	ensure_roles()
	seed_event_types()
	frappe.db.commit()


def ensure_roles():
	"""Create the ProgressOS roles if they do not already exist."""
	for role_name in APP_ROLES:
		if not frappe.db.exists("Role", role_name):
			frappe.get_doc(
				{
					"doctype": "Role",
					"role_name": role_name,
					"desk_access": 1,
				}
			).insert(ignore_permissions=True)


def seed_event_types():
	"""Seed the default catalog of event types, skipping any that already exist."""
	for order, (name, icon, color, requires_outcome, requires_next_action) in enumerate(
		DEFAULT_EVENT_TYPES
	):
		if frappe.db.exists("Event Type", name):
			continue
		frappe.get_doc(
			{
				"doctype": "Event Type",
				"event_type_name": name,
				"icon": icon,
				"color": color,
				"enabled": 1,
				"display_order": order,
				"requires_outcome": requires_outcome,
				"requires_next_action": requires_next_action,
			}
		).insert(ignore_permissions=True)
