#!/bin/bash

# Mohur AI Chatbot Deployment Script
# This script streamlines the deployment process for both Docker and Vercel

set -e

echo "MohurBot Deployment Script"
echo "======================================"
command_exists() {
    command -v "$1" >/dev/null 2>&1
}
deploy_vercel() {
    echo "Deploying to Vercel..."
    
    if ! command_exists vercel; then
        echo "Vercel CLI not found. Installing..."
        npm install -g vercel
    fi
    
    echo "Setting up environment variables..."
    echo "Please make sure you have set your OPENAI_API_KEY in Vercel dashboard"
    echo "Visit: https://vercel.com/dashboard and add your environment variable"
    
    echo "Deploying to Vercel..."
    vercel --prod
    
    echo "Deployment complete!"
    echo "Your app should be available at the provided Vercel URL"
}

# Function to build Docker images
build_docker() {
    echo "Building Docker images..."
    
    if ! command_exists docker; then
        echo "Docker not found. Please install Docker first."
        exit 1
    fi
    
    echo "Building backend image..."
    docker build -t mohur-bot-backend .
    
    echo "Building frontend image..."
    docker build -t mohur-bot-frontend ./frontend
    
    echo "Docker images built successfully!"
}

# Function to run with Docker Compose
run_docker_compose() {
    echo "Starting application with Docker Compose..."
    
    if ! command_exists docker-compose; then
        echo "Docker Compose not found. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        echo "No .env file found. Creating template..."
        cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EOF
        echo "Please edit .env file with your OpenAI API key"
        return 1
    fi
    
    docker-compose up --build -d
    
    echo "Application started!"
    echo "Frontend: http://localhost:3000"
    echo "Backend API: http://localhost:8000"
    echo "API Docs: http://localhost:8000/docs"
}

# Function to stop Docker Compose
stop_docker_compose() {
    echo "Stopping Docker Compose services..."
    docker-compose down
    echo "Services stopped!"
}

# Function to install dependencies locally
install_deps() {
    echo "Installing dependencies..."
    
    # Backend dependencies
    echo "Installing backend dependencies..."
    cd backend
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    
    # Frontend dependencies
    echo "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
    
    echo "Dependencies installed!"
}

# Function to run locally
run_local() {
    echo "Starting local development servers..."
    
    # Check if .env file exists
    if [ ! -f "backend/.env" ]; then
        echo "No .env file found in backend. Creating template..."
        cat > backend/.env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EOF
        echo "Please edit backend/.env file with your OpenAI API key"
        return 1
    fi
    
    echo "Starting backend server..."
    cd backend
    source venv/bin/activate
    python main.py &
    BACKEND_PID=$!
    cd ..
    
    echo "Starting frontend server..."
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    echo "Servers started!"
    echo "Frontend: http://localhost:3000"
    echo "Backend API: http://localhost:5000"
    echo "Press Ctrl+C to stop servers"
    
    # Wait for interrupt
    trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
    wait
}

# Function to setup environment
setup_env() {
    echo "🔧 Setting up environment..."
    
    # Create backend .env file
    if [ ! -f "backend/.env" ]; then
        cat > backend/.env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EOF
        echo "Backend .env file created"
    fi
    
    # Create root .env file for Docker Compose
    if [ ! -f ".env" ]; then
        cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EOF
        echo "Root .env file created"
    fi
    
    echo "Please edit the .env files with your actual OpenAI API key"
}

# Main menu
case "${1:-}" in
    "vercel")
        deploy_vercel
        ;;
    "docker-build")
        build_docker
        ;;
    "docker-run")
        run_docker_compose
        ;;
    "docker-stop")
        stop_docker_compose
        ;;
    "install")
        install_deps
        ;;
    "local")
        run_local
        ;;
    "setup")
        setup_env
        ;;
    *)
        echo "Usage: $0 {vercel|docker-build|docker-run|docker-stop|install|local|setup}"
        echo ""
        echo "Commands:"
        echo "  setup       - Setup environment files"
        echo "  install     - Install dependencies locally"
        echo "  local       - Run application locally"
        echo "  docker-build - Build Docker images"
        echo "  docker-run  - Run with Docker Compose"
        echo "  docker-stop - Stop Docker Compose services"
        echo "  vercel      - Deploy to Vercel"
        echo ""
        echo "Examples:"
        echo "  $0 setup      # First time setup"
        echo "  $0 install    # Install dependencies"
        echo "  $0 local      # Run locally"
        echo "  $0 docker-run # Run with Docker"
        echo "  $0 vercel     # Deploy to Vercel"
        exit 1
        ;;
esac