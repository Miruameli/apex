# ADR-0010: Theme/Branding Customization — UI-Only

## Status
Accepted

## Context
The customization doc (`docs/community/setup/08-customization.md`) lists "Tema & branding [OPEN]" with two dimensions:
- **UI theme**: dark/light/user-defined palette (already in `apex.json` → `ui.theme`)
- **Product branding**: logo, colors, product identity

These are distinct concerns. UI theme affects user comfort; product branding affects project identity.

## Decision
**Theme/branding customization = UI-only** (dark/light/user palette). Product branding (logo, colors, name "Apex") is fixed.

### Scope
| Aspect | Customizable? | Mechanism |
|--------|---------------|-----------|
| UI color palette (dark/light/custom) | ✅ Yes | `apex.json` → `ui.theme` |
| UI font, spacing, icons | ✅ Yes | Theme config |
| Product name "Apex" | ❌ No | Fixed |
| Product logo | ❌ No | Fixed |
| Product primary colors | ❌ No | Fixed |
| CLI/TUI command names | ❌ No | Fixed per D1, D12 |

### Rationale
- **Brand consistency**: Solo OSS dev tool needs recognizable identity. Customizable logo/colors dilute brand.
- **Scope creep prevention**: Product branding opens endless customization (favicon, splash, about screen, docs theme).
- **User comfort achieved via UI theme**: Dark/light/custom palette covers accessibility and preference needs.
- **Solo dev reality**: Maintaining themeable product branding = design system work, not core value.

## Alternatives Considered

### Option A: Full branding customization (UI + product)
- **Pros**: Forks can rebrand completely
- **Cons**: Design system maintenance, brand dilution, fork confusion, not core value

### Option B: No theming at all (fixed dark only)
- **Pros**: Simplest implementation
- **Cons**: Accessibility issues, user frustration, poor DX

## Consequences

### Positive
- Clear boundary: `ui.theme` = user comfort, product identity = fixed
- Simpler implementation: only UI palette engine needed
- Brand recognition preserved
- Solo dev maintains single design system

### Negative
- Users wanting white-label cannot achieve it
- Fork maintainers must hardcode branding changes

## Mitigations
- Forks can still modify source (MIT license) — just not via config
- Document branding as "not configurable by design" in customization docs

## Date
2026-10-07

## Author
Apex Executive

## Review Date
2026-11-07