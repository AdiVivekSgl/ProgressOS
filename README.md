# ProgressOS

ProgressOS is an open-source Frappe application that turns transactional systems into a system of organizational memory. It captures the conversations, decisions, observations, progress, and context that connect business records together.

## Vision

ERP systems record what happened. ProgressOS records how it happened.

The product is designed to help teams capture institutional knowledge, collaborate around operational context, recognize meaningful progress, and prepare rich timeline data for AI-native workflows without becoming employee monitoring software.

## Phase 1 Direction

Phase 1 intentionally does not implement full product features. It establishes the app scaffold and architecture needed for review before DocTypes and behavior are built.

Planned MVP DocTypes:

- Timeline Event
- Activity Type
- Reaction Type
- Reaction
- ProgressOS Settings

## Installation

### Frappe Cloud

1. Go to your Frappe Cloud dashboard → **Apps** → **Add App** → **Add from GitHub**.
2. Select this repository (`progress-os/progress_os`) and the branch you want to deploy.
3. Add the app to a bench group running **Frappe v15**, then install it on your site.

### Self-hosted bench

```bash
# From your bench directory
bench get-app https://github.com/progress-os/progress_os --branch main
bench --site your-site.local install-app progress_os
bench --site your-site.local migrate
```

Requires Frappe v15+ and Python 3.10+.

## Documentation

- **[Product Brief](docs/product_brief.md)** — canonical vision, principles, and Phase 1 scope (start here)
- **[Event Model](docs/event_model.md)** — Sprint 1 design spec for the core `Progress Event`
- [Architecture](docs/architecture.md)
- [Data Model](docs/data_model.md)
- [Module Boundaries](docs/module_boundaries.md)
- [DocType Specifications](docs/doctype_specifications.md)
- [API Design](docs/api_design.md)
- [Permission Model](docs/permission_model.md)
- [UI Wireframes](docs/ui_wireframes.md)
- [Development Roadmap](docs/roadmap.md)

## Development Principles

- Event-driven: everything meaningful is represented as an event.
- ERP-agnostic: ProgressOS must not assume ERPNext or any specific business app.
- Document-agnostic: events can reference any Frappe DocType through generic references.
- AI-native: timeline data should be structured for future provider-independent intelligence.
- Social-first: the primary interface is a collaborative activity feed, not a report.

## License

GPL-3.0-only. See [LICENSE](LICENSE).
