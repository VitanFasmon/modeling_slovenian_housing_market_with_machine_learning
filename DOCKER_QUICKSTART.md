# Docker Setup - Quick Reference

## ✅ Files Created

1. **Dockerfile** - Image definition with Python 3.12, dependencies, and Flask app
2. **docker-compose.yml** - Multi-container orchestration with health checks
3. **.dockerignore** - Excludes unnecessary files from Docker image
4. **DOCKER_README.md** - Complete Docker documentation (8000+ words)
5. **README.md** - Updated main README with Docker quick start

## 🚀 How to Use Docker

### Quick Start (3 commands)

```bash
# Make sure you're in the project directory
cd /home/user/Documents/AlmaMater/2.\ stopnja/1.\ letnik/Temelji\ racunalniskih\ znanj/projects/final_project

# Build and start (first run takes 3-5 minutes to execute notebooks)
docker compose up --build

# Open browser
# http://localhost:5000
```

**⏱️ What happens during startup:**

1. Container builds (installs Python + dependencies)
2. Executes all 4 Jupyter notebooks sequentially:
   - `01_data_cleaning.ipynb` - Processes raw data
   - `02_bootstrap_analysis.ipynb` - Bootstrap analysis
   - `03_montecarlo_simulation.ipynb` - Monte Carlo simulations
   - `04_ml_prediction.ipynb` - ML models & forecasts
3. Starts Flask server on port 5000

After notebooks complete, the application is ready!

### Stop the Container

```bash
# Stop with Ctrl+C or:
docker-compose down
```

## 📦 What's Inside the Docker Image?

- **Base:** Python 3.12-slim (Debian-based)
- **Size:** ~400MB (optimized)
- **Contents:**
  - Flask application (app.py)
  - All Python dependencies (pandas, scikit-learn, etc.)
  - Templates (HTML files)
  - Figures and results (from notebooks)
  - Helper modules

## 🔍 Advantages of Docker

### For You (Development)
✅ **No dependency conflicts** - Everything runs in isolated container  
✅ **Consistent environment** - Same setup on any machine  
✅ **Easy to reset** - `docker-compose down` and start fresh  
✅ **No Python version issues** - Container has Python 3.12  

### For Others (Sharing)
✅ **One-command deployment** - `docker-compose up`  
✅ **No installation needed** - Only Docker required  
✅ **Works everywhere** - Linux, Mac, Windows  
✅ **Reproducible** - Same results on every machine  

### For Production
✅ **Scalable** - Can run multiple containers  
✅ **Portable** - Deploy to any cloud (AWS, GCP, Azure)  
✅ **Reliable** - Health checks ensure app is running  
✅ **Secure** - Isolated from host system  

## 🛠 Common Commands

### Build and Run

```bash
# Build only
docker-compose build

# Run in background (detached mode)
docker-compose up -d

# Build and run
docker-compose up --build

# Build without cache (clean build)
docker-compose build --no-cache
```

### Monitor

```bash
# View logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# Check status
docker-compose ps

# Check resource usage
docker stats
```

### Debug

```bash
# Access container shell
docker-compose exec flask-app /bin/bash

# Run Python in container
docker-compose exec flask-app python -c "print('Hello from Docker!')"

# Check environment
docker-compose exec flask-app env
```

### Clean Up

```bash
# Stop containers
docker-compose down

# Remove containers and networks
docker-compose down --volumes

# Remove all Docker images (careful!)
docker system prune -a
```

## 📊 Docker vs Local Comparison

| Feature | Docker | Local Install |
|---------|--------|---------------|
| Setup time | 2 minutes | 10+ minutes |
| Dependencies | Automatic | Manual pip install |
| Python version | Fixed (3.12) | Your system version |
| Isolation | Full | None |
| Portability | High | Low |
| Learning curve | Medium | Low |
| Production-ready | ✅ Yes | ❌ No |

## 🔧 Configuration

### Change Port

Edit `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Change 5000 to any port
```

Then restart:
```bash
docker-compose down
docker-compose up
```

### Enable Debug Mode

Edit `docker-compose.yml`:

```yaml
environment:
  - FLASK_DEBUG=1  # Change 0 to 1
```

### Add Environment Variables

```yaml
environment:
  - FLASK_DEBUG=0
  - MY_VARIABLE=value
  - DATABASE_URL=postgresql://...
```

## 🌐 Deployment Options

### 1. Local Network (current setup)
```bash
docker-compose up -d
# Accessible at: http://localhost:5000
```

### 2. Cloud (AWS, GCP, Azure)
```bash
# Push to Docker Hub
docker tag housing-market-analysis yourusername/housing-market-analysis
docker push yourusername/housing-market-analysis

# Deploy on cloud
# AWS ECS, Google Cloud Run, Azure Container Instances
```

### 3. Heroku
```bash
heroku container:login
heroku create your-app-name
heroku container:push web
heroku container:release web
```

## ✅ Verification Checklist

After running `docker-compose up`:

- [ ] Container starts without errors
- [ ] Logs show "Running on http://0.0.0.0:5000"
- [ ] Browser opens http://localhost:5000
- [ ] Dashboard loads with 4 sections
- [ ] All images display correctly
- [ ] Tables render properly
- [ ] No console errors

## 📚 Learn More

- **Full Docker Guide:** See [DOCKER_README.md](DOCKER_README.md)
- **Project Setup:** See [README.md](README.md)
- **Flask App:** See [app.py](app.py)

## ❓ Troubleshooting

### Port already in use

```bash
# Find process on port 5000
lsof -i :5000

# Kill it or change Docker port
docker-compose down
# Edit docker-compose.yml: "5001:5000"
docker-compose up
```

### Container exits immediately

```bash
# Check logs
docker-compose logs flask-app

# Common issues:
# - Missing src/figures or src/results directories
# - Port conflict
# - Python dependency errors
```

### Permission denied

```bash
# Fix file permissions
chmod -R 755 src/

# Or run as root
docker-compose exec -u root flask-app /bin/bash
```

## 🎓 Next Steps

1. **Learn Docker basics:** https://docs.docker.com/get-started/
2. **Explore Docker Compose:** https://docs.docker.com/compose/
3. **Deploy to cloud:** AWS, GCP, or Azure tutorials
4. **Add CI/CD:** GitHub Actions + Docker Hub automated builds

---

**Created:** November 2025  
**Docker Version:** 24.0+  
**Docker Compose Version:** 2.0+
