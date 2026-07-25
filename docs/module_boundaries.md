# Module Boundaries

## Timeline

Owns timeline events, activity types, generic references, event lifecycle hooks, and validation rules.

## Feed

Owns activity feed queries, filters, personalized views, infinite scroll, and feed rendering conventions.

## Recognition

Owns reaction types, reactions, appreciations, badges, and recognition-oriented feed views.

## Actions

Owns follow-ups, next actions, escalations, reminders, and action completion events.

## Intelligence

Owns AI summaries, provider-independent AI adapters, daily summaries, weekly digests, monthly digests, and trend detection.

## Analytics

Owns dashboards, activity reports, team metrics, and heatmaps.

## Search

Owns global timeline search, AI search, and future semantic search integrations.

## Dependency Rule

Timeline is the only required foundation module. Other modules may depend on Timeline, but Timeline must not depend on Feed, Recognition, Actions, Intelligence, Analytics, or Search.
