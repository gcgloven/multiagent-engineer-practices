# Prepare a release decision for the actual environment

Use this reference when a candidate is being handed to maintainers, piloted with other systems, or considered for live operation. Select the target, operating envelope, and accountable decision owner using the A, B, and C definitions below and the actual project's requirements.

## Evidence to assemble

Identify the exact candidate, configuration, compatible dependencies, installation/run instructions, and accepted criteria. Relate them to the current roadmap increment and proposed transition: which behavior has been demonstrated, which quality constraints have been accepted, and which readiness evidence is still missing. State what the candidate can do and what its evidence does not cover. Include known limitations and unresolved risks with owners. A claim such as “handles retries” must state whether it means sequential duplicate events, concurrent delivery, restart recovery, or a combination.

Plan observations that distinguish healthy operation from silent failure. For a stateful service, these may include rejected transitions, failed/stalled work, queue age, error rate, and dependency health. Define units, thresholds or interpretation, and who responds. Avoid logging secrets or retaining unnecessary sensitive data.

Describe recovery in operational terms: how to stop new effects, identify affected work/data, restore a compatible candidate, reconcile state, and confirm recovery. A binary rollback alone may not undo data or external side effects. Rehearse the relevant recovery path before claiming it works.

## Match the transition

| Target | Concrete questions before accepting the transition |
| --- | --- |
| **A — Internal use** | Can another maintainer set up and run it? Are state lifetime, failure behavior, data correctness, access needs, and ownership clear? Is recovery credible for actual use? |
| **B — Integrated pilot** | Have actual consumer contracts and representative failures been exercised? Are exposure, users, duration, monitoring, stop conditions, and fallback defined? Has recovery been exercised with representative state? |
| **C — Live industrial operation** | Has the responsible engineering/operational authority identified hazards, governing assurance requirements, protective boundaries, safe-state behavior, intervention and commissioning evidence? Does the candidate satisfy that project-specific process? |

Do not fill evidence gaps with a generic checklist or a previous target's PASS. Record `not demonstrated` and the owner/next test. A laboratory fixture does not establish resilience of the deployed system, and the workflow does not certify equipment safety.

Prepare the candidate and evidence within existing authorization, then obtain any required release decision for that candidate and environment. A pending release decision should not prevent already authorized local checks and preparation. Deployment, operational mutation, or equipment actuation requires the applicable authority.

Give the decision owner a substantive chat readiness account with canonical evidence links: accepted scope, unmet criteria, operating instructions, recovery/ownership, and the proposed next action. Include a compact evidence table or focused visual when it clarifies the readiness judgment. A pile of attachments or a test count alone is not a readiness decision. Preserve the same current record across revisions and update affected evidence rather than publishing repeated bundles by default.

After an authorized pilot or release, compare observations with expected behavior and feed evidence into the roadmap. Good outcomes can justify expansion; failures can justify rollback, a changed design, or a narrower operating envelope.
