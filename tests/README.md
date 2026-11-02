# Runtime verification

The local implementation has 33 pytest acceptance cases in
[test_workspace.py](test_workspace.py) and seven Chromium workflows in
[workspace.spec.ts](../web/e2e/workspace.spec.ts). The [verification record](../docs/development/s6-verification.md)
records actual outcomes and their limits; [Development](../docs/development/README.md)
contains reproducible commands.

Tests exercise invalid input atomicity, revisions, source bytes, collection-specific
decisions, Save/reopen/Undo, concurrent Save conflicts, corruption, exact exports,
HTTP types/origins, reactive views, delayed responses and keyboard/focus recovery.
Temporary databases are isolated from normal saved studies. Synthetic examples and
arbitrary test identities are labelled; no scientific result is established.

The [exchange fixtures](../contracts/README.md) remain structural test inputs, not
proof of semantic acceptance on their own. Future formal-language integration has
separate [F01–F10 gates](../docs/architecture/ircomp-integration.md#future-integration-acceptance-criteria);
no current test claims a working YAML/compiler/graph adapter. Real user usability
sessions remain separate from automated browser checks.
