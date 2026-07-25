# ProgressOS Architecture

## Product Intent

ProgressOS is a generic Frappe application for capturing organizational memory. It records meaningful work events that explain how operational outcomes happened, while avoiding surveillance-oriented patterns.

## Architectural Principles

1. **Event driven**: the timeline event is the core domain object.
2. **ERP agnostic**: the app must not depend on ERPNext-specific DocTypes or workflows.
3. **Document agnostic**: events can attach to any Frappe DocType through generic references.
4. **AI native**: timeline data should be clean, structured, and provider-independent.
5. **Social first**: feeds, comments, reactions, mentions, and recognition shape the user experience.
6. **Configuration first**: administrators should configure behavior without code changes.

## Layered Design

- **Domain layer**: DocTypes and domain services for events, activity types, and reactions.
- **Application layer**: whitelisted APIs, hooks, digest orchestration, notifications, and feed queries.
- **Integration layer**: provider-independent adapters for AI, search, notifications, and external subscribers.
- **Presentation layer**: workspaces, list views, quick entry, form layouts, and future feed components.

## Phase 1 Boundary

Phase 1 creates the repository scaffold and design documents. It does not implement DocTypes, migrations, custom pages, AI calls, or feed logic until the architecture is approved.

## Extension Events

The following extension points should be introduced as stable hook names during implementation:

- `on_event_created`
- `on_event_updated`
- `on_reaction_added`
- `on_action_completed`
- `on_digest_generated`
