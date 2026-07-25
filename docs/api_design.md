# API Design

## Design Goals

APIs should enable quick event creation, feed retrieval, reactions, and external subscription without assuming ERPNext.

## Planned Public APIs

### `create_event`

Creates a timeline event from minimal input: activity type, description, optional references, and optional metadata.

### `get_feed`

Returns recent timeline events with filters for user, department, reference document, visibility, mentions, and recognition.

### `add_reaction`

Adds or updates a reaction for the current user on a timeline event.

### `remove_reaction`

Removes the current user's reaction from a timeline event.

### `get_reference_timeline`

Returns events attached to any arbitrary document identified by DocType and document name.

## Provider Interfaces

AI providers should implement a narrow interface for summarization, classification, and search enrichment. The interface must stay provider-independent so candidate backends — OpenAI, Claude, Gemini, Raven, Ollama, and future providers — are interchangeable. Provider-specific credentials and prompts belong in configuration, not domain DocTypes.

## Compatibility

APIs should be versioned once exposed publicly. Early internal methods may change until the first tagged release.
