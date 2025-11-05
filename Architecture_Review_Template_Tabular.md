# Architecture Review Template (Tabular Format)

This template standardizes the architecture review process across teams. Each section corresponds to a review category with questions to assess system resilience and reliability.

## Reliability & Redundancy

| Question | Score (1-5) | Risk Level | Notes / Findings | Remediation Recommendation |
|-----------|--------------|-------------|------------------|-----------------------------|
| Are services deployed across multiple availability zones? |  |  |  |  |
| Is failover automatic and tested periodically? |  |  |  |  |
| Are dependencies (e.g., databases, queues) redundant? |  |  |  |  |

## Scalability & Performance

| Question | Score (1-5) | Risk Level | Notes / Findings | Remediation Recommendation |
|-----------|--------------|-------------|------------------|-----------------------------|
| Can the system handle traffic spikes automatically? |  |  |  |  |
| Are there defined SLAs and performance baselines? |  |  |  |  |
| Is autoscaling configured appropriately? |  |  |  |  |

## Data Management & Backup

| Question | Score (1-5) | Risk Level | Notes / Findings | Remediation Recommendation |
|-----------|--------------|-------------|------------------|-----------------------------|
| Are backups automated and verified? |  |  |  |  |
| Is data replicated across regions? |  |  |  |  |
| Is RPO/RTO clearly defined and achievable? |  |  |  |  |

## Security & Identity

| Question | Score (1-5) | Risk Level | Notes / Findings | Remediation Recommendation |
|-----------|--------------|-------------|------------------|-----------------------------|
| Is identity management centralized and secure? |  |  |  |  |
| Are secrets stored securely (e.g., Key Vault)? |  |  |  |  |
| Are network security groups properly configured? |  |  |  |  |

## Observability & Incident Response

| Question | Score (1-5) | Risk Level | Notes / Findings | Remediation Recommendation |
|-----------|--------------|-------------|------------------|-----------------------------|
| Are logs, metrics, and traces centrally collected? |  |  |  |  |
| Are alerts actionable and noise-controlled? |  |  |  |  |
| Is there an incident response playbook? |  |  |  |  |

## Deployment & Automation

| Question | Score (1-5) | Risk Level | Notes / Findings | Remediation Recommendation |
|-----------|--------------|-------------|------------------|-----------------------------|
| Is infrastructure defined as code (IaC)? |  |  |  |  |
| Is there an automated rollback mechanism? |  |  |  |  |
| Are environment promotions tested and consistent? |  |  |  |  |

