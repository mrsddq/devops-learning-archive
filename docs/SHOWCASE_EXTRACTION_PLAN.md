# Showcase Extraction Plan

This repository is strongest as a learning archive plus tooling source. For portfolio presentation, extract focused labs instead of pointing reviewers at every raw note.

## Best Extraction Candidates

| Candidate Repo | Source Material | What It Should Prove |
|---|---|---|
| `terraform-aws-webapp` | `DevOps-AWS/*/main.tf` | Terraform structure, variables, state, and documented teardown. |
| `jenkins-tomcat-pipeline` | Jenkins and Tomcat notes | CI/CD pipeline from build to deploy. |
| `docker-kubernetes-labs` | Docker/Kubernetes YAML notes | Containers, manifests, probes, resources, and local verification. |
| `devops-validation-toolkit` | `devops_toolkit/` | Static analysis CLI with tests and CI. |

## Extraction Standard

- Minimal source files only.
- `README.md` with setup, run, verify, and teardown.
- CI or a reproducible local verification command.
- Screenshots or terminal output for the final state.
- No cloud credentials, generated state, or local machine paths.
