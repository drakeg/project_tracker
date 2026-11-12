# Sprint Process

This repository uses short, reviewable Agile iterations with explicit sprint
goals, a prioritized backlog, and a stable definition of done.

## Cadence

The default cadence is a one-week sprint. A sprint can close early when its goal
is complete and all included work meets the definition of done. Urgent security
or CI-repair work may interrupt the sprint, but unrelated feature work should
not.

Each sprint should contain a small number of related stories that support one
clear goal. Prefer several focused pull requests over one large mixed pull
request.

## Roles

- Product owner: sets priorities, accepts scope, and decides whether optional
  product work such as billing belongs in the roadmap.
- Development agent: refines stories, implements changes, adds tests/docs,
  watches CI, and keeps backlog/roadmap documentation current.
- Reviewer/maintainer: reviews and merges pull requests and validates behavior
  that requires a running environment.

One person may perform multiple roles.

## Sprint lifecycle

### 1. Backlog refinement

Before a sprint begins:

- review open defects, security findings, dependency work, and product requests;
- split large items into independently testable stories;
- add acceptance criteria;
- identify dependencies and migrations;
- assign a priority and rough size;
- remove or mark obsolete backlog items.

### 2. Sprint planning

Select only enough work to support one sprint goal. Record:

- sprint goal;
- committed stories;
- stretch stories;
- known risks/dependencies;
- validation required before merge.

### 3. Implementation

For every story:

1. create a focused branch;
2. implement the smallest complete change;
3. add or update tests;
4. update user/developer documentation when behavior changes;
5. run lint/format/checks locally or through CI;
6. open a focused pull request;
7. repair the same pull request if CI fails.

### 4. Review and validation

A story is not done merely because code exists. It must satisfy its acceptance
criteria, pass CI, and have current documentation. Docker validation is required
for container/deployment changes.

### 5. Sprint close

At the end of a sprint:

- verify merged code on `master`;
- verify post-merge CI;
- close or update stale issues;
- remove merged branches where supported;
- move unfinished stories back to the backlog;
- record completed work and lessons;
- choose the next sprint goal from the highest-value ready items.

## Definition of ready

A backlog item is ready for a sprint when:

- the user/business outcome is clear;
- acceptance criteria are testable;
- dependencies are known;
- security/data-migration implications are identified;
- the item is small enough for one focused PR or has been split;
- no unresolved product decision blocks implementation.

## Definition of done

A sprint item is complete when:

- implementation is merged to `master`;
- PR CI is green;
- post-merge `master` CI is green;
- Docker validation is green when applicable;
- migrations are committed for model changes;
- tests cover the behavior and important failure modes;
- documentation reflects the current behavior;
- security-sensitive changes avoid exposing secrets or weakening defaults;
- stale/superseded issues are updated or closed;
- the merged feature branch is deleted where supported.

## Story format

Use this format for backlog items and sprint stories:

> **As a** <user/operator/developer>, **I want** <capability>, **so that**
> <outcome>.

Each story should include:

- acceptance criteria;
- priority;
- size;
- dependencies;
- test/validation notes.

## Priority model

- **P0** — production/security/CI blocker; interrupt current sprint.
- **P1** — high-value reliability, security, or core product work.
- **P2** — normal roadmap feature or maintainability work.
- **P3** — polish, convenience, or speculative future work.

## Size model

Use relative sizes rather than time estimates:

- **S** — small, usually one narrow code path and tests.
- **M** — multiple files or behaviors, still one focused PR.
- **L** — should usually be split before sprint commitment.

## Current planning artifacts

- [Product roadmap](ROADMAP.md)
- [Prioritized backlog](BACKLOG.md)

The backlog is the source of truth for upcoming work. The roadmap groups that
work into outcomes and sequencing. This sprint-process document defines how
items move from idea to done.
