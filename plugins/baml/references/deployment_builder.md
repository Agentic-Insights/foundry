# Deployment Builder Module

**Version**: 1.0.0
**Purpose**: Generate deployment configurations

## Docker Configuration

```
FUNCTION generate_docker_config(language, framework):
  dockerfile = generate_dockerfile(language, framework)
  compose = generate_docker_compose(language)

  RETURN {
    "Dockerfile": dockerfile,
    "docker-compose.yml": compose,
    ".dockerignore": generate_dockerignore()
  }

FUNCTION generate_dockerfile(language, framework):
  IF language == "python":
    RETURN """
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN baml-cli generate

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

  ELSE IF language == "typescript":
    RETURN """
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npx baml-cli generate
RUN npm run build

CMD ["npm", "start"]
"""
```

## Kubernetes Configuration

```
FUNCTION generate_k8s_config(app_name):
  RETURN {
    "deployment.yaml": generate_k8s_deployment(app_name),
    "service.yaml": generate_k8s_service(app_name),
    "configmap.yaml": generate_k8s_configmap(app_name)
  }
```

## Environment Variables

```
FUNCTION generate_env_example():
  RETURN """
# BAML Application Environment Variables

# Model API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Application Config
PORT=8000
LOG_LEVEL=INFO

# Optional: Model Selection
DEFAULT_MODEL=gpt-4o-mini
"""
```

---

**Status**: Deployment configs for Docker, K8s
