# DocType Specifications

## Timeline Event

Purpose: store one meaningful unit of organizational memory.

Recommended fields:

- `title` (Data): concise event title.
- `description` (Text Editor or Small Text): main event narrative.
- `activity_type` (Link to Activity Type): configured event category.
- `event_datetime` (Datetime): when the event occurred.
- `status` (Select): open, in progress, done, needs attention, archived.
- `outcome` (Small Text): result or decision.
- `next_action` (Small Text): optional next step.
- `due_date` (Date): optional follow-up date.
- `visibility` (Select): private, team, department, organization, restricted.
- `department` (Link or Dynamic configuration): optional team grouping.
- `location` (Data): optional location text.
- `tags` (Data or Tag integration): searchable labels.

Child/reference fields should support multiple generic document links using Dynamic Link conventions.

## Activity Type

Purpose: configure user-facing event categories.

Recommended fields: title, description, icon, color, enabled, default visibility, requires outcome, requires next action.

## Reaction Type

Purpose: configure available reaction and appreciation types.

Recommended fields: title, emoji or icon, color, enabled, counts as appreciation, display order.

## Reaction

Purpose: capture a user's reaction to a timeline event.

Recommended fields: timeline event, reaction type, user, note, created datetime.

## ProgressOS Settings

Purpose: hold global application settings.

Recommended fields: default visibility, enable reactions, enable mentions, enable AI, AI provider, digest settings, reminder defaults, notification defaults.

## Non-Goals for MVP DocTypes

Do not add workflow-heavy or analytics DocTypes in the first implementation pass. Capture the smallest stable event model before adding specialized behavior.
