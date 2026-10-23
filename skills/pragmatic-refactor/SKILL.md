---
name: pragmatic-refactor
description: Simplify existing code by removing unnecessary
  complexity, duplication, obsolete logic, and unjustified
  abstractions. Use for refactoring or code simplification
  tasks. Do not use for unrelated feature implementation.
---

# Pragmatic Refactoring

The goal is to reduce complexity while preserving required
behavior and existing contracts.

## Method

1. Understand the relevant implementation and callers.
2. Identify concrete sources of complexity.
3. Separate required complexity from accidental complexity.
4. Apply the smallest coherent simplification.
5. Remove obsolete code and redundant indirection.
6. Verify behavior through focused tests or inspection.

## Simplification Principles

- Prefer fewer concepts over more layers.
- Inline abstractions that have no independent value.
- Eliminate redundant state and duplicated validation.
- Remove unreachable branches when supported by evidence.
- Avoid speculative extensibility.
- Avoid compatibility scaffolding without actual consumers.
- Prefer direct code when abstraction obscures intent.
- Preserve genuine error handling and trust boundaries.

## Constraints

- Do not sacrifice correctness for fewer lines.
- Do not alter public behavior without authorization.
- Do not assume a branch is unreachable without evidence.
- Do not introduce a new architecture merely to simplify
  a local implementation.
- Do not rewrite unrelated code.

## Reporting

Explain only consequential simplifications, behavior
changes, and verification results.

