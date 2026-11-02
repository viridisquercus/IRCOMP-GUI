# Test strategy

No runtime tests exist at the scaffold stage. Add each suite with implemented
behavior; directory names alone do not establish test coverage.

| Level | First useful contracts |
| --- | --- |
| Unit | Interval/identity checks, missing versus zero, revision compatibility |
| Component | Import parser preserves raw evidence; failed import changes no accepted state |
| Integration | Save/reopen round trip; service and persistence agree on revision/decision identity |
| End-to-end | Repair input; attach compatible evidence; change decision; recover; export/reopen |

S5 [exchange fixtures](../contracts/README.md) are available for implementation.
Their structural checks pass; runtime semantic acceptance has not been tested.
Use the [S6 matrix](../docs/architecture/s6-acceptance.md) for operation coverage.

Use small synthetic fixtures beside the owning suite, labelled with format
version, intended case and expected outcome. Do not copy private genomic data.
Scientific correctness is a separate claim from a UI or persistence test.
