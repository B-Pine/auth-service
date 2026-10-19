## What

<!-- What does this PR change? One or two sentences. -->

## Why

<!-- Why is this change needed? -->

## Type of change

- [ ] Feature
- [ ] Bug fix
- [ ] Refactor (no behaviour change)
- [ ] Tests only
- [ ] Docs / configuration

## Checklist

- [ ] Targets `develop` (only release PRs target `main`)
- [ ] Commits show the TDD cycle: failing test → minimal code → refactor
- [ ] `pre-commit run --all-files` passes
- [ ] `python -m pytest` passes with 100% coverage
- [ ] New code has tests, including failure cases (duplicates, weak passwords, wrong credentials)
- [ ] Passwords are never stored, logged, or returned in plain text
- [ ] Public modules, classes and functions have Google-style docstrings
- [ ] No duplicated logic: shared code lives in a reusable component