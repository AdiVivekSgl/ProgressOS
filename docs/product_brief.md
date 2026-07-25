# ProgressOS – Product Brief

> This is the canonical product brief. It deliberately establishes product vision,
> architecture, and the first milestone before implementation details. All other
> documents in `docs/` are derived from and must stay consistent with this brief.

## Vision

ProgressOS is an open-source Frappe application that transforms ERPNext from a system
of transactions into a system of organizational memory.

ERPNext records **what happened** (Lead, Quotation, Sales Order, Invoice).
ProgressOS records **how it happened**.

Every meaningful interaction, observation, decision, discussion, insight, challenge,
and achievement becomes part of a searchable organizational timeline.

The objective is not employee surveillance. The objective is to:

- Capture institutional knowledge
- Improve collaboration
- Encourage continuous recognition
- Provide AI with rich organizational context
- Reduce dependence on WhatsApp, email and memory
- Make work visible without creating administrative burden

## Design Philosophy

ProgressOS should feel more like:

- GitHub Activity
- LinkedIn Feed
- Slack Threads
- Notion Timeline

than:

- Daily Work Reports
- CRM Call Logs
- Employee Monitoring Software

The primary design goal is:

**Logging meaningful work should take less than 30 seconds.**

## Product Principles

### 1. Event Driven

Everything is an Event. Not every event is a task. Not every event is a transaction.

Examples:

- Customer Visit
- Phone Call
- Competitor Information
- Internal Discussion
- Sample Dispatch
- Production Delay
- Engineering Suggestion
- Customer Complaint
- AI Insight
- Recognition
- Automated Notification

The system should revolve around events.

### 2. ERP Agnostic

The application must not assume ERPNext. It should work with:

- ERPNext
- CRM
- HRMS
- Helpdesk
- Custom Frappe Applications

Everything should be configurable.

### 3. Document Agnostic

Events can be attached to any DocType. Examples: Customer, Lead, Opportunity,
Quotation, Sales Order, Supplier, Issue, Project, Task, Asset, Work Order, or any
custom DocType.

Never hardcode business objects.

### 4. AI Native

AI should not be an add-on. ProgressOS should be designed assuming AI will eventually
become the primary consumer of timeline data. AI integrations should remain
provider-independent.

Possible providers:

- OpenAI
- Claude
- Gemini
- Raven
- Ollama
- Future providers

### 5. Social First

ProgressOS is not a reporting tool. It is a collaborative work feed. Users should
naturally browse activity the way they browse Slack or LinkedIn.

## Repository

- **Repository Name:** progress_os
- **Frappe App:** progress_os
- **License:** GPL v3 (recommended)
- **Python:** Latest supported by Frappe
- **Framework:** Frappe v15+

## High-Level Modules

### Timeline

Core event engine. Responsible for:

- Timeline Events
- Attachments
- Comments
- References
- Activity Types

### Feed

Provides: Activity Feed, Filters, Notifications, Infinite Scroll, Personalized Views.

### Recognition

Provides: Reactions, Recognition, Appreciations, Badges.

### Actions

Provides: Follow Ups, Next Actions, Escalations, Reminders.

### Intelligence

Provides: Daily Summary, Weekly Digest, Monthly Digest, AI Summaries, Trend Detection.

### Analytics

Provides: Dashboards, Activity Reports, Team Metrics, Heatmaps.

### Search

Provides: Global Timeline Search, AI Search, Semantic Search (future).

## Phase 1 Scope (MVP)

The first milestone should intentionally remain small. Deliver only the minimum
framework required.

### Core DocTypes

- Timeline Event
- Activity Type
- Reaction Type
- Reaction
- ProgressOS Settings

Nothing else initially.

### Timeline Event Requirements

Each event should contain:

**Basic**

- Title
- Description
- Event Type
- Date/Time
- Created By

**Relationships**

Allow linking to one or more arbitrary documents. This linkage must be generic using
Frappe's Dynamic Link pattern wherever possible.

**Progress**

- Status
- Outcome
- Next Action
- Due Date

**Collaboration**

- Comments
- Mentions
- Attachments

**Recognition**

- Reactions
- Appreciations

**Metadata**

- Tags
- Visibility
- Department
- Location (optional)

## User Experience Goals

Logging an event should require:

- One click
- One dropdown
- One text box

No complex forms. No unnecessary mandatory fields. The experience should be faster
than sending a WhatsApp message.

### Feed

Provide a workspace showing: Recent Activity, My Activity, Team Activity, Mentions,
Needs Attention, Recognition, Recent Wins.

The feed should become the default landing page for users.

### Configuration

Administrators should configure: Activity Types, Recognition Types, Departments,
Visibility Rules, Notification Rules, AI Provider, Reminder Policies.

No business logic should require code changes.

## Extensibility

ProgressOS should expose hooks/events for developers. Examples:

- `on_event_created`
- `on_event_updated`
- `on_reaction_added`
- `on_action_completed`
- `on_digest_generated`

External applications should be able to subscribe.

## Coding Standards

- Follow standard Frappe conventions.
- Avoid unnecessary custom JavaScript where framework features exist.
- Use Workspaces instead of custom pages where possible.
- Keep client-side logic lightweight.
- Prefer server-side business rules.
- Document every public class and API.
- Write unit tests for core functionality.
- Maintain a clean modular architecture with minimal coupling.

## Deliverables for Phase 1

Do not implement features immediately. Instead, produce:

1. Repository structure
2. Initial Frappe app scaffold
3. Architecture document
4. Data model
5. Module boundaries
6. DocType specifications
7. API design
8. Permission model
9. UI wireframes
10. Development roadmap

Only after the architecture is approved should implementation begin.

## Long-Term Vision

ProgressOS should become a generic Frappe application that captures the operational
narrative of an organization.

- ERP systems record transactions.
- Document Management Systems store files.
- CRMs track customers.

ProgressOS should capture the conversations, decisions, observations, progress, and
context that connect everything together.

Its ultimate goal is to become the organization's living memory, enabling better
collaboration, richer AI insights, and a continuously evolving knowledge base rather
than a collection of isolated business records.
