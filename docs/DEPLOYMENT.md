# Deployment Guide

## Docker Deployment (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- AWS credentials configured
- Polygon.io API key

### Quick Start
```bash
git clone https://github.com/vanhoangkha/ai-finance-assistant.git
cd ai-finance-assistant
cp .env.example .env
# Edit .env with your API keys
make docker-run
```

### Production Deployment
```bash
# Build optimized image
docker compose -f config/docker-compose.yml build --no-cache

# Run with resource limits
docker compose -f config/docker-compose.yml up -d

# Monitor logs
docker compose -f config/docker-compose.yml logs -f
```

## AWS ECS Deployment

### Task Definition
```json
{
  "family": "ai-finance-assistant",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "your-ecr-repo/ai-finance-assistant:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "AWS_DEFAULT_REGION",
          "value": "us-east-1"
        }
      ]
    }
  ]
}
```

## Kubernetes Deployment

### Deployment YAML
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-finance-assistant
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-finance-assistant
  template:
    metadata:
      labels:
        app: ai-finance-assistant
    spec:
      containers:
      - name: app
        image: ai-finance-assistant:latest
        ports:
        - containerPort: 8501
        env:
        - name: AWS_DEFAULT_REGION
          value: "us-east-1"
```

## Environment Variables

### Required
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `POLYGON_API_KEY`: Polygon.io API key

### Optional
- `AWS_DEFAULT_REGION`: AWS region (default: us-east-1)
- `STREAMLIT_SERVER_PORT`: Port (default: 8501)
- `DEBUG`: Debug mode (default: false)

## Health Checks

The application provides health check endpoint:
```
GET /_stcore/health
```

## Monitoring

### Logs
```bash
# Docker logs
docker compose logs -f

# Kubernetes logs
kubectl logs -f deployment/ai-finance-assistant
```

### Metrics
- Application startup time
- API response times
- Error rates
- Resource usage

## Scaling

### Horizontal Scaling
- Multiple container instances
- Load balancer configuration
- Session state management

### Vertical Scaling
- Increase CPU/memory limits
- Optimize data processing
- Cache frequently accessed data
