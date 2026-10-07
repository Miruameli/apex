# ADR-0009: Marketplace Plugin Timing — V2 (Not V1)

## Status
Accepted

## Context
The feature matrix (`docs/product/03-feature-matrix.md`) places "Marketplace plugin" in V1, while the marketplace system spec (`docs/engineering/subsystems/extensibility/39-system-marketplace.md`) labels it V2. This discrepancy must be resolved before Phase 2 implementation.

Marketplace requires:
1. **Registry infrastructure** — API for search, publish, install, versioning
2. **Trust model** — Signed skills, community review, permission scanning
3. **Security sandbox** — Docker-level isolation for untrusted skills
4. **Discovery UX** — `apex skill search`, `apex skill install`, `apex skill list --remote`
5. **Governance** — Review process, maintainer verification, audit logging
6. **Hosting & operations** — Domain, CDN, uptime, abuse handling, legal

MVP scope (locked per D11): chat, context, review, commit, ship, skills (local only), MCP (local connectors), TUI, safety.

## Decision
**Marketplace plugin = V2** (not MVP, not V1).

### Timeline
- **MVP**: Local skills only (`apex skill add <local-path>`, `apex skill run <name>`). No registry, no remote install.
- **V1**: Auto-fix, plan mode, local LLM default, cost tracker, theme engine — core productivity features.
- **V2**: Marketplace plugin + voice input + collaboration + multi-agent + Docker sandbox default.

### Rationale for V2 (not V1)
- **Solo OSS dev constraint**: Operating a public skill registry (hosting, moderation, abuse handling, legal, uptime) is platform-level work beyond solo capacity at V1.
- **Security surface**: Remote code execution via skills requires Docker sandbox (V2 per 24-system-security.md level 3), trust model, permission scanning — all V2 infrastructure.
- **Trust model unproven**: Signed skills, community review, maintainer verification need real-world validation before public registry.
- **V1 focus**: Core productivity (auto-fix, plan mode, local LLM, cost tracker, themes) delivers more value to solo devs than marketplace.
- **Decentralized alternative**: Users can share skills via Git repos in V1 (`apex skill add github:user/repo`) without centralized registry.

## Alternatives Considered

### Option A: V1 (as per feature matrix)
- **Pros**: Earlier ecosystem, viral growth potential
- **Cons**: Registry ops burden on solo dev, security surface large, trust model unproven, Docker sandbox not ready

### Option B: MVP (ship with registry)
- **Pros**: Maximum differentiation
- **Cons**: 3-6 months delay on MVP, operational nightmare for solo dev

## Consequences

### Positive
- MVP ships fastest (core value only)
- V1 focuses on solo dev productivity features
- V2 has clear milestone: marketplace + voice + collaboration + multi-agent + Docker default
- Git-based skill sharing works in V1 without registry ops

### Negative
- V1 users cannot `apex skill install <name>` from public registry
- Manual skill sharing via Git in V1

## Mitigations
- V1: Document skill authoring (`SKILL.md` + script) + Git-based install workflow
- V1: Design registry API spec for V2 implementation
- V2: Start with GitHub as decentralized registry backend (GitHub Packages/Releases) to minimize custom infra

## Date
2026-10-07

## Author
Apex Executive

## Review Date
2026-11-07