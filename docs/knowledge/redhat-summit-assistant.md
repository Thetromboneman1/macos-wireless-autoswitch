# Red Hat Summit Knowledge Assistant

Date: 2026-06-23
Owner: Enterprise Architecture

## Purpose

The Red Hat Summit Knowledge Assistant translates Summit notes, announcements, and platform implications into architecture, automation, and executive artifacts.

## Sources

| Source | Use |
|---|---|
| Summit notes | Session takeaways, vendor direction, product signals |
| Announcements | New capabilities, lifecycle changes, roadmap implications |
| Architecture implications | Impact on TAP Lite, ADRs, standards, risk |
| Platform implications | AAP, Satellite, local AI, operations, governance impact |
| Executive priorities | Decision framing, funding, timing, risk language |

## Capabilities

| Capability | Output |
|---|---|
| Announcement triage | Ranked implications with owner and timing |
| Architecture implication review | Standards changes, ADR candidates, TAP Lite inputs |
| Platform implication review | AAP, Satellite, operations, security, governance actions |
| Executive briefing | Concise leadership summary with decision asks |
| Follow-up backlog | Owner-tagged action list with validation needs |

## Workflow

1. Attach Summit notes or announcement summaries.
2. Classify each item by domain, urgency, and business impact.
3. Route architecture items to Enterprise Architecture Copilot.
4. Route automation items to AAP Platform or Automation Discovery Copilot.
5. Route lifecycle and compliance items to Satellite Platform Copilot.
6. Route leadership narrative to Executive Communications Copilot.

## Validation

The assistant is valid when every recommendation names a source note, impact area, owner, next action, and whether the item is fact, inference, or open question.
