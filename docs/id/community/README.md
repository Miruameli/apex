# Community Docs

Everything a contributor needs: environment setup, contribution rules, and the RFC process.

## Subfolders

| Folder | Scope |
|---|---|
| [`setup/`](setup/) | Dev setup, installation guide, customization |
| [`practice/`](practice/) | Contributing, code of conduct, key custody policy |
| [`rfc/`](rfc/) | RFC process for large proposals |

## Start here

| Goal | Read |
|---|---|
| First run on a new machine | [`setup/50-dev-setup.md`](setup/50-dev-setup.md) |
| Install a released build | [`setup/56-installation-guide.md`](setup/56-installation-guide.md) |
| Submit a pull request | [`practice/10-contributing.md`](practice/10-contributing.md) |
| Propose a large change | [`rfc/53-rfc-process.md`](rfc/53-rfc-process.md) |
| Configure provider keys | [`practice/09-security-key-custody.md`](practice/09-security-key-custody.md) |
| Change defaults and theme | [`setup/08-customization.md`](setup/08-customization.md) |

## Ground rules

1. Read `CONTRIBUTING.md` in the repo root before opening a PR.
2. Conventional Commits for every commit message.
3. Tests required for any logic change.
4. Documentation updated in the same PR as the behavior change.
5. Keys stay local; never commit `.env`.
