# Permission Model

## Goals

ProgressOS must make work visible without becoming surveillance software. Permissions should emphasize user trust, clear visibility, and administrator configuration.

## Visibility Levels

- Private: visible only to creator and explicitly mentioned users.
- Team: visible to members of the configured team or department.
- Department: visible within a department boundary.
- Organization: visible to all permitted internal users.
- Restricted: visible only through explicit sharing rules.

## Ownership

Event creators can edit drafts and recent events according to configured policies. Administrators can manage activity types, reaction types, and settings.

## Reference Documents

When an event links to another document, feed visibility should account for both event visibility and the user's permission to read the referenced document where feasible.

## Auditability

System-generated and AI-generated events must clearly identify their source. AI output should never silently overwrite human-authored timeline data.
