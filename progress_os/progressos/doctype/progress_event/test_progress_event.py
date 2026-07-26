# Copyright (c) 2026, ProgressOS Contributors and contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

from progress_os.progressos.services import event_service


class TestProgressEvent(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		_ensure_event_type("Test Visit")
		_ensure_event_type("Test Delay", requires_outcome=1, requires_next_action=1)

	def test_create_minimal_event(self):
		"""An event needs only an event type and description."""
		result = event_service.create_event(
			event_type="Test Visit",
			description="Visited **ABC Transformers**.",
		)
		self.assertTrue(result["name"])
		self.assertEqual(result["event_type"], "Test Visit")
		self.assertEqual(result["status"], "Open")
		self.assertFalse(result["is_archived"])
		# Markdown is rendered for clients but stored raw.
		self.assertIn("<strong>ABC Transformers</strong>", result["description_html"])
		self.assertIn("**ABC Transformers**", result["description"])

	def test_create_event_with_related_documents(self):
		"""Generic linking attaches an event to arbitrary documents."""
		result = event_service.create_event(
			event_type="Test Visit",
			description="Follow-up visit.",
			related_documents=[
				{"link_doctype": "User", "link_name": "Administrator", "relationship": "Primary"},
			],
		)
		self.assertEqual(len(result["related_documents"]), 1)
		link = result["related_documents"][0]
		self.assertEqual(link["link_doctype"], "User")
		self.assertEqual(link["link_name"], "Administrator")
		self.assertEqual(link["relationship"], "Primary")

	def test_document_timeline(self):
		"""A linked document can retrieve its own event timeline."""
		event_service.create_event(
			event_type="Test Visit",
			description="Timeline entry.",
			related_documents=[{"link_doctype": "User", "link_name": "Administrator"}],
		)
		timeline = event_service.get_document_timeline("User", "Administrator")
		self.assertGreaterEqual(len(timeline), 1)
		self.assertTrue(
			all(
				any(
					r["link_doctype"] == "User" and r["link_name"] == "Administrator"
					for r in event["related_documents"]
				)
				for event in timeline
			)
		)

	def test_event_type_requires_outcome(self):
		"""requires_outcome / requires_next_action are enforced on validate."""
		with self.assertRaises(frappe.ValidationError):
			event_service.create_event(
				event_type="Test Delay",
				description="Line stopped.",
			)

		# Supplying both clears the requirement.
		result = event_service.create_event(
			event_type="Test Delay",
			description="Line stopped.",
			outcome="Resumed after 2h.",
			next_action="Order spare motor.",
		)
		self.assertTrue(result["name"])

	def test_set_status_and_archive(self):
		created = event_service.create_event(
			event_type="Test Visit",
			description="Status test.",
		)
		updated = event_service.set_status(created["name"], "Needs Attention")
		self.assertEqual(updated["status"], "Needs Attention")

		with self.assertRaises(frappe.ValidationError):
			event_service.set_status(created["name"], "Bogus")

		archived = event_service.archive_event(created["name"])
		self.assertTrue(archived["is_archived"])


def _ensure_event_type(name, requires_outcome=0, requires_next_action=0):
	if not frappe.db.exists("Event Type", name):
		frappe.get_doc(
			{
				"doctype": "Event Type",
				"event_type_name": name,
				"enabled": 1,
				"requires_outcome": requires_outcome,
				"requires_next_action": requires_next_action,
			}
		).insert(ignore_permissions=True)
