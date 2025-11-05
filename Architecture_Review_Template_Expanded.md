# Architecture Review Template (Expanded)

This template is designed for in-depth architecture assessments across multiple teams and systems.

Each category includes 15 detailed review questions crafted for architects.

## Reliability & Redundancy

| Question | Score (1-5) | Risk Level | Notes / Findings | Remediation Recommendation |
|-----------|--------------|-------------|------------------|-----------------------------|
| Are services deployed across multiple availability zones or regions? |  |  |  |  |
| Is failover automated and periodically tested under real load? |  |  |  |  |
| Do all services have clear RTO and RPO objectives defined? |  |  |  |  |
| Are critical dependencies (e.g., databases, queues) deployed redundantly? |  |  |  |  |
| Are load balancers configured for health-based traffic distribution? |  |  |  |  |
| Is stateful session management avoided or externalized? |  |  |  |  |
| Do you employ active-active or active-passive failover for services? |  |  |  |  |
| Are retry policies and circuit breakers implemented for downstream dependencies? |  |  |  |  |
| Are there service-level redundancy plans for DNS and ingress endpoints? |  |  |  |  |
| Is caching infrastructure replicated or resilient to cache misses? |  |  |  |  |
| Do you use Azure Availability Sets or Zone Redundant Services where applicable? |  |  |  |  |
| Is there a backup communication mechanism for critical alerts (e.g., alternate region)? |  |  |  |  |
| Are external APIs handled gracefully in case of provider downtime? |  |  |  |  |
| Do you perform game days or chaos testing to validate resiliency? |  |  |  |  |
| Is a rollback or degradation strategy defined for partial outages? |  |  |  |  |

## Scalability & Performance

| Question | Score (1-5) | Risk Level | Notes / Findings | Remediation Recommendation |
|-----------|--------------|-------------|------------------|-----------------------------|
| Can the system auto-scale based on CPU, memory, or custom metrics? |  |  |  |  |
| Have you validated scale-out and scale-in behavior under production load? |  |  |  |  |
| Are there any components that limit horizontal scalability? |  |  |  |  |
| Is asynchronous processing used for long-running workloads? |  |  |  |  |
| Do you use caching effectively to reduce database and API load? |  |  |  |  |
| Are there established SLAs and performance thresholds per service? |  |  |  |  |
| Do you perform regular load and stress testing? |  |  |  |  |
| Is there a clear capacity planning and forecasting process? |  |  |  |  |
| Are hotspots identified through profiling and telemetry? |  |  |  |  |
| Is content delivery optimized using CDN or edge caching? |  |  |  |  |
| Is latency between dependent services monitored and acceptable? |  |  |  |  |
| Are thread pools, queues, and connections tuned for concurrency? |  |  |  |  |
| Are resource limits defined and enforced in Kubernetes or App Service plans? |  |  |  |  |
| Can the system gracefully handle burst traffic or sudden load spikes? |  |  |  |  |
| Are database queries and indexes optimized for scale? |  |  |  |  |

## Data Management & Backup

| Question | Score (1-5) | Risk Level | Notes / Findings | Remediation Recommendation |
|-----------|--------------|-------------|------------------|-----------------------------|
| Are production databases replicated across regions? |  |  |  |  |
| Are backups automated and periodically validated for integrity? |  |  |  |  |
| Are transactional logs retained per compliance requirements? |  |  |  |  |
| Is data encrypted in transit and at rest? |  |  |  |  |
| Are storage accounts configured for geo-redundant replication? |  |  |  |  |
| Is there a defined data lifecycle management policy (retention/archival)? |  |  |  |  |
| Do you have a documented disaster recovery plan with tested restore procedures? |  |  |  |  |
| Are backups stored in separate Azure regions or vaults? |  |  |  |  |
| Is there versioning enabled for blob and object storage? |  |  |  |  |
| Are schema migrations reversible and validated pre-deployment? |  |  |  |  |
| Is data access governed via least privilege policies? |  |  |  |  |
| Are RPO/RTO values documented and tested during DR drills? |  |  |  |  |
| Is data consistency validated between replicas and caches? |  |  |  |  |
| Are large data transfers optimized via batching or streaming? |  |  |  |  |
| Are recovery processes automated through Infrastructure as Code or scripts? |  |  |  |  |

## Security & Identity

| Question | Score (1-5) | Risk Level | Notes / Findings | Remediation Recommendation |
|-----------|--------------|-------------|------------------|-----------------------------|
| Is Azure AD used as the central identity provider? |  |  |  |  |
| Are all secrets stored securely using Key Vault or managed identities? |  |  |  |  |
| Are role-based access controls implemented consistently? |  |  |  |  |
| Is Multi-Factor Authentication (MFA) enforced for all privileged access? |  |  |  |  |
| Is network segmentation applied through VNets, subnets, and NSGs? |  |  |  |  |
| Are public endpoints restricted or protected with WAF/CDN rules? |  |  |  |  |
| Is encryption (TLS 1.2+) enforced across all ingress and egress channels? |  |  |  |  |
| Are service-to-service communications authenticated and authorized? |  |  |  |  |
| Are logs protected from tampering and securely stored? |  |  |  |  |
| Are vulnerability scans and penetration tests performed regularly? |  |  |  |  |
| Are Azure Policies and Defender for Cloud recommendations applied? |  |  |  |  |
| Is least privilege enforced for managed identities and SPNs? |  |  |  |  |
| Are dependencies scanned for known vulnerabilities (e.g., SCA tools)? |  |  |  |  |
| Are incident response and escalation procedures documented? |  |  |  |  |
| Are customer data isolation and compliance requirements met (e.g., GDPR, SOC2)? |  |  |  |  |

## Observability & Incident Response

| Question | Score (1-5) | Risk Level | Notes / Findings | Remediation Recommendation |
|-----------|--------------|-------------|------------------|-----------------------------|
| Are logs, metrics, and traces collected centrally (e.g., Azure Monitor, App Insights)? |  |  |  |  |
| Do dashboards provide real-time visibility into critical KPIs? |  |  |  |  |
| Are alert thresholds tuned to minimize noise while catching issues early? |  |  |  |  |
| Is synthetic monitoring in place for critical endpoints? |  |  |  |  |
| Are alerts routed to the correct on-call teams with context and runbooks? |  |  |  |  |
| Do logs contain sufficient context (correlation IDs, request metadata)? |  |  |  |  |
| Are distributed traces used to identify cross-service latency? |  |  |  |  |
| Is there a defined post-incident review (PIR) or RCA process? |  |  |  |  |
| Are escalation paths documented and tested periodically? |  |  |  |  |
| Is downtime automatically reported to stakeholders? |  |  |  |  |
| Are error budgets defined and tracked per service? |  |  |  |  |
| Is monitoring coverage verified for all production components? |  |  |  |  |
| Are anomaly detection or ML-based alerting systems used? |  |  |  |  |
| Are runbooks maintained for common operational incidents? |  |  |  |  |
| Do teams conduct regular incident response simulations? |  |  |  |  |

## Deployment & Automation

| Question | Score (1-5) | Risk Level | Notes / Findings | Remediation Recommendation |
|-----------|--------------|-------------|------------------|-----------------------------|
| Is all infrastructure defined and deployed using Infrastructure as Code (IaC)? |  |  |  |  |
| Is there a standardized CI/CD pipeline across teams? |  |  |  |  |
| Are deployments automated, with manual approval gates for production? |  |  |  |  |
| Are blue/green or canary deployments used for critical systems? |  |  |  |  |
| Are rollback procedures automated and validated regularly? |  |  |  |  |
| Are secrets and configuration values injected securely at runtime? |  |  |  |  |
| Is deployment verification automated via smoke or health tests? |  |  |  |  |
| Do pipeline runs include automated linting and static analysis? |  |  |  |  |
| Are environment configurations version-controlled? |  |  |  |  |
| Is drift detection in place for infrastructure environments? |  |  |  |  |
| Are artifacts signed and verified for provenance and integrity? |  |  |  |  |
| Do teams follow consistent branching and release strategies? |  |  |  |  |
| Are pipelines integrated with security scanning and compliance checks? |  |  |  |  |
| Is there a disaster recovery pipeline for redeploying infrastructure? |  |  |  |  |
| Is deployment frequency and change failure rate tracked (DORA metrics)? |  |  |  |  |

