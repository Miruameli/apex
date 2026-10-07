# 39 — System: Agent Skills Marketplace (V2)

## Tujuan

Registry publik skill yang bisa di-install via `apex skill add <name>`.

## Arsitektur (draft V2)

```
User → `apex skill add github:user/repo` → fetch manifest → validate → install ke skills/
```

## Manifest requirements

- `apex.skill.json` valid
- `SKILL.md` dokumentasi lengkap
- Permission scope minimal (least privilege)
- License jelas (MIT/Apache/dll)
- Maintainer info

## Trust model

| Level | Cara |
|---|---|
| `trusted` | Signed by Apex core team |
| `community` | User-submitted, review minimal |
| `local` | Skill lokal, no review |

## Discovery

- `apex skill search <query>` → query registry API
- `apex skill list --remote` → list available
- `apex skill install <name>` → fetch + validate + install

## Security

- Verify signature jika `trusted`
- Scan manifest untuk dangerous permission (`shell: true` + `net: *` = warning)
- Sandbox level sesuai permission (V2: Docker default)
- Audit log setiap skill run

## Marketplace hosting (TBD)

- `skills.apex.dev` (official)
- GitHub-based registry (decentralized)
- Both (hybrid)
