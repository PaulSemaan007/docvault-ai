# DocVault AI

> Intelligent Document Management System with AI-Powered Processing

[![Built for Laserfiche](https://img.shields.io/badge/Built%20for-Laserfiche%20Internship-blue)](https://www.laserfiche.com)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Overview

DocVault AI is a full-stack document management system that demonstrates enterprise-grade document processing capabilities using modern AI/ML technologies. Built as a portfolio project for the Laserfiche Software Engineer Internship application.

### Key Features

- **AI-Powered Document Classification** - Automatically categorize documents (invoices, contracts, reports) using zero-shot ML classification
- **Smart Entity Extraction** - Extract names, dates, amounts, and organizations using NLP
- **OCR Processing** - Extract text from scanned documents and images
- **Workflow Automation** - Create rules to auto-tag, route, and process documents
- **Full-Text Search** - Search across all document content with powerful filters
- **Role-Based Access Control** - Admin, Manager, and User roles with audit logging
- **Enterprise Security** - JWT authentication, audit trails, and secure storage

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│                   (Next.js on Vercel)                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │
│  │Dashboard│  │ Upload  │  │ Search  │  │ Workflow Builder│ │
│  └─────────┘  └─────────┘  └─────────┘  └─────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API
┌──────────────────────────▼──────────────────────────────────┐
│                        BACKEND                               │
│                 (Python FastAPI on Railway)                  │
│  ┌──────────────┐  ┌─────────────┐  ┌────────────────────┐  │
│  │ Auth/Security│  │ ML Pipeline │  │ Workflow Engine    │  │
│  │ - JWT        │  │ - Tesseract │  │ - Rule evaluation  │  │
│  │ - RBAC       │  │ - HuggingFace│ │ - Auto-routing     │  │
│  │ - Audit logs │  │ - spaCy     │  │ - Notifications    │  │
│  └──────────────┘  └─────────────┘  └────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                       DATA LAYER                             │
│  ┌─────────────────┐          ┌────────────────────────┐    │
│  │ PostgreSQL      │          │ Supabase Storage       │    │
│  │ (Supabase)      │          │ (Document Files)       │    │
│  └─────────────────┘          └────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | Next.js 14 + TypeScript | React framework with App Router |
| Styling | Tailwind CSS | Utility-first CSS |
| Backend | Python 3.11 + FastAPI | High-performance async API |
| ML Classification | Hugging Face Transformers | Zero-shot document classification |
| NLP | spaCy | Named entity recognition |
| OCR | Tesseract | Text extraction from images/PDFs |
| Database | PostgreSQL (Supabase) | Document metadata storage |
| File Storage | Supabase Storage | Secure document storage |
| Authentication | JWT + Supabase Auth | Secure token-based auth |
| Frontend Hosting | Vercel | Serverless deployment |
| Backend Hosting | Railway | Container deployment |

## Project Structure

```
docvault-ai/
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/              # App router pages
│   │   │   ├── page.tsx      # Landing page
│   │   │   ├── login/        # Authentication
│   │   │   ├── register/
│   │   │   └── dashboard/    # Main app
│   │   │       ├── page.tsx  # Dashboard home
│   │   │       ├── documents/
│   │   │       ├── upload/
│   │   │       ├── search/
│   │   │       └── workflows/
│   │   ├── components/       # Reusable components
│   │   └── lib/              # Utilities
│   └── package.json
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── main.py           # Application entry
│   │   ├── config.py         # Settings management
│   │   ├── api/              # REST endpoints
│   │   │   ├── auth.py
│   │   │   ├── documents.py
│   │   │   ├── search.py
│   │   │   ├── workflows.py
│   │   │   └── admin.py
│   │   ├── ml/               # ML pipeline
│   │   │   ├── classifier.py # Document classification
│   │   │   ├── ner.py        # Entity extraction
│   │   │   ├── ocr.py        # Text extraction
│   │   │   └── pipeline.py   # Processing orchestration
│   │   ├── security/         # Auth & audit
│   │   │   ├── jwt.py
│   │   │   └── audit.py
│   │   └── services/         # Business logic
│   ├── requirements.txt
│   └── Dockerfile
│
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/docvault-ai.git
   cd docvault-ai
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv

   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate

   pip install -r requirements.txt
   python -m spacy download en_core_web_sm

   # Create .env file
   cp .env.example .env

   # Start the server
   uvicorn app.main:app --reload
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install

   # Create .env.local
   cp .env.example .env.local

   # Start the dev server
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create new account |
| POST | `/api/auth/login` | Authenticate user |
| GET | `/api/auth/me` | Get current user |

### Documents
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/documents/upload` | Upload and process document |
| GET | `/api/documents` | List all documents |
| GET | `/api/documents/{id}` | Get document details |
| DELETE | `/api/documents/{id}` | Delete document |

### Search
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/search?q=query` | Full-text search |
| GET | `/api/search/filters` | Get filter options |

### Workflows
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/workflows` | Create workflow rule |
| GET | `/api/workflows` | List all workflows |
| PUT | `/api/workflows/{id}` | Update workflow |
| DELETE | `/api/workflows/{id}` | Delete workflow |

## ML Pipeline

### Document Classification
Uses Hugging Face's zero-shot classification to categorize documents:
- **Invoice** - Bills, payment requests
- **Contract** - Agreements, terms
- **Report** - Analysis, summaries
- **Letter** - Correspondence
- **Form** - Applications, questionnaires

### Entity Extraction
Extracts key information using spaCy NER:
- **PERSON** - Names of individuals
- **ORGANIZATION** - Company names
- **DATE** - Dates and times
- **MONEY** - Financial amounts
- **EMAIL** - Email addresses
- **PHONE** - Phone numbers

## Deployment

### Deploy Frontend to Vercel
1. Push code to GitHub
2. Import repository in Vercel
3. Set environment variables
4. Deploy

### Deploy Backend to Railway
1. Connect GitHub repository
2. Add environment variables
3. Deploy with Dockerfile

## Skills Demonstrated

This project showcases competencies aligned with Laserfiche's requirements:

| Requirement | Implementation |
|-------------|----------------|
| Cloud-based systems | Vercel + Railway + Supabase architecture |
| Clean, documented code | TypeScript strict mode, Python type hints, docstrings |
| Machine Learning | Document classification, NER, OCR integration |
| Cybersecurity | RBAC, JWT auth, audit logging, input validation |
| Problem-solving | Full-stack architecture, ML pipeline design |
| Programming skills | Python, TypeScript, SQL |

## Future Enhancements

- [ ] Real-time collaboration on documents
- [ ] Advanced workflow conditions (AND/OR logic)
- [ ] Document versioning and history
- [ ] Integration with external storage (Google Drive, OneDrive)
- [ ] Custom ML model training on user data
- [ ] Batch document processing
- [ ] Mobile-responsive improvements

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

Built for the Laserfiche Software Engineer Internship application.

---

*This project demonstrates enterprise document management concepts inspired by Laserfiche's mission to make enterprise information more accessible and secure.*
