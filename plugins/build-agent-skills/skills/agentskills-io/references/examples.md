# Agent Skills Examples

This document provides complete, real-world examples of Agent Skills for different use cases and complexity levels.

## Example 1: PostgreSQL Migration Skill

A complete skill for managing database migrations with rollback support.

```yaml
---
name: postgres-migration
description: Create and run database migrations for PostgreSQL with rollback support. Use when adding tables, modifying schemas, or seeding data in PostgreSQL databases.
license: MIT
metadata:
  author: example-org
  version: "1.2.0"
  category: database
  difficulty: intermediate
---

# PostgreSQL Migration Skill

Manage database schema changes with version control and rollback capabilities.

## Prerequisites

- PostgreSQL 14+ installed and running
- `psql` client available in PATH
- Database connection string in `DATABASE_URL` environment variable
- Python 3.10+ for migration scripts

## Creating a Migration

### 1. Generate Migration File

```bash
python scripts/create-migration.py --name add_users_table
```

This creates a timestamped file: `migrations/YYYYMMDD_HHMMSS_add_users_table.sql`

### 2. Write UP Migration

Add the changes to apply:

```sql
-- UP
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

### 3. Write DOWN Migration

Add the rollback logic:

```sql
-- DOWN
DROP INDEX IF EXISTS idx_users_email;
DROP TABLE IF EXISTS users;
```

## Running Migrations

### Apply All Pending Migrations

```bash
python scripts/migrate.py up
```

**Expected Output**:
```
Running migrations...
✓ 20240101_120000_add_users_table.sql
✓ 20240102_140000_add_posts_table.sql
Applied 2 migrations successfully
```

### Rollback Last Migration

```bash
python scripts/migrate.py down
```

**Expected Output**:
```
Rolling back...
✓ Reverted 20240102_140000_add_posts_table.sql
Rollback completed successfully
```

### Check Migration Status

```bash
python scripts/migrate.py status
```

**Expected Output**:
```
Migration Status:
✓ 20240101_120000_add_users_table.sql (applied)
✓ 20240102_140000_add_posts_table.sql (applied)
○ 20240103_150000_add_comments_table.sql (pending)
```

## Troubleshooting

**Issue**: "Permission denied for database"
**Solution**: Grant necessary permissions:
```sql
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
GRANT ALL ON ALL TABLES IN SCHEMA public TO myuser;
```

**Issue**: Migration fails partway through
**Solution**:
1. Check `migrations/.applied` to see what succeeded
2. Manually rollback partial changes if needed
3. Fix the migration SQL
4. Re-run with `--force` flag

**Issue**: "relation already exists"
**Solution**: Migration may have been applied manually. Options:
1. Mark as applied without running: `python scripts/migrate.py mark-applied <migration-name>`
2. Add `IF NOT EXISTS` clauses to migration SQL

## Advanced Usage

### Seed Data Migrations

```sql
-- UP
INSERT INTO users (email) VALUES
  ('admin@example.com'),
  ('user@example.com')
ON CONFLICT (email) DO NOTHING;
```

### Dependent Migrations

```sql
-- UP
ALTER TABLE posts
  ADD COLUMN user_id INTEGER REFERENCES users(id);

UPDATE posts SET user_id = 1 WHERE user_id IS NULL;

ALTER TABLE posts
  ALTER COLUMN user_id SET NOT NULL;
```

### Data Transformation Migrations

```sql
-- UP
-- Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);

-- Populate from existing data
UPDATE users SET full_name = first_name || ' ' || last_name;

-- Drop old columns
ALTER TABLE users DROP COLUMN first_name;
ALTER TABLE users DROP COLUMN last_name;
```
```

## Example 2: AWS Lambda Deployment Skill

A skill for deploying serverless functions.

```yaml
---
name: deploy-lambda-function
description: Package and deploy Python functions to AWS Lambda with dependencies, environment variables, and IAM roles. Use when creating serverless APIs, event processors, or scheduled tasks on AWS.
license: Apache-2.0
compatibility: Requires AWS CLI 2.x, Python 3.9+, valid AWS credentials
metadata:
  author: agentic-insights
  version: "1.0.0"
  category: aws-deployment
  difficulty: intermediate
  estimated-time: 15min
allowed-tools: bash aws zip python
---

# AWS Lambda Deployment Skill

Deploy Python functions to AWS Lambda with proper dependency packaging and configuration.

## Prerequisites

- AWS CLI installed and configured (`aws configure`)
- Python 3.9 or later
- Valid AWS credentials with Lambda permissions
- IAM role ARN for Lambda execution

## Quick Start

Deploy a simple function:

```bash
# 1. Create function
cat > handler.py <<'EOF'
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }
EOF

# 2. Package and deploy
python scripts/deploy.py \
  --function-name my-function \
  --handler handler.lambda_handler \
  --runtime python3.9 \
  --role arn:aws:iam::123456789012:role/lambda-execution-role
```

## Step-by-Step Deployment

### 1. Prepare Function Code

Create your Lambda handler:

```python
# handler.py
import json
import boto3

def lambda_handler(event, context):
    """
    Process incoming events and return response.
    """
    # Your business logic here
    print(f"Received event: {json.dumps(event)}")

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'Success',
            'requestId': context.request_id
        })
    }
```

### 2. Add Dependencies

If your function requires external packages, create `requirements.txt`:

```txt
boto3==1.26.0
requests==2.28.1
python-json-logger==2.0.4
```

### 3. Configure Deployment

Create `config.json`:

```json
{
  "function_name": "my-api-function",
  "handler": "handler.lambda_handler",
  "runtime": "python3.9",
  "role_arn": "arn:aws:iam::123456789012:role/lambda-role",
  "memory_size": 256,
  "timeout": 30,
  "environment": {
    "STAGE": "production",
    "LOG_LEVEL": "INFO",
    "API_KEY": "{{SSM:/my-app/api-key}}"
  },
  "vpc_config": {
    "subnet_ids": ["subnet-12345", "subnet-67890"],
    "security_group_ids": ["sg-12345"]
  }
}
```

### 4. Deploy

```bash
python scripts/deploy.py --config config.json
```

**Expected Output**:
```
Packaging dependencies...
✓ Installed 3 packages
Creating deployment package...
✓ Created lambda-package.zip (2.3 MB)
Deploying to AWS...
✓ Function deployed: arn:aws:lambda:us-east-1:123456789012:function:my-api-function
✓ Version: $LATEST

Function URL: https://abc123.lambda-url.us-east-1.on.aws/
```

### 5. Test Deployment

Invoke the function:

```bash
aws lambda invoke \
  --function-name my-api-function \
  --payload '{"test": "data"}' \
  output.json

cat output.json
```

## Advanced Configuration

### Environment Variables from AWS Systems Manager

Reference SSM parameters in your config:

```json
{
  "environment": {
    "DB_HOST": "{{SSM:/myapp/db/host}}",
    "DB_PASSWORD": "{{SSM:/myapp/db/password}}",
    "API_KEY": "{{SSM:/myapp/api-key}}"
  }
}
```

The deployment script resolves these automatically.

### VPC Configuration

Deploy Lambda inside VPC for database access:

```json
{
  "vpc_config": {
    "subnet_ids": ["subnet-private-1", "subnet-private-2"],
    "security_group_ids": ["sg-lambda"]
  }
}
```

**Note**: Requires NAT Gateway for internet access and longer cold start times.

### Layers for Shared Dependencies

Use Lambda Layers for common dependencies:

```bash
# Create layer
python scripts/create-layer.py \
  --name my-common-libs \
  --requirements requirements-layer.txt

# Deploy with layer
python scripts/deploy.py \
  --config config.json \
  --layers arn:aws:lambda:us-east-1:123456789012:layer:my-common-libs:1
```

## Troubleshooting

**Issue**: "Unzipped size must be smaller than X bytes"
**Solution**:
1. Use Lambda Layers for large dependencies
2. Remove unnecessary packages from requirements.txt
3. Consider using Lambda Container Images for large applications

**Issue**: Function times out
**Solution**:
1. Increase timeout in config.json (max 900 seconds)
2. Check CloudWatch Logs for bottlenecks
3. Optimize database queries or API calls

**Issue**: "AccessDeniedException" when deploying
**Solution**: Ensure IAM user/role has these permissions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:CreateFunction",
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration",
        "iam:PassRole"
      ],
      "Resource": "*"
    }
  ]
}
```

**Issue**: Cannot connect to RDS from Lambda
**Solution**:
1. Verify Lambda and RDS are in same VPC
2. Check security group rules allow traffic
3. Ensure NAT Gateway exists for internet access
4. Verify RDS credentials in environment variables

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy Lambda
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      - run: python scripts/deploy.py --config config.json
```

## Monitoring

After deployment, monitor your function:

```bash
# View recent logs
aws logs tail /aws/lambda/my-api-function --follow

# Get metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=my-api-function \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```
```

## Example 3: PDF Processing Skill (Minimal)

A minimal skill demonstrating the simplest valid structure.

```yaml
---
name: extract-pdf-text
description: Extract text content from PDF files using PyPDF2. Use when processing documents, invoices, or reports to retrieve plain text.
license: MIT
---

# Extract PDF Text

Extract text from PDF files and save to text files.

## Prerequisites

- Python 3.8+
- PyPDF2 library (`pip install PyPDF2`)

## Usage

```python
from PyPDF2 import PdfReader

def extract_text(pdf_path, output_path):
    """Extract all text from PDF to text file."""
    reader = PdfReader(pdf_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        for page in reader.pages:
            text = page.extract_text()
            f.write(text)
            f.write('\n\n--- Page Break ---\n\n')

    print(f"Extracted {len(reader.pages)} pages to {output_path}")

# Example
extract_text('invoice.pdf', 'invoice.txt')
```

## Expected Output

```
Extracted 3 pages to invoice.txt
```

The output file will contain all text from the PDF, with page breaks marked.
```

## Example 4: Multi-Tool DevOps Skill (Complex)

A comprehensive skill combining multiple tools and workflows.

```yaml
---
name: k8s-app-deploy
description: Deploy containerized applications to Kubernetes with health checks, rolling updates, and automatic rollback. Use when deploying microservices, APIs, or batch jobs to Kubernetes clusters.
license: Apache-2.0
compatibility: Requires kubectl, docker, helm 3.x, valid kubeconfig
metadata:
  author: devops-team
  version: "2.0.0"
  category: kubernetes
  difficulty: advanced
  estimated-time: 45min
  tags: [kubernetes, docker, helm, deployment, devops]
allowed-tools: bash kubectl docker helm
---

# Kubernetes Application Deployment

Deploy containerized applications to Kubernetes with production-grade reliability patterns.

## Prerequisites

- Kubernetes cluster (1.24+) with kubeconfig configured
- Docker installed and running
- Helm 3.x installed
- kubectl CLI installed
- Container registry access (Docker Hub, ECR, GCR, etc.)

## Quick Deploy

For simple deployments:

```bash
python scripts/quick-deploy.py \
  --app my-api \
  --image myregistry/my-api:v1.0.0 \
  --namespace production
```

For complete examples and production patterns, see [references/deployment-patterns.md](references/deployment-patterns.md).

## Full Deployment Workflow

See [references/deployment-workflow.md](references/deployment-workflow.md) for detailed steps.

## Configuration Reference

See [references/configuration.md](references/configuration.md) for all available options.

## Troubleshooting

Common issues and solutions in [references/troubleshooting.md](references/troubleshooting.md).
```

This example demonstrates progressive disclosure by keeping the main skill brief and linking to detailed references.

## Using These Examples

To adapt these examples for your use case:

1. **Copy the structure** that matches your complexity level
2. **Customize the frontmatter** with your skill details
3. **Replace example content** with your actual instructions
4. **Test with validation**: `skills-ref validate ./your-skill`
5. **Iterate based on agent feedback** when using the skill

## More Examples

Find community-contributed skills at:
- https://github.com/agentskills/agentskills/tree/main/skills
- https://github.com/Agentic-Insights/claude-plugins-marketplace/tree/main/plugins
