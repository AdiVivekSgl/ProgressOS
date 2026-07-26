# Event Model (Sprint 1)

> Detailed design for the atomic unit of ProgressOS. Subordinate to
> [`product_brief.md`](product_brief.md). This document is the contract that the
> Sprint 1 DocTypes, service layer, and tests implement.

## The atomic unit

Everything in ProgressOS derives from one object: a **Progress Event**. Feed,
recognition, follow-ups, digests, and analytics are all *views over* or
*enrichments of* events. Get this model right and the rest of the product becomes
presentation.

### Why "Progress Event" and not "Event"

Frappe core already defines a globally-unique DocType named `Event` (the desk
calendar). DocType names are unique per site, so our type is named **`Progress
Event`** internally. Product surfaces (Desk labels, the future standalone/mobile
app) are free to call it simply "Event" — the internal name only needs to be
collision-proof.

## DocTypes introduced in Sprint 1

| DocType | Kind | Purpose |
| --- | --- | --- |
| `Progress Event` | Master | One meaningful unit of organizational memory |
| `Progress Event Related Document` | Child table | Generic link from an event to any DocType |
| `Event Type` | Master (config) | Configurable event categories (Customer Visit, etc.) |

Deliberately **not** in Sprint 1: reactions/recognition (Sprint 5), follow-up
automation (Sprint 6), ProgressOS Settings, digests, AI. See the roadmap.

## What we lean on Frappe-native for

To honor "avoid unnecessary custom", these are **not** custom-built:

- **Discussion (comments)** → Frappe's native Comment on the event doc. Comments
  are *not* events.
- **Attachments** → Frappe's native File attachments (`attach` / sidebar), not a
  custom child table.
- **Tags** → Frappe's native tagging (`_user_tags`), not a custom Tag table.
- **Created By / timestamps** → Frappe's built-in `owner`, `creation`,
  `modified`. We add an explicit `event_datetime` because *when the work happened*
  can differ from *when it was logged*.

## `Progress Event` fields

Naming: `naming_rule = "Random"` (`autoname = "hash"`) — every event gets an
opaque, stable, UUID-like id. Titles are not identifiers.

### Content
| Field | Type | Notes |
| --- | --- | --- |
| `event_type` | Link → Event Type | **Required.** The one dropdown in the composer. |
| `event_datetime` | Datetime | **Required**, defaults to now. When the work happened. |
| `title` | Data | Optional. Short headline; auto-derivable from description later. |
| `description` | Long Text | Markdown source. Stored raw (AI-friendly); rendered via `frappe.utils.md_to_html` at display time. |
| `outcome` | Small Text | Optional result/decision. |

Markdown-as-storage is a deliberate AI-native choice: markdown is cleaner context
for LLMs than the HTML a rich-text editor would produce, and it round-trips to any
future non-Frappe client.

### Progress (distinct from publication lifecycle)
| Field | Type | Notes |
| --- | --- | --- |
| `status` | Select | `Open` / `In Progress` / `Done` / `Needs Attention`. Default `Open`. Drives the "Needs Attention" feed. |
| `next_action` | Small Text | Optional. |
| `due_date` | Date | Optional. Foundation for Sprint 6 follow-ups. |

### Relationships
| Field | Type | Notes |
| --- | --- | --- |
| `related_documents` | Table → Progress Event Related Document | Zero or more generic links. |

### Metadata
| Field | Type | Notes |
| --- | --- | --- |
| `visibility` | Select | `Private` / `Team` / `Department` / `Organization` / `Restricted`. Default `Organization`. Stored now; enforced in filtering from the Feed sprint. |
| `department` | Data | Free text, **not** a link — staying ERP-agnostic (no dependency on ERPNext/HR `Department`). |
| `location` | Data | Optional. |
| `is_archived` | Check | Publication lifecycle (see below). Default `0`. |

Required fields total **two**: `event_type` and `description`. Everything else is
optional and lives in collapsed sections so logging stays under 20 seconds.

## `Progress Event Related Document` (child)

The generic-linking table — what makes ProgressOS document-agnostic.

| Field | Type | Notes |
| --- | --- | --- |
| `link_doctype` | Link → DocType | **Required.** The target document's type. |
| `link_name` | Dynamic Link (options = `link_doctype`) | **Required.** The target document. |
| `relationship` | Select | `Primary` / `Related` / `Generated From` / `Mentioned`. Default `Related`. |

No business object is ever hardcoded. An event can link a `Customer` as `Primary`,
an `Opportunity` as `Related`, and a `Quotation` as `Generated From` — or link to
any custom DocType the same way.

## `Event Type` fields (config master)

Naming: `autoname = "field:event_type_name"`.

| Field | Type | Notes |
| --- | --- | --- |
| `event_type_name` | Data | **Required, unique.** e.g. "Customer Visit". |
| `description` | Small Text | Admin-facing help. |
| `icon` | Data | Emoji or icon class for feed cards. |
| `color` | Color | Feed accent color. |
| `enabled` | Check | Default `1`. Disabled types hide from the composer. |
| `default_visibility` | Select | Pre-fills an event's visibility. |
| `requires_outcome` | Check | If set, events of this type require an outcome. |
| `requires_next_action` | Check | If set, events of this type require a next action. |
| `display_order` | Int | Composer ordering. |

### Seeded defaults (`after_install`, idempotent)

Customer Visit, Phone Call, Internal Discussion, Sample Dispatch, Production Delay,
Engineering Suggestion, Customer Complaint, Competitor Information, Recognition,
AI Insight, Automated Notification. Seeding is skipped for any type that already
exists, so it is safe to re-run.

## Lifecycle

Two orthogonal concepts, deliberately not conflated:

- **Publication lifecycle**: events **publish immediately** on save. There is no
  Draft gate (it would fight the 20-second rule) and the doctype is **not
  submittable** (submit/cancel immutability is wrong for a social feed). The only
  lifecycle transition is archival via `is_archived`.
- **Progress status**: the `status` field tracks the *work*, independent of
  publication — an event can be `Published + Needs Attention`.

```
create ──▶ Published ──▶ (is_archived = 1) ──▶ Archived
                 ▲                                   │
                 └───────────── unarchive ───────────┘
```

## Permissions

Two app roles (auto-created on migrate from the DocPerms) plus System Manager:

| Role | Progress Event | Event Type |
| --- | --- | --- |
| System Manager | Full | Full |
| ProgressOS Manager | Full (read all, write, delete, report) | Full (manage config) |
| ProgressOS User | Create + read; write/delete only `if_owner` | Read only |

Visibility-based row filtering (Private/Team/etc.) is enforced starting in the Feed
sprint; Sprint 1 ships the field and the role model.

## API contract (service layer — "API first")

Business logic lives in `progress_os/progressos/services/event_service.py` and is
exposed through thin whitelisted wrappers in `progress_os/api.py`, so the Desk UI
and the future standalone/mobile app call the **same** methods.

| Method | Signature (essentials) | Returns |
| --- | --- | --- |
| `progress_os.api.create_event` | `event_type, description, title=None, related_documents=None, outcome=None, status=None, next_action=None, due_date=None, visibility=None, event_datetime=None` | the created event as a dict |
| `progress_os.api.get_event` | `name` | one event dict (with related docs) |
| `progress_os.api.get_feed` | `event_type=None, status=None, owner=None, start=0, page_length=20` | list of event dicts, newest first |
| `progress_os.api.get_document_timeline` | `doctype, name, start=0, page_length=20` | events linked to that document |
| `progress_os.api.set_status` | `name, status` | updated event dict |
| `progress_os.api.archive_event` | `name, archived=True` | updated event dict |

`related_documents` accepts a list of `{link_doctype, link_name, relationship?}`.

### Extension events

`Progress Event`'s controller dispatches app hooks so other apps can subscribe
without patching core:

- `on_progress_event_created`
- `on_progress_event_updated`

Additional hooks (`on_reaction_added`, `on_action_completed`,
`on_digest_generated`) arrive with their respective sprints.

## Timeline rendering rules (contract for Sprint 2)

Sprint 1 ships the data + service layer only, but the renderer must follow:

- Order by `event_datetime` desc, then `creation` desc.
- Group by day (`TODAY`, `YESTERDAY`, then dates).
- Each card shows: event-type icon + color, title or first line of rendered
  markdown, author (`owner`), relative time, linked-document chips, and indicators
  for comments / next action / status when `Needs Attention`.
- Render `description` markdown → HTML at display time; never store HTML.
- Archived events are hidden from default feeds but visible on a document's own
  timeline when explicitly requested.
