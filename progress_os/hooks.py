"""Frappe hooks for the ProgressOS application.

Sprint 1 introduces the core Progress Event model, install-time seeding, and the
first public extension events. Feature hooks (assets, scheduler, notifications)
are added as their sprints land.
"""

app_name = "progress_os"
app_title = "ProgressOS"
app_publisher = "ProgressOS Contributors"
app_description = "Organizational memory and activity timeline for Frappe."
app_email = "maintainers@example.com"
app_license = "GPL-3.0-only"

# Include JS/CSS only when feature implementation begins.
app_include_css = []
app_include_js = []

# Installation
# ------------
after_install = "progress_os.setup.install.after_install"

# Extension events
# ----------------
# Other apps can subscribe to the ProgressOS event lifecycle by registering
# handlers under these hook keys. Each handler receives the Progress Event doc.
# Example (in another app's hooks.py):
#     on_progress_event_created = ["my_app.handlers.notify_team"]
on_progress_event_created = []
on_progress_event_updated = []
