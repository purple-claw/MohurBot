# Mohur AI Chatbot

Initially an Assigment from the MOHUR Team, but turned out to be the best wholesome experience, and Finally a Visually Stunning, Personalised ChatBot Assistant.

## Features

### Core Functionality
- **AI-Powered Responses**: Integration with OpenAI GPT-3.5-turbo for intelligent conversations
- **Knowledge Base Integration**: Local knowledge base with smart matching algorithms
- **Hybrid Response System**: Combines knowledge base context with AI enhancement
- **Real-time Chat Interface**: Modern, responsive chat UI with typing indicators
- **Chat History Management**: Persistent conversation history with clear functionality
- **Response Source Tracking**: Visual indicators showing response origins (AI, KB, Hybrid)

### User Interface
- **McLaren Dark Theme**: Pure black background with signature orange accents
- **Responsive Design**: Optimized for desktop and mobile devices
- **Interactive Elements**: Smooth animations and hover effects
- **Statistics Dashboard**: Real-time conversation metrics
- **History Modal**: Dedicated chat history viewer with search capabilities

### Technical Capabilities
- **CORS Enabled**: Proper cross-origin resource sharing configuration
- **Error Handling**: Comprehensive error management and fallback systems
- **Environment Configuration**: Secure API key management
- **Performance Optimized**: Efficient data loading and state management

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.13**: Latest Python version with enhanced performance
- **OpenAI SDK**: Integration with GPT-3.5-turbo model
- **Uvicorn**: ASGI server for production deployment
- **python-dotenv**: Environment variable management

### Frontend
- **React 18**: Modern JavaScript library for building user interfaces
- **Axios**: HTTP client for API communication
- **CSS3**: Custom styling with gradient effects and animations
- **React Hooks**: State management and lifecycle handling

## Project Structure

```
Mohur_bot/
├── backend/
│   ├── main.py                 # FastAPI application and endpoints
│   ├── chatHis.py             # Chat history management
│   ├── knowledgeBase.py       # Local knowledge base operations
│   ├── llm_service.py         # OpenAI integration service
│   ├── chat_history.json     # Persistent chat storage
│   └── .env                   # Environment variables
├── frontend/
│   ├── public/
│   │   ├── index.html         # Main HTML template
│   │   └── ...                # Static assets
│   ├── src/
│   │   ├── App.js             # Main application component
│   │   ├── App.css            # Global styles and theme
│   │   ├── ChatInterface.js   # Main chat interface
│   │   ├── ChatHistory.js     # History modal component
│   │   ├── ChatHistory.css    # History component styles
│   │   └── index.js           # React entry point
│   └── package.json           # Frontend dependencies
└── README.md                  # Project documentation
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager
- OpenAI API key

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install fastapi uvicorn openai python-dotenv
   ```

4. **Configure environment variables**
   Create a `.env` file in the backend directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Start the backend server**
   ```bash
   python main.py
   ```
   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```
   The application will open at `http://localhost:3000`

## Deployment

### Quick Start with Deployment Script

We've included a comprehensive deployment script that streamlines the entire process:

```bash
# Make script executable (first time only)
chmod +x deploy.sh

# Setup environment files
./deploy.sh setup

# Choose your deployment method:
./deploy.sh local      # Run locally
./deploy.sh docker-run # Run with Docker
./deploy.sh vercel     # Deploy to Vercel
```

### Deployment Options

#### 1. Local Development
```bash
./deploy.sh install    # Install dependencies
./deploy.sh local      # Start both servers
```

#### 2. Docker Deployment
```bash
./deploy.sh docker-build  # Build images
./deploy.sh docker-run    # Start with compose
./deploy.sh docker-stop   # Stop services
```

#### 3. Vercel Deployment (Recommended for Production)

**Prerequisites:**
- Vercel account (free tier available)
- Vercel CLI installed globally

**Steps:**
1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Setup environment variables**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Add `OPENAI_API_KEY` in your project settings
   - Set the value to your OpenAI API key

3. **Deploy**
   ```bash
   ./deploy.sh vercel
   ```

**Manual Vercel Deployment:**
```bash
# Login to Vercel
vercel login

# Deploy
vercel --prod

# Follow the prompts to configure your project
```

### Docker Configuration

The project includes optimized Docker configurations:

- **Multi-stage builds** for production optimization
- **Security hardening** with non-root users
- **Health checks** for reliability
- **Nginx optimization** for frontend
- **Environment variable support**

**Docker Compose Services:**
- **Backend**: FastAPI on port 8000
- **Frontend**: React with Nginx on port 3000
- **Volumes**: Persistent data storage
- **Networks**: Isolated container communication

### Environment Variables

**Required:**
- `OPENAI_API_KEY`: Your OpenAI API key

**Optional:**
- `LOG_LEVEL`: Logging level (default: INFO)
- `MAX_HISTORY_ENTRIES`: Chat history limit (default: 10)

### Vercel Configuration

The `vercel.json` file includes:
- **Serverless functions** for the backend API
- **Static hosting** for the React frontend
- **Route handling** for SPA routing
- **Environment variable management**
- **Function timeout configuration**

### Production Considerations

**Performance:**
- Frontend assets are cached and compressed
- Backend uses efficient FastAPI with async support
- Database operations are optimized for chat history

**Security:**
- CORS properly configured
- Environment variables for sensitive data
- Non-root Docker containers
- Security headers in Nginx

**Monitoring:**
- Health check endpoints
- Comprehensive logging
- Error handling and fallbacks

## API Documentation

### Endpoints

#### Chat Operations
- **POST /ask** - Send a question and receive AI-powered response
- **GET /history** - Retrieve chat conversation history
- **DELETE /history** - Clear all chat history

#### System Operations
- **GET /health** - Check API health status
- **GET /stats** - Get conversation statistics
- **GET /test-cors** - Verify CORS configuration
- **POST /enhance** - Enhance text using AI

### Request/Response Examples

#### Send Question
```bash
curl -X POST "http://localhost:5000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "How can I improve my productivity?"}'
```

Response:
```json
{
  "question": "How can I improve my productivity?",
  "answer": "To boost productivity, try time-blocking your schedule...",
  "status": "success",
  "source": "llm_with_kb"
}
```

#### Get Statistics
```bash
curl "http://localhost:5000/stats"
```

Response:
```json
{
  "total_conversations": 15,
  "llm_enhanced_responses": 12,
  "knowledge_base_responses": 3,
  "status": "success"
}
```

## Configuration

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Required
OPENAI_API_KEY=sk-your-openai-api-key

# Optional
LOG_LEVEL=INFO
MAX_HISTORY_ENTRIES=10
```

### Customization Options

#### Knowledge Base
Edit `backend/knowledgeBase.py` to add domain-specific knowledge:

```python
knowledge_base = [
    {
        "question": "your custom question",
        "answer": "your expert answer",
        "keywords": ["relevant", "keywords", "list"]
    }
]
```

#### Theme Customization
Modify `frontend/src/App.css` to customize the McLaren theme:

```css
:root {
  --primary-orange: #FF8000;
  --secondary-orange: #FF6600;
  --accent-orange: #FFB366;
  --pure-black: #000000;
}
```

## Usage Guide

### Basic Operation

1. **Start Conversation**: Type your question in the input field
2. **Send Message**: Click the "Send" button or press Enter
3. **View Responses**: AI-generated responses appear with source badges
4. **Check History**: Click "History" button to view past conversations
5. **View Statistics**: Click "Stats" button for conversation metrics

### Advanced Features

#### Response Sources
- **AI+KB**: AI-enhanced response using knowledge base context
- **AI**: Pure AI-generated response
- **KB**: Knowledge base only response
- **ERR**: Error fallback response

#### History Management
- **Refresh**: Reload conversation history
- **Clear All**: Remove all chat history (requires confirmation)
- **Use Question**: Copy previous question to input field
- **View Full**: See complete conversation details

## Development

### Code Style
- Follow PEP 8 for Python code
- Use ES6+ features for JavaScript
- Maintain consistent indentation (2 spaces for JS, 4 for Python)
- Add comments for complex logic

### Testing
Test the application by running both servers and accessing:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:5000/docs` (FastAPI auto-documentation)

### Building for Production

#### Backend Deployment
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

#### Frontend Build
```bash
npm run build
```

## Troubleshooting

### Common Issues

#### CORS Errors
Ensure the backend CORS middleware includes your frontend URL:
```python
allow_origins=["http://localhost:3000"]
```

#### API Key Issues
Verify your OpenAI API key is correctly set in the `.env` file and has sufficient credits.

#### Port Conflicts
If ports 3000 or 5000 are in use, modify the startup commands:
- Frontend: `PORT=3001 npm start`
- Backend: Modify `uvicorn.run(app, host="0.0.0.0", port=5001)` in `main.py`

#### Installation Problems
Clear npm cache and reinstall:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- OpenAI for providing the GPT-3.5-turbo model
- FastAPI team for the excellent web framework
- React team for the frontend library
- McLaren for the inspiring color scheme


---

**Built with Love by Nitin Sri**