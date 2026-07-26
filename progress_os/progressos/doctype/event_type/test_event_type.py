# Copyright (c) 2026, ProgressOS Contributors and contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestEventType(FrappeTestCase):
	def test_name_is_the_type_name(self):
		"""Event Type is named by its title (autoname field:event_type_name)."""
		if not frappe.db.exists("Event Type", "Unit Test Type"):
			doc = frappe.get_doc(
				{
					"doctype": "Event Type",
					"event_type_name": "Unit Test Type",
					"enabled": 1,
				}
			).insert(ignore_permissions=True)
			self.assertEqual(doc.name, "Unit Test Type")

	def test_type_name_is_unique(self):
		frappe.get_doc(
			{"doctype": "Event Type", "event_type_name": "Dup Type", "enabled": 1}
		).insert(ignore_permissions=True)
		with self.assertRaises(frappe.DuplicateEntryError):
			frappe.get_doc(
				{"doctype": "Event Type", "event_type_name": "Dup Type", "enabled": 1}
			).insert(ignore_permissions=True)
