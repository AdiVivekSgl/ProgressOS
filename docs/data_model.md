# Data Model

## Core Entities

### Timeline Event

Represents a meaningful observation, interaction, decision, progress update, recognition, or system-generated insight.

Key field groups:

- Basic: title, description, event type, event datetime, owner/created by.
- Progress: status, outcome, next action, due date.
- Metadata: tags, visibility, department, optional location.
- Collaboration: comments, mentions, attachments through Frappe-native mechanisms where possible.
- Recognition: related reactions and appreciations.

### Activity Type

Configures allowed event categories such as customer visit, phone call, internal discussion, production delay, customer complaint, recognition, or AI insight.

### Reaction Type

Configures available reactions, appreciation types, icons, labels, and optional scoring semantics.

### Reaction

Represents a user's reaction to a timeline event. It references a timeline event, a reaction type, and the reacting user.

### ProgressOS Settings

Stores global configuration such as default visibility, enabled modules, notification preferences, AI provider selection, and reminder policies.

## Generic References

Timeline events must support one or more links to arbitrary Frappe documents. Implementation should use Frappe's Dynamic Link pattern or a child table with `link_doctype` and `link_name` fields so no business object is hardcoded.

## Future Entities

The following entities are intentionally out of MVP scope: follow-up action, digest, saved feed, semantic embedding, badge, notification rule, visibility rule, and integration provider.
