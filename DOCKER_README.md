# Docker Setup for Housing Market Analysis

This guide explains how to run the Flask application using Docker. The Docker container automatically executes all Jupyter notebooks to generate data, results, and visualizations before starting the Flask server.

## 🐳 Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed (usually comes with Docker Desktop)

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start the container
docker compose up --build

# Or run in detached mode (background)
docker compose up -d --build

# Stop the container
docker compose down
```

**⏱️ First run takes 3-5 minutes** as it executes all notebooks:

1. `01_data_cleaning.ipynb` - Processes raw SURS data
2. `02_bootstrap_analysis.ipynb` - Generates bootstrap results
3. `03_montecarlo_simulation.ipynb` - Runs Monte Carlo simulations
4. `04_ml_prediction.ipynb` - Trains ML models and creates forecasts

After notebooks complete, the Flask application will be available at: <http://localhost:5000>

### Option 2: Using Docker directly

```bash
# Build the Docker image
docker build -t housing-market-analysis .

# Run the container
docker run -p 5000:5000 --name housing-market-app housing-market-analysis

# Stop the container
docker stop housing-market-app
docker rm housing-market-app
```

## 📋 Docker Commands Reference

### Build Commands

```bash
# Build the image
docker-compose build

# Rebuild without cache (for clean build)
docker-compose build --no-cache
```

### Run Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Start with rebuild
docker-compose up --build
```

### Stop Commands

```bash
# Stop running services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v
```

### Monitoring Commands

```bash
# View logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs flask-app

# Check running containers
docker-compose ps

# Check container health
docker ps
```

### Debugging Commands

```bash
# Access container shell
docker-compose exec flask-app /bin/bash

# Run Python commands inside container
docker-compose exec flask-app python -c "import pandas; print(pandas.__version__)"

# View container resource usage
docker stats
```

## 📁 Project Structure in Docker

```
/app/                       # Working directory in container
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── templates/              # Jinja2 templates
│   ├── base.html
│   └── index.html
└── src/
    ├── figures/            # Generated visualizations
    │   ├── bootstrap/
    │   ├── montecarlo/
    │   ├── ml_prediction/
    │   └── original_data/
    ├── results/            # Analysis results (CSV)
    │   ├── bootstrap/
    │   ├── montecarlo/
    │   └── ml_prediction/
    └── helpers/
        └── data_processing.py
```

## 🔧 Configuration

### Environment Variables

You can modify environment variables in `docker-compose.yml`:

```yaml
environment:
  - FLASK_DEBUG=0          # Set to 1 for debug mode
  - PYTHONUNBUFFERED=1     # Force Python output to stdout
```

### Ports

Default port mapping: `5000:5000` (host:container)

To change the host port (e.g., to 8080):

```yaml
ports:
  - "8080:5000"
```

Then access at: http://localhost:8080

### Volumes

Current volume mounts in `docker-compose.yml`:

- `./src/figures:/app/src/figures:ro` - Read-only access to figures
- `./src/results:/app/src/results:ro` - Read-only access to results
- `./templates:/app/templates` - Live updates to templates (development)

**For production:** Remove template volumes to use baked-in files.

## 🏗 Building for Different Environments

### Development Mode

Includes live code reloading:

```yaml
# In docker-compose.yml
environment:
  - FLASK_DEBUG=1
volumes:
  - ./app.py:/app/app.py
  - ./templates:/app/templates
```

### Production Mode

Optimized for deployment:

```yaml
# In docker-compose.yml
environment:
  - FLASK_DEBUG=0
# Remove volumes (uses baked-in files from image)
```

Build production image:

```bash
docker build -t housing-market-analysis:production .
docker run -p 5000:5000 housing-market-analysis:production
```

## 🐛 Troubleshooting

### Port Already in Use

**Error:** `Bind for 0.0.0.0:5000 failed: port is already allocated`

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process or change Docker port
docker-compose down
# Edit docker-compose.yml to use different port (e.g., 5001:5000)
docker-compose up
```

### Container Exits Immediately

**Check logs:**
```bash
docker-compose logs flask-app
```

**Common causes:**
- Missing `src/figures` or `src/results` directories
- Python dependency errors
- Port conflicts

### Permission Issues

**Error:** Permission denied accessing files

**Solution:**
```bash
# Fix file permissions on host
chmod -R 755 src/

# Or run container as root
docker-compose exec -u root flask-app /bin/bash
```

### Image Build Fails

**Clear Docker cache and rebuild:**
```bash
docker-compose down
docker system prune -a
docker-compose build --no-cache
```

## 📊 Health Check

The container includes a health check that pings the Flask app every 30 seconds:

```bash
# Check health status
docker inspect housing-market-analysis | grep -A 10 Health

# View health check logs
docker inspect --format='{{json .State.Health}}' housing-market-analysis
```

## 🚢 Deployment

### Docker Hub

```bash
# Tag the image
docker tag housing-market-analysis:latest yourusername/housing-market-analysis:v1.0

# Push to Docker Hub
docker login
docker push yourusername/housing-market-analysis:v1.0

# Pull and run on another machine
docker pull yourusername/housing-market-analysis:v1.0
docker run -p 5000:5000 yourusername/housing-market-analysis:v1.0
```

### Cloud Platforms

**AWS (ECS/Fargate):**
```bash
# Install AWS CLI and configure
aws ecr create-repository --repository-name housing-market-analysis
docker tag housing-market-analysis:latest [AWS_ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com/housing-market-analysis
docker push [AWS_ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com/housing-market-analysis
```

**Google Cloud Run:**
```bash
gcloud builds submit --tag gcr.io/[PROJECT-ID]/housing-market-analysis
gcloud run deploy --image gcr.io/[PROJECT-ID]/housing-market-analysis --platform managed
```

**Heroku:**
```bash
heroku container:login
heroku create your-app-name
heroku container:push web -a your-app-name
heroku container:release web -a your-app-name
```

## 🔒 Security Best Practices

1. **Don't run as root in production:**
   ```dockerfile
   # Add to Dockerfile
   RUN useradd -m -u 1000 appuser
   USER appuser
   ```

2. **Use specific Python version:**
   ```dockerfile
   FROM python:3.12.1-slim  # Instead of :3.12-slim
   ```

3. **Scan for vulnerabilities:**
   ```bash
   docker scan housing-market-analysis
   ```

4. **Use multi-stage builds** (for smaller images):
   ```dockerfile
   # Build stage
   FROM python:3.12-slim AS builder
   # ... install dependencies
   
   # Runtime stage
   FROM python:3.12-slim
   COPY --from=builder /app /app
   ```

## 📈 Performance Optimization

### Reduce Image Size

Current image size: ~400MB

**Optimize:**
```dockerfile
# Use Alpine Linux (smaller base)
FROM python:3.12-alpine

# Or use distroless
FROM gcr.io/distroless/python3
```

### Multi-stage Build Example

```dockerfile
# Stage 1: Build
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

## ✅ Verification Checklist

After running Docker:

- [ ] Container starts without errors: `docker-compose logs`
- [ ] Health check passes: `docker ps` (shows "healthy")
- [ ] Flask app accessible: Open http://localhost:5000
- [ ] All 4 sections load (Original Data, Bootstrap, Monte Carlo, ML)
- [ ] Images display correctly
- [ ] Tables render properly
- [ ] No console errors in browser

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Flask in Docker Best Practices](https://flask.palletsprojects.com/en/2.3.x/deploying/docker/)
- [Python Docker Best Practices](https://pythonspeed.com/docker/)

---

**Need help?** Check the main `README.md` or open an issue on GitHub.
