# Mohur AI Chatbot - Complete Deployment Guide

## What's Been Created

### 🐳 Docker Configuration
- **Dockerfile**: Multi-stage production build for backend
- **frontend/Dockerfile**: Optimized React build with Nginx
- **docker-compose.yml**: Complete orchestration for local development
- **nginx.conf**: Production-ready Nginx configuration
- **.dockerignore**: Optimized build context

### ☁️ Vercel Configuration
- **vercel.json**: Complete Vercel deployment configuration
- **backend/requirements.txt**: Python dependencies for serverless functions
- **.vercelignore**: Optimized deployment files
- **GitHub Actions**: Automated CI/CD pipeline

### 🚀 Deployment Script
- **deploy.sh**: One-command deployment for all platforms
- Supports: Local, Docker, and Vercel deployments
- Automatic environment setup and dependency management

### 🔧 Configuration Files
- **.env templates**: Secure environment variable management
- **.gitignore**: Complete git ignore patterns
- **Updated package.json**: Vercel-compatible build scripts

## Quick Start Commands

```bash
# 1. Setup (First time only)
./deploy.sh setup
# Edit .env files with your OpenAI API key

# 2. Choose deployment method:

# Local Development
./deploy.sh install && ./deploy.sh local

# Docker (Recommended for local production testing)
./deploy.sh docker-run

# Vercel (Production deployment)
npm install -g vercel
./deploy.sh vercel
```

## Deployment Options Comparison

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Local** | Development | Fast iteration, easy debugging | Manual setup, not scalable |
| **Docker** | Local Production | Consistent environment, easy scaling | Requires Docker knowledge |
| **Vercel** | Production | Auto-scaling, global CDN, free tier | Limited to Vercel ecosystem |

## Architecture Overview

```
Frontend (React) → Vercel Edge Network → Backend (FastAPI) → OpenAI API
                ↘                    ↗
                  Docker Container
```

### Frontend Deployment
- **Vercel**: Static React build served via global CDN
- **Docker**: Nginx-served optimized build
- **Local**: React development server

### Backend Deployment
- **Vercel**: Serverless functions (auto-scaling)
- **Docker**: Containerized FastAPI with health checks
- **Local**: Python uvicorn development server

## Environment Variables

### Required
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Optional
```env
LOG_LEVEL=INFO
MAX_HISTORY_ENTRIES=10
```

## Vercel Setup Details

### 1. Prerequisites
- Vercel account (free tier available)
- GitHub repository (optional but recommended)
- OpenAI API key

### 2. Environment Configuration
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Import your project from GitHub or upload manually
3. Add environment variable: `OPENAI_API_KEY`
4. Deploy automatically

### 3. Custom Domains (Optional)
- Add custom domain in Vercel dashboard
- Configure DNS settings
- SSL automatically handled

## Docker Production Setup

### 1. Build and Run
```bash
# Build images
./deploy.sh docker-build

# Start services
./deploy.sh docker-run
```

### 2. Production Considerations
- Uses multi-stage builds for smaller images
- Non-root user for security
- Health checks for reliability
- Persistent volumes for data

### 3. Scaling
```bash
# Scale backend
docker-compose up --scale backend=3

# Load balancer setup (nginx)
# See nginx.conf for configuration
```

## Monitoring and Maintenance

### Health Checks
- **Local**: `http://localhost:5000/health`
- **Docker**: `http://localhost:8000/health`
- **Vercel**: `https://your-app.vercel.app/api/health`

### Logs
```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Vercel logs
vercel logs your-deployment-url
```

### Updates
```bash
# Update dependencies
./deploy.sh install

# Rebuild and deploy
./deploy.sh docker-run
./deploy.sh vercel
```

## Security Considerations

### Production Checklist
- ✅ Environment variables properly configured
- ✅ CORS restricted to your domain
- ✅ HTTPS enabled (automatic with Vercel)
- ✅ Non-root Docker containers
- ✅ Security headers in Nginx
- ✅ API key stored securely

### Best Practices
1. **Never commit API keys** to version control
2. **Use HTTPS** in production (automatic with Vercel)
3. **Regular updates** of dependencies
4. **Monitor usage** and costs
5. **Backup chat history** if using Docker

## Troubleshooting

### Common Issues

#### Environment Variables Not Loading
```bash
# Check if .env file exists
ls -la .env

# Verify format (no spaces around =)
OPENAI_API_KEY=sk-your-key-here
```

#### CORS Errors
- Ensure backend allows your frontend domain
- Check Vercel function routes in `vercel.json`

#### Docker Build Failures
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

#### Vercel Deployment Issues
```bash
# Clear Vercel cache
vercel --force

# Check function logs
vercel logs
```

## Performance Optimization

### Frontend
- Static assets cached by CDN (Vercel)
- Gzip compression enabled (Nginx/Vercel)
- Optimized React build

### Backend
- Async FastAPI for concurrent requests
- Efficient JSON storage for chat history
- Connection pooling for OpenAI API

## Cost Estimation

### Vercel (Free Tier Limits)
- **Bandwidth**: 100GB/month
- **Function Executions**: 100,000/month
- **Build Time**: 6,000 minutes/month

### OpenAI API
- **GPT-3.5-turbo**: ~$0.002 per 1K tokens
- **Average chat**: ~$0.001-0.01 per interaction

### Docker (Self-hosted)
- **VPS**: $5-20/month depending on provider
- **Bandwidth**: Usually unlimited
- **Compute**: Based on VPS specifications

## Next Steps

1. **Deploy to Vercel** for production use
2. **Set up monitoring** with Vercel Analytics
3. **Configure custom domain** if needed
4. **Add authentication** for private use
5. **Implement rate limiting** for public use
6. **Set up automated backups** for chat history

## Support

For issues or questions:
1. Check this deployment guide
2. Review the main README.md
3. Check Vercel documentation
4. Review Docker Compose logs
5. Open an issue in the repository

---

**🎉 Your Mohur AI Chatbot is now ready for production deployment!**