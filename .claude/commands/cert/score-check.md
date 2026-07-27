---
description: Interpret a score report or practice result and decide whether to book, study, or retake
argument-hint: [certification] [your scores, by domain if you have them]
---

Interpret the results in `$ARGUMENTS` and give a decision, not just a summary.

## Input

Accept any of these: a real Pearson score report with its scaled score and percent-correct by domain, results from `/cert:mock` or `/cert:diagnostic` earlier in this session, or informal self-assessment. Ask for the certification if it was not named. If only an overall number was given, ask whether a per-domain breakdown exists, since the decision depends on where the marks were lost, not only how many.

## Analyse

1. Read the certification's `README.md` for domain weights and `mock-exam.md` for the readiness bands.
2. For each domain, compute the gap between the score and a passing standard, then weight that gap by the domain's share of the exam. Rank by the weighted gap: a weak domain worth 33% of the paper matters far more than a weak domain worth 3%.
3. Note any domain that is strong, so time is not wasted there.

## Decide

Give one of three verdicts, with the reasoning shown:

- **Book it.** Scores are comfortably above the band and no heavily weighted domain is weak.
- **Close the gap first.** Name the specific domains and objectives, estimate the study time from the size of the weighted gaps, and recommend `/cert:drill` on each in priority order followed by `/cert:mock`.
- **Rebuild the foundation.** Several heavy domains are weak. Recommend `/cert:prep-plan` and the underlying courses rather than more question practice, since drilling cannot fix material never learned.

For a real failed attempt, add the retake facts from `guide/policies.md`: the waiting period for that attempt number, the four-attempts-per-year limit, and that the fee applies again. Point out that the official score report's per-domain percentages are the most reliable study signal available, and should drive the next plan.
