# Copyright (c) 2026, ProgressOS Contributors and contributors
# For license information, please see license.txt

"""Controller for the Progress Event DocType.

A Progress Event is the atomic unit of ProgressOS: one meaningful observation,
interaction, decision, or progress update. Feed, recognition, follow-ups, and
analytics are all views over events, so the domain rules live here and the
service layer builds on top of them.
"""

import frappe
from frappe.model.document import Document


class ProgressEvent(Document):
	"""Domain rules and lifecycle for a single event."""

	def validate(self):
		self._apply_event_type_requirements()

	def before_insert(self):
		if not self.event_datetime:
			self.event_datetime = frappe.utils.now_datetime()

	def after_insert(self):
		self._dispatch("on_progress_event_created")

	def on_update(self):
		# Skip the update signal on the insert pass; after_insert already fired.
		if not self.flags.in_insert:
			self._dispatch("on_progress_event_updated")

	def _apply_event_type_requirements(self):
		"""Honor per-type `requires_outcome` / `requires_next_action` flags."""
		if not self.event_type:
			return

		requires_outcome, requires_next_action = frappe.db.get_value(
			"Event Type",
			self.event_type,
			["requires_outcome", "requires_next_action"],
		) or (0, 0)

		if requires_outcome and not (self.outcome or "").strip():
			frappe.throw(
				frappe._("Event Type {0} requires an Outcome.").format(self.event_type)
			)
		if requires_next_action and not (self.next_action or "").strip():
			frappe.throw(
				frappe._("Event Type {0} requires a Next Action.").format(self.event_type)
			)

	def _dispatch(self, hook_name: str):
		"""Run any app hooks registered under `hook_name` and emit realtime.

		Lets other apps subscribe to event lifecycle without patching core. Handler
		errors are logged, never allowed to break event creation.
		"""
		for handler in frappe.get_hooks(hook_name) or []:
			try:
				frappe.get_attr(handler)(self)
			except Exception:
				frappe.log_error(
					title=f"ProgressOS {hook_name} handler failed: {handler}",
					message=frappe.get_traceback(),
				)

		frappe.publish_realtime(hook_name, {"name": self.name}, after_commit=True)
