# ADR-0011: Business Model — Sponsorship + Future Commercial

## Status
Accepted

## Context
Apex is a solo OSS dev tool (MIT license). Sustainable funding needed for maintenance, infrastructure, and potential full-time work. No VC, no exit pressure.

## Decision
**Business model = GitHub Sponsors + Open Collective (V1-V2) → Commercial dual-license evaluation at V2+ if enterprise demand.**

### Phased Approach
| Phase | Model | Rationale |
|-------|-------|-----------|
| MVP-V1 | GitHub Sponsors + Open Collective | Zero overhead, community-funded, aligns with OSS values |
| V2 | Evaluate commercial dual-license (MIT + commercial) | If enterprise demand proven, dual-license allows corporate adoption while keeping MIT for community |
| V3+ | Add paid features (hosted sync, team management) | Only if user base >10k and clear willingness to pay |

### What Stays Free (MIT Forever)
- Core CLI/TUI: chat, context, review, commit, ship, skills, TUI
- Local MCP connectors
- All current MVP features
- Source code, documentation

### What Could Be Commercial (V2+)
- Hosted skill registry (if marketplace V2)
- Team/organization features (shared config, audit logs)
- Hosted context sync across devices
- Priority support SLA

## Alternatives Considered

### Option A: Pure donations (GitHub Sponsors only)
- **Pros**: Simplest, pure OSS
- **Cons**: Unpredictable, rarely covers full-time

### Option B: Open Core from start
- **Pros**: Clear monetization path
- **Cons**: Community backlash, fragmentation, against solo OSS ethos

### Option C: SaaS from start
- **Pros**: Recurring revenue
- **Cons**: Hosting complexity, not core value, diverts from product

## Consequences

### Positive
- MIT license preserved — community trust maintained
- Low overhead — no billing, no license enforcement
- Flexibility — pivot if needed at V2+
- Aligned with solo dev sustainability

### Negative
- No guaranteed income
- Commercial pivot may alienate purists
- Enterprise sales requires separate effort

## Mitigations
- Transparent funding goals on GitHub Sponsors page
- Clear "what's free forever" documentation
- Commercial features only additive, never subtractive
- Community veto on any MIT feature removal

## Date
2026-10-07

## Author
Apex Executive

## Review Date
2027-04-07