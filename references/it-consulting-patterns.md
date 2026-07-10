# IT consulting patterns

Use these patterns together with `references/content-density.md`. IT, cloud, data, security and AI pages must connect technical design to measurable business or operating outcomes. A diagram without baseline, target, trade-off and implementation evidence is incomplete.

## Cloud migration

Use 6R language where appropriate: rehost, replatform, refactor, repurchase, retire and retain.

Minimum analysis:

- application inventory count and coverage;
- business criticality, technical health, lifecycle and dependency profile;
- current infrastructure and operations cost baseline;
- utilization, availability, incident and recovery metrics;
- migration disposition by workload, not only a conceptual 6R explanation;
- wave capacity, migration factory throughput and critical dependencies;
- one-off migration cost and target-state run cost;
- base, upside and downside TCO scenarios;
- regulatory, residency, security and continuity constraints;
- retained/on-premises rationale and exit conditions.

Common exhibits:

- application portfolio segmentation with counts and spend;
- dependency-aware migration wave plan;
- current-to-target unit-cost benchmark;
- landing-zone architecture with control decisions and target service levels;
- TCO waterfall plus sensitivity;
- operating model and RACI with measurable service KPIs.

Do not use a generic three-wave roadmap without workload counts, exit criteria, owners, dependencies and target outcomes.

## AI transformation

Core modules: use-case prioritization, process baseline, data readiness, model/platform architecture, responsible AI controls, evaluation, adoption and value tracking.

Minimum analysis:

- comprehensive use-case inventory by business function and user group;
- process volume, handling time, labor effort, error rate, conversion or service baseline;
- explicit value mechanism for each use case;
- weighted prioritization criteria and evidence behind scores;
- sensitivity to prioritization weights;
- data source, entitlement, freshness, quality and remediation effort;
- model quality, latency, cost, context limits and deployment constraints;
- evaluation dataset size, metrics, thresholds and failure categories;
- human-in-the-loop design and escalation path;
- inference/platform/implementation cost model;
- adoption curve and productivity-capture assumption;
- counter-evidence on expected productivity or automation benefits;
- stage gates from pilot to production to scale.

Common exhibits:

- use-case portfolio with score detail and value ranges;
- process baseline and value bridge;
- data-readiness heatmap with evidence-based scoring;
- model/platform benchmark table;
- target AI architecture with design decisions and control points;
- evaluation scorecard and release gate;
- hub-and-spoke operating model with ownership and funding;
- value realization dashboard and adoption funnel;
- base/upside/downside business case.

Do not claim a percentage productivity gain without defining the task scope, affected users, adoption, time saved, capture rate and source or assumption.

## Application modernization

Core modules: technical debt, business criticality, modernization pattern, target architecture, dependency analysis and migration waves.

Minimum analysis:

- application count, age, technology stack, support status and ownership;
- incident frequency, lead time, release frequency, change-failure rate and recovery time;
- run cost, license cost, infrastructure cost and maintenance effort;
- business criticality and revenue/process dependency;
- dependency graph and shared-component constraints;
- disposition by application with evidence-based rationale;
- modernization effort, sequencing, resource demand and risk;
- expected KPI improvement and benefit realization timing.

Common exhibits:

- portfolio heatmap with counts, cost and risk;
- technical-debt driver tree;
- dependency map focused on critical migration constraints;
- pattern decision table: replatform/refactor/replace/retire/retain;
- modernization roadmap with application cohorts and exit criteria;
- business-case bridge and sensitivity.

## Data platform

Core modules: data-product strategy, lakehouse/data mesh architecture, governance, lineage, quality, access control and analytics operating model.

Minimum analysis:

- data-source inventory, volume, growth, latency and criticality;
- current pipeline count, failure rate, processing time and operating effort;
- duplication, data-quality incidents and reconciliation effort;
- analytics demand, report count, time-to-data and user adoption;
- regulatory classification, residency and retention requirements;
- target data products, owners, consumers and service levels;
- platform consumption and storage/compute cost drivers;
- interoperability, metadata, lineage and access-control design decisions;
- migration sequence and coexistence period;
- quality, freshness and adoption KPIs.

Common exhibits:

- current-state data-flow and pain-point map;
- data-domain/value mapping;
- target layered architecture with SLAs and controls;
- cost and consumption driver analysis;
- data-product portfolio and ownership model;
- governance RACI and issue-escalation workflow;
- migration roadmap with source counts and exit criteria.

## Security and compliance

Core modules: zero trust, control mapping, data classification, identity, auditability, incident response and regulatory requirements.

Minimum analysis:

- asset, identity, application and data scope;
- current incidents, vulnerabilities, control exceptions and remediation backlog;
- control coverage and effectiveness, not only policy existence;
- regulatory or standard requirements mapped to actual controls;
- maturity scores with evidence and scoring definitions;
- target architecture decisions and enforcement points;
- risk probability, business impact, leading indicators and residual risk;
- remediation effort, owner, timeline, dependencies and acceptance evidence.

Common exhibits:

- evidence-based control heatmap;
- risk matrix with trigger, owner and residual risk;
- regulatory mapping table;
- identity/data/network control architecture;
- remediation roadmap with backlog counts and measurable closure criteria;
- security operating model and escalation cadence.

Do not use generic zero-trust pillars as the main analysis. Show where controls are missing, how the gap is measured and what changes first.

## Vendor and platform evaluation

Minimum analysis:

- requirements traceability;
- official capability evidence;
- test or benchmark results where possible;
- integration, identity, data, security and operational fit;
- pricing units, consumption assumptions and discount boundaries;
- implementation and migration effort;
- portability, exit cost and lock-in;
- roadmap dependency and product limitations;
- customer references relevant to scale and industry;
- weighted scoring and sensitivity.

Separate vendor claims from independently verified facts. Explain the reason for rejecting the second-best option and the safeguards needed for the preferred option.

## Business case

Use CAPEX/OPEX, run-rate savings, productivity benefits, risk reduction, payback, NPV/IRR where appropriate and sensitivity analysis.

Required components:

- current-state cost baseline and source period;
- one-off implementation, migration, data remediation and change cost;
- recurring licenses, consumption, operations, support and staffing;
- benefit categories with owner and realization timing;
- adoption and productivity-capture rates;
- base, upside and downside scenarios;
- sensitivity to the two largest assumptions;
- benefits that are financial versus non-financial;
- double-counting checks;
- confidence and caveat by major assumption.

Always show assumptions and calculation basis. Do not combine avoided cost, cash savings and productivity capacity into one total without explaining whether each item is actually realizable.

## Adoption and operating model

Cover CoE, product ownership, platform ownership, business champions, training, change management, governance cadence, demand intake and benefits tracking.

Minimum analysis:

- target users and affected roles;
- current adoption baseline;
- usage, retention, satisfaction, task completion and productivity KPIs;
- training and support demand;
- centralized versus federated decision rights;
- funding model and prioritization process;
- intake-to-production workflow and stage gates;
- benefit owner and measurement cadence;
- capacity required by central platform and domain teams;
- escalation and exception handling.

Common exhibits:

- hub-and-spoke model with explicit decision rights;
- RACI plus escalation rules;
- intake and release workflow;
- adoption funnel with targets by phase;
- training/coaching plan by user cohort;
- benefits-realization dashboard;
- governance cadence with required inputs and outputs.

## IT roadmap completion gate

Before producing an IT consulting roadmap, confirm that it contains:

1. named workstreams and owners;
2. scoped assets, applications, use cases or data sources by wave;
3. measurable deliverables and exit criteria;
4. architecture, security and operational dependencies;
5. decision gates and approval owners;
6. resource and budget implications;
7. target KPIs by phase;
8. critical path and parallelizable work;
9. top risks and leading indicators;
10. appendix backup for detailed inventory, architecture and cost assumptions.