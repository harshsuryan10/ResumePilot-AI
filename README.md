AI Resume Copilot
A full-stack web application that analyzes resumes using AI to provide:
✅ ATS (Applicant Tracking System) score
📊 Resume strengths and weaknesses
💡 AI-powered improvement suggestions
🔑 Keyword analysis and recommendations
---
🏗 Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    AI Resume Copilot                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────┐      ┌──────────────────────┐     │
│  │  React + Vite        │      │  Python FastAPI      │     │
│  │  (Port 5173)         │◄────►│  (Port 8000)         │     │
│  │                      │      │                      │     │
│  │  • Login/Register    │      │  • Auth endpoints    │     │
│  │  • Resume Upload     │      │  • PDF Analysis      │     │
│  │  • Results Display   │      │  • AI Processing     │     │
│  └──────────────────────┘      └──────────────────────┘     │
│                                                               │
│                   ↕ REST API (/api/v1) ↕                    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```
---
🚀 Quick Start
Prerequisites
Node.js 18+ (`node --version`)
Python 3.9+ (`python --version`)
Installation & Run (3 Steps)
Step 1: Install All Dependencies
```bash
pnpm install
cd backend && pip install -r requirements.txt && cd ..
```
Step 2: Setup Backend Config
```bash
cd backend
cp .env.example .env
# Edit .env with your database URL, API keys, etc.
cd ..
```
Step 3: Start Both Services (Two Terminal Windows)
Terminal Window 1 - Frontend:
```bash
pnpm dev
```
🌐 Starts on: http://localhost:5173
Terminal Window 2 - Backend:
```bash
pnpm backend
```
⚙️ Starts on: http://localhost:8000
---
📝 How to Use
Register: Create a new account with email & password
Login: Sign in with your credentials
Upload Resume: Drag & drop or click to upload a PDF resume
Get Analysis: View your ATS score, suggestions, and keyword analysis
Improve: Use feedback to enhance your resume
Repeat: Upload improved resume versions to track progress
---
📂 Project Structure
```
ai-resume-copilot/
│
├── src/                          # 🎨 React Frontend
│   ├── pages/
│   │   ├── LoginPage.jsx        # Authentication
│   │   ├── RegisterPage.jsx     # User signup
│   │   └── ResumePage.jsx       # Main application
│   ├── components/
│   │   ├── FileUpload.jsx       # PDF upload handler
│   │   └── ResumeAnalysis.jsx   # Results display
│   ├── lib/
│   │   └── api.js              # API client with JWT auth
│   ├── App.jsx                 # Router & auth logic
│   ├── main.jsx                # React entry point
│   └── index.css               # Styling
│
├── backend/                      # ⚙️ Python FastAPI
│   ├── app/
│   │   ├── main.py            # FastAPI app setup
│   │   ├── routes/            # API endpoints
│   │   │   ├── auth.py       # Login/Register endpoints
│   │   │   └── resume.py     # Resume analysis endpoints
│   │   ├── models/            # Pydantic data models
│   │   ├── services/          # Business logic & AI processing
│   │   └── database/          # Database connections
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example           # Environment template
│   └── tests/                 # Unit tests
│
├── index.html                  # HTML template
├── vite.config.js             # Vite build config
├── package.json               # npm scripts
├── .env.local                 # Frontend env vars
├── SETUP.md                   # Detailed setup guide
├── QUICKSTART.md              # Quick reference
└── README.md                  # This file
```
---
🔐 Authentication Flow
```
User Registration/Login
         ↓
   [Frontend Form]
         ↓
   [Backend Validates]
         ↓
   [JWT Tokens Generated]
         ↓
   [Stored in localStorage]
         ↓
   [Auto-refresh on 401]
         ↓
   [Protected Routes Access]
```
---
📡 API Endpoints
Authentication
Method	Endpoint	Purpose
POST	`/api/v1/auth/register`	Create new account
POST	`/api/v1/auth/login`	Login user
POST	`/api/v1/auth/refresh`	Refresh access token
Resume Analysis
Method	Endpoint	Purpose
POST	`/api/v1/resume/analyze`	Analyze PDF resume
Example Request:
```bash
curl -X POST http://localhost:8000/api/v1/resume/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@resume.pdf"
```
Example Response:
```json
{
  "data": {
    "ats_score": 85,
    "strengths": ["Clear structure", "Good keywords"],
    "weaknesses": ["Missing metrics", "Vague descriptions"],
    "improvement_suggestions": ["Add quantified achievements"],
    "keywords_present": ["Python", "FastAPI"],
    "missing_keywords": ["Docker", "AWS"]
  }
}
```
---
⚙️ Environment Variables
Frontend (.env.local)
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```
Backend (backend/.env)
```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/resume_db

# JWT
JWT_SECRET=your-secret-key-here
JWT_EXPIRY=3600

# Optional: AI Service (if using external APIs)
OPENAI_API_KEY=your-key-here
```
---
🛠 Development
Frontend Development
Framework: React 18
Build Tool: Vite
Router: React Router v6
HTTP Client: Axios
Styling: Tailwind CSS
State: React hooks + Context API
Backend Development
Framework: FastAPI
Database: PostgreSQL (default)
Auth: JWT tokens
PDF Processing: PyPDF2 / pdfplumber
AI Integration: OpenAI API (configurable)
---
🐛 Troubleshooting
Frontend Issues
"Cannot GET /"
Frontend isn't running. Run `pnpm dev`
"CORS error" or "Cannot reach API"
Backend isn't running. Run `pnpm backend`
Check `VITE_API_BASE_URL` in `.env.local`
"Module not found"
Run `pnpm install`
Clear node_modules: `rm -rf node_modules && pnpm install`
Backend Issues
"ModuleNotFoundError"
Run `pip install -r requirements.txt`
Activate virtual environment if using one
"Database connection error"
Check `DATABASE_URL` in `backend/.env`
Verify database server is running
"Port 8000 already in use"
```bash
# Kill process on port 8000 (macOS/Linux)
lsof -ti:8000 | xargs kill -9

# Or use different port
python -m uvicorn app.main:app --port 8001
```
---
📦 Build for Production
Frontend:
```bash
pnpm build
# Output: dist/
```
Backend:
```bash
cd backend
gunicorn app.main:app --workers 4
```
---
🧪 Testing
Frontend Tests:
```bash
# Configure vitest if needed
npm test
```
Backend Tests:
```bash
cd backend
pytest
```
---
🤝 Contributing
Create a feature branch: `git checkout -b feature/feature-name`
Commit changes: `git commit -m "Add feature"`
Push to branch: `git push origin feature/feature-name`
Submit pull request
---
📄 License
This project is private. All rights reserved.
---
📞 Support
For issues:
Check `SETUP.md` for detailed instructions
Review `QUICKSTART.md` for common scenarios
Check backend logs for errors
Verify all environment variables are set
---
✨ Features Implemented
Frontend ✅
[x] Responsive React UI
[x] User authentication (login/register)
[x] PDF file upload
[x] Results visualization
[x] Token management
[x] Protected routes
[x] Error handling
[x] Loading states
Backend ✅
[x] JWT authentication
[x] PDF parsing & analysis
[x] ATS score calculation
[x] Keyword extraction
[x] Strengths/weaknesses analysis
[x] Improvement suggestions
[x] Error handling
[x] Database integration
---
Ready to launch! Start with `QUICKSTART.md` for fastest setup. 🚀