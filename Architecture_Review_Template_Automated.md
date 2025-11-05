# Architecture Review Template (Automated Scoring)

This template is designed to standardize architecture reviews across teams.

## Columns
| Column | Description |
|--------|--------------|
| Category | Area of evaluation (e.g., Reliability, Security) |
| Question | Review question for the system |
| Score (1-5) | Numeric score for each question |
| Risk Level (Auto) | Automatically calculated risk level based on score |
| Notes / Findings | Observations or issues found during review |
| Remediation Recommendation | Action items or improvements to implement |

## Automated Scoring Logic
- **Score (1-5)**: Lower scores indicate higher risk.
- **Risk Level (Auto)**: Auto-calculated using Excel formulas.
  - 1–2 = High Risk 🔴
  - 3 = Medium Risk 🟡
  - 4–5 = Low Risk 🟢
- **Color Coding**: Conditional formatting highlights risks:
  - Red for high risk
  - Yellow for medium risk
  - Green for low risk

---
Use this template to capture consistent architecture review data and aggregate results across systems for an organization-wide view of reliability maturity.
