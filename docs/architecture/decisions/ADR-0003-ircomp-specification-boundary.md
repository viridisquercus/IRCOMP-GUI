# ADR-0003: IRCOMP specification ownership and staged GUI integration

Status: Selected for GUI architecture; compiler product schema remains provisional

Date: 2026-11-02

## Context

Prepare edits a bounded CRISPR request; Review records decisions over immutable
imported evidence. These workflows are independently useful for ITU. The longer
term direction is a graphical editor/viewer of IRCOMP user specifications and
compiler products. Current local request fields do not express the entire proposed
IRCOMP specification language.

IRCOMP's inspected I/O design selects structured YAML for human-authored requests
and an equivalent structured model for machine consumers. It explicitly leaves the
exact product schema and runtime interfaces unfrozen. GUI architecture must follow
that ownership without treating the local `1.0` exchange as an authoritative copy.

## Decision

1. IRCOMP owns specification semantics, its normalized request model, language
   parser/schema, cartridge validation, formal goals, planning, controller acceptance,
   backend compilation, execution and scientific assessment.
2. IRCOMP-GUI owns workspace persistence, presentation, local editing rules and the
   separate review layer. Prepare is the initial editor of a restricted subset of
   user intent. It must remain useful without an installed compiler.
3. A separately versioned adapter maps supported GUI data to an accepted IRCOMP
   request contract. The internal Study/RequestRevision model stays distinct from
   that contract. Conversion rejects unsupported/unmappable specification meaning;
   it never silently drops constraints or invents missing scientific policy.
4. Workspace data, user specifications, formal goals, plans/IR, backend bundles,
   execution records and scientific evidence retain distinct identities and states.
5. YAML is a representation of IRCOMP-owned semantics. Future form, text and graph
   interfaces must share those semantics and authoritative validation. Reuse the
   accepted IRCOMP parser/validator through its supported boundary; no second
   language implementation or compiler in this repository.
6. Current ITU work retains the local JSON exchange, Prepare/Review/Export and S6
   operation inventory. YAML editing, compiler routes, new policy controls and graph
   editing are deferred. This decision adds no runtime API or schema fields.

The [integration contract and gap register](../ircomp-integration.md) records
mapping obligations, validation boundaries, rollout gates and future acceptance
criteria. It is the entry point for future integration work.

## Alternatives and consequences

| Alternative | Assessment |
| --- | --- |
| Make the workspace schema identical to the compiler request | Conflates review/draft data with scientific intent and couples ITU to an unfinished schema |
| Build YAML/compiler semantics independently in the GUI | Creates competing authorities and inconsistent normalization/validation |
| Implement the full compiler frontend for the November milestone | Expands scope before upstream contracts and basic workflows are ready |
| Explicit local model plus versioned adapter | Selected; preserves delivery scope and makes integration gaps reviewable |

Architectural compatibility is a design obligation, not a claim of current request
interoperability. Some local studies will require additional user-supplied intent
before conversion is possible. Advanced and expert modes remain optional future
work, gated by accepted contracts and capacity.

## Source inspected

[IRCOMP I/O design at ffde336](https://github.com/viridisquercus/IRCOMP/blob/ffde336832dfa8250e4051b9c7f785009ff1e4e8/docs/architecture/contracts/input-output-error-contract.md),
particularly §§2–4, 5.3, 7 and 9. Inspected 2 November 2026. It describes draft
`0.1`, awaiting project-owner acceptance; it does not establish a released parser,
request schema or compiler transport. This ADR selects GUI direction only.
