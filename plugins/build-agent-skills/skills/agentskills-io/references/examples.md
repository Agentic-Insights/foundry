# Agent Skills Examples

## Minimal Skill (PDF Text Extraction)

```yaml
---
name: extract-pdf-text
description: Extract text from PDFs using PyPDF2. Use when processing documents or invoices.
license: MIT
---
# Extract PDF Text

## Prerequisites
- Python 3.8+, PyPDF2 (`pip install PyPDF2`)

## Usage
```python
from PyPDF2 import PdfReader
reader = PdfReader('doc.pdf')
for page in reader.pages:
    print(page.extract_text())
```
```

## Standard Skill (AWS Lambda)

```yaml
---
name: deploy-lambda-function
description: Deploy Python functions to AWS Lambda with dependencies. Use for serverless APIs or event processors.
license: Apache-2.0
compatibility: AWS CLI 2.x, Python 3.9+, valid AWS credentials
metadata:
  author: agentic-insights
  version: "1.0.0"
  category: aws-deployment
allowed-tools: bash aws zip python
---
# AWS Lambda Deployment

## Prerequisites
- AWS CLI configured, IAM role ARN for Lambda

## Quick Deploy
```bash
python scripts/deploy.py --function-name my-fn --handler handler.lambda_handler --runtime python3.9
```

## Troubleshooting
- **Size limit**: Use Lambda Layers for large deps
- **Timeout**: Increase in config (max 900s)
- **AccessDenied**: Need `lambda:CreateFunction`, `iam:PassRole` permissions
```

## Complex Skill (K8s Deploy with Progressive Disclosure)

```yaml
---
name: k8s-app-deploy
description: Deploy apps to Kubernetes with health checks and rollback. Use for microservices or APIs on K8s.
license: Apache-2.0
compatibility: kubectl, docker, helm 3.x, valid kubeconfig
metadata:
  author: devops-team
  version: "2.0.0"
  difficulty: advanced
allowed-tools: bash kubectl docker helm
---
# Kubernetes Deployment

## Quick Deploy
```bash
python scripts/quick-deploy.py --app my-api --image myregistry/my-api:v1.0.0 --namespace prod
```

## References
- [Deployment patterns](references/deployment-patterns.md)
- [Configuration](references/configuration.md)
- [Troubleshooting](references/troubleshooting.md)
```

## Key Patterns

| Pattern | When | Example |
|---------|------|---------|
| Minimal | Simple tools | 50-100 lines, no refs |
| Standard | Most skills | 200-300 lines, scripts/ |
| Progressive | Complex domains | <200 lines main, refs for details |
