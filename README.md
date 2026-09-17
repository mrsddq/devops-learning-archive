# DevOps Learning Archive

DevOps learning and reference archive covering Linux, Git, Jenkins, Maven, Tomcat, Docker, Kubernetes, Terraform, AWS, and Azure.

This repository is intentionally an archive, but it now has a learning spine so the material reads as a coherent DevOps path instead of disconnected notes.

## Structure

```text
DevOps-AWS/       AWS, Jenkins, Terraform, Tomcat, YAML, and pipeline notes
DevOps-Azure/     Azure Terraform labs
Revision/         Docker and container revision examples
docs/
  roadmap.md
  labs-index.md
  command-checklist.md
  production-readiness.md
scripts/
  devops_audit.py
devops_toolkit/
tests/
```

## Learning Path

1. Linux, Git, and shell fundamentals
2. CI with Jenkins
3. Java build and deployment with Maven and Tomcat
4. Docker images and containers
5. Kubernetes workloads and services
6. Terraform infrastructure as code
7. AWS and Azure deployment patterns
8. Monitoring, quality gates, and release discipline

## Recommended Portfolio Use

Keep this repository as a learning archive. For showcase work, extract polished labs into separate focused repos such as:

- `terraform-aws-webapp`
- `jenkins-tomcat-pipeline`
- `docker-kubernetes-labs`
- `azure-terraform-foundations`

Use [docs/SHOWCASE_EXTRACTION_PLAN.md](docs/SHOWCASE_EXTRACTION_PLAN.md) to decide what should become a focused repo.

## Repository Audit

Python 3.11 and the standard library are sufficient; there is no package-install step. Run from the repository root:

```bash
python scripts/devops_audit.py --strict
python -m devops_toolkit.cli --json
python -m unittest discover -s tests
```

The toolkit inventories Terraform, Kubernetes YAML, Jenkins/Groovy, Dockerfiles, and documentation. It flags common repository hygiene issues such as unpinned Docker base images, missing Docker copy sources, unpinned Kubernetes image tags, and secret-like markers.

## What the checks establish

The unit tests exercise the archive auditor and its command-line entry point. The JSON command produces an inventory and findings report; `--strict` fails when policy findings remain. This is a static heuristic audit, not a Terraform plan, Kubernetes deployment test, or proof that historical labs are secure. Run old provisioning commands only after reviewing their account, cost, credentials, and cleanup assumptions.

Earlier lesson files and attribution are preserved as a learning record. For the maintained standalone auditing project, see [DevOps Policy Audit Toolkit](https://github.com/mrsddq/devops-policy-audit-toolkit).
