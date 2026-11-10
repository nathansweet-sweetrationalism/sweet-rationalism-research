# Consciousness Naturalized: prospective rival tournament v0.1.0

**Date:** 2026-11-10  
**Author:** Nathan Sweet  
**State:** Pre-data *proposal*, not a completed study-specific preregistration.  
**Canonical article:** https://sweetrationalism.com/articles/consciousness/consciousness-naturalized-a-falsifiable-substrate-agnostic-consciousness-theory-ai-biology/

## Primary target and limitation

The organizational hypothesis (RPOC) proposes that conscious perspective may depend on a temporally persistent, endogenously maintained and causally effective form of self/world/action regulation. This is an abductive, **constitutive hypothesis**, not a definition or established identity. Its independently testable engineering claim concerns maintenance, repair and counterfactual control, whereas its phenomenal claim requires additional participant-linked evidence. Do not infer phenomenal experience from engineering success, closure, complexity, self-report alone or biological origin.

The comparison tournament should contain fixed, proponent-specified versions of RPOC, GNW, RPT, HOT, IIT, biological necessity, predictive-processing/active-inference, enactive/sensorimotor and simpler physiological/dynamical accounts. Broad frameworks can have different operationalizations. A failed implementation demotes that specified implementation; a claim of refuting an entire framework demands a bridge showing that the discriminating prediction is entailed by it. Individual projects may narrow the tournament when unavailable measures are explicitly reported.

## Typed variables and independent observation

- `B, τ`: subject/system boundary and timescale, declared before measurement. Boundary choice can change the truth conditions; run preregistered sensitivity alternatives.
- `C`: causal maintenance/repair and temporal-closure variables measured with interventions, not the outcome label.
- `X_G, X_R, X_H, X_I, X_B, X_A`: rival-access, recurrence, metarepresentation, integration, biological and active-inference measures under each signed-off implementation.
- `Y`: participant-linked phenomenal target, assessed by externally calibrated, independent reports and where justified clinical ratings, not `Y := 1[C > c]` or any other closure-derived classification.
- `F`: engineering functionality, viability and restoration time; may be decisive for an agency claim but is not a proxy by stipulation for `Y`.
- `M`: metaproblem judgment or argument that experience is inexplicable; distinguished from presence, intensity and character of experience itself.

Assess measurement provenance, dependency between multiple judges, missingness, blinding, protocol drift and participant capacity. The same observations may contribute to both predictor and outcome only if that dependence is explicitly modeled and the independent-replication claim is withdrawn. Human reports are defeasible evidence, not revelation; machine reports are also evidence of reporting behavior, not automatically phenomenology.

## Five candidate protocols

### P1. Recovery hysteresis

In existing, appropriately approved anesthesia/sleep/recovery datasets, prospectively test whether restoration of causal self/world/action regulation adds prediction of independently assessed recovery state beyond fixed physiological and GNW/RPT/IIT alternatives. Matched physiological covariates, delayed measurements and transition-direction controls are essential. **RPOC loses its distinctive incremental claim** when held-out gain is negligible or a simpler rival predicts the transition equally well under matched degrees of freedom. Hysteresis itself can be generic dynamics; its observation alone would not identify phenomenality.

### P2. Selective perspectival disconnection

Study dissociations among awareness, ownership, agency and self/world integration, with independently calibrated participant reports and specified interventions or natural experiments. A proposal that one construct must track another faces counterexamples in which they dissociate. RPOC, HOT, GNW, RPT and other models must first state which construct and level they predict. **Do not score a change in agency as a consciousness loss by definitional substitution.**

### P3. Endogenous loop versus externally yoked correction

Tier A is an engineered, randomized comparison between causally self-maintained systems and externally corrected replay under resource, latency, memory and output matching, with held-out perturbation families. Measure repair and viability `F`. Tier B is a separately approved human/VR or prosthetic contingent-feedback comparison using independently calibrated ownership, agency and presence `Y`, with live versus yoked feedback and sham controls. Tier A can establish causal engineering differences but **no machine phenomenal labels**. Tier B may be predicted by enactive, IIT and GNW accounts too; distinguish them only where their frozen versions explicitly differ.

### P4. Boundary/topology intervention

Where safe and technically feasible, vary coupling topology or candidate boundaries while controlling gross complexity, recurring information access, behavior and task demands. Require a measurement-invariance audit at each boundary and a causal perturbation that changes the proposed endogenous structure without merely degrading everything. Prioritize discriminating boundary predictions signed off by IIT and active-inference proponents, not straw-man interpretations. If rivals predict the boundary shifts as well or better, RPOC gains no unique credit.

### P5. Metaproblem judgments

Measure judgments about the explanatory gap, confidence in arguments and actual reports of experience separately across explanation and framing interventions. A shift in the judgment `M` after conceptual intervention supports a model of the *judgment*, not an inference that phenomenality is unreal. Loss conditions target explanatory-genealogy claims and do not settle the metaphysical debate.

The structured details, rival mechanisms, forecast contrasts, controls, provenance and loss rules are in `prereg_proposals/P1-HYSTERESIS.json` through `P5-METAPROBLEM.json` and the aggregate `PROSPECTIVE_COMPARISON_PROTOCOL_v0.1.0.json`. Their schema validation is only structural.

## Comparison rule

For a fixed study and fixed outcome `Y`, freeze competing forecasts, covariates, scoring rule, training/tuning procedure and test holdout before outcomes are revealed. A proper score such as Brier or log loss can compare probabilistic discrimination, supplemented by causal-intervention contrasts and an explicit complexity budget. A numerical gain must be accompanied by calibration, uncertainty and evidence that it persists across sites, interventions and subject subgroups; a one-off gain does not establish constitutive necessity. Both positive and negative controls are mandatory. Any model that exceeds the stated flexibility budget is penalized or excluded under a predeclared equal rule.

If RPOC adds no replicated held-out incremental prediction after stronger simpler accounts and matched interventions, demote the **distinctive-marker claim**. If independently measured phenomenal states occur in a case where RPOC says the organization is necessary but is absent under accurate measurement, demote that **necessity** claim. If all required organization is present with validated evidence against the predicted experience, demote the corresponding **sufficiency** claim. Neither loss logically refutes every version of organizational biology. Likewise, support for dynamics does not by itself vindicate phenomenal constitution.

## Registration completion gates

Before any study calls its findings confirmatory, publicly freeze and register:

1. Named population/system, recruitment/data source, exact version and prior exposure to outcomes.
2. Sample size and power, minimal meaningful effect or precision rationale; site, safety/ethics and participant consent, where applicable.
3. Independent construct operationalizations, instruments, calibration and inter-rater dependence.
4. Intervention and allocation, sham/negative controls, exact boundary and temporal grain.
5. Rival versions and proponent-reviewed forecasts, flexibility and cost matching.
6. Primary outcome, scoring equation, uncertainty intervals, exclusion/missingness and multiplicity handling.
7. Holdout partition, preregistered update/loss rule and planned sensitivity analyses.
8. Immutable registry URL/identifier with timestamp **before** the specified confirmatory observations.

None of these fields should be invented to manufacture the appearance of preregistration. Current owner authorization is for publication of the prospective research proposal, not clinical recruitment or intervention. Negative outcomes, failed branches and protocol deviations belong in the public record.
