# ADR-0012: Target Acquisition Channel — GitHub + HN + Twitter/X

## Status
Accepted

## Context
Apex targets solo OSS developers. Need 100 active users for V1 validation. Channel strategy must be sustainable, low-cost, and reach the right persona.

## Decision
**Primary: GitHub (permanent discovery) + Hacker News (launch validation) + Twitter/X (ongoing community). Secondary: Reddit cross-post only.**

### Channel Strategy

| Channel | Role | Tactics | Metrics |
|---------|------|---------|---------|
| **GitHub** | Permanent discovery | SEO-optimized repo, topics, stars, social preview, release notes | Stars, clones, traffic |
| **Hacker News** | Launch validation | Show HN at V1 release, engage in comments | Upvotes, comments, referral traffic |
| **Twitter/X** | Ongoing community | Dev updates, tips, user showcases, thread launches | Followers, engagement, referral |
| **Reddit** | Secondary cross-post | r/rust, r/neovim, r/vim, r/programmingtools (cross-post only) | Upvotes, comments |

### Why Not Others
- **Product Hunt**: One-time spike, wrong audience (founders not solo devs)
- **Dev.to / Hashnode**: Low solo-dev density, high content maintenance
- **Discord/Slack**: Support burden > value for solo dev tool
- **Newsletter**: Building list from zero, slow
- **Paid ads**: Against OSS ethos, poor ROI for dev tools

### Launch Sequence (V1)
1. **Week -2**: Prepare repo (README, screenshots, demo GIF, release notes)
2. **Week -1**: Soft launch to followers, collect feedback
3. **Day 0**: GitHub release + Show HN + Twitter thread (coordinated)
4. **Day 1-7**: Engage all comments, fix critical bugs, thank users
5. **Week 2+**: Weekly Twitter tips, monthly GitHub releases, quarterly HN updates

## Alternatives Considered

### Option A: Product Hunt + Dev.to + Newsletter
- **Pros**: Standard "launch playbook"
- **Pros**: Wrong audience, high maintenance, low retention

### Option B: Community-first (Discord + Reddit + Twitter)
- **Pros**: Engaged community
- **Cons**: Support burden unsustainable for solo dev

## Consequences

### Positive
- Low maintenance (GitHub auto-discovery, Twitter async)
- Reaches exact persona (solo devs on HN/Twitter/GitHub)
- Compound effect: stars → discoverability → more stars
- No platform dependency (own repo + public platforms)

### Negative
- HN/Twitter algorithm dependency
- No owned community channel (email/Discord)
- Reddit hostile to self-promotion

## Mitigations
- Build email capture on GitHub Sponsors page (opt-in)
- Cross-post HN thread to Twitter for amplification
- Document "How Apex got first 100 users" for future reference

## Date
2026-10-07

## Author
Apex Executive

## Review Date
2027-01-07