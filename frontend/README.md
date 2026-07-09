# 🚀 AI-First CRM HCP Module

An AI-powered Customer Relationship Management (CRM) application designed for pharmaceutical field representatives to efficiently log and manage Healthcare Professional (HCP) interactions.

This project was developed as part of a technical assignment to demonstrate how Large Language Models (LLMs) and AI agents can simplify CRM workflows by allowing users to interact naturally through conversation while maintaining structured business records.

---

# 📌 Features

### 📝 Manual Interaction Logging
- Log HCP interactions using a structured CRM form.
- Capture meeting details, attendees, discussion topics, materials shared, sentiment, outcomes, and follow-up actions.

### 🤖 AI-Powered Interaction Logging
- Describe meetings in natural language.
- AI automatically extracts structured CRM information.
- Auto-populates the interaction form.
- Stores interaction data in PostgreSQL.

### ✏️ Edit Existing Interactions
- Update previously logged interactions using natural language.

Example:

> Update interaction 5 sentiment to Neutral.

---

### 👨‍⚕️ Retrieve HCP History

Retrieve previous interactions and HCP details before a meeting.

Example:

> Show me Dr. John Smith's interaction history.

---

### 📅 Schedule Follow-ups

Create follow-up reminders for Healthcare Professionals.

Example:

> Schedule a follow-up meeting with Dr. John Smith next Monday.

---

### ✅ Sample Compliance Check

Verify whether sample distribution limits have been exceeded.

Example:

> Check sample compliance for Dr. John Smith.

---

# 🏗️ Tech Stack

## Frontend

- React
- TypeScript
- Redux Toolkit
- Vite
- CSS
- Google Inter Font

---

## Backend

- Python
- FastAPI
- SQLAlchemy
- LangGraph
- LangChain
- Groq LLM
- PostgreSQL (Supabase)

---

## AI

- LangGraph Agent
- Groq Llama 3.3 70B Versatile
- LangChain Tool Calling

---

# 📂 Project Structure

```
AI-First-HCP-CRM
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── store
│   │   ├── api.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── backend
│   ├── main.py
│   ├── agent.py
│   ├── database.py
│   ├── schemas.py
│   ├── models.py
│   ├── requirements.txt
│   └── .env.example
│
├── README.md
└── .gitignore
```

---

# ⚙️ System Architecture

```
                React + Redux
                       │
                       │ REST API
                       ▼
                FastAPI Backend
                       │
         ┌─────────────┴─────────────┐
         │                           │
   LangGraph Agent             PostgreSQL
         │                      (Supabase)
         │
     Groq LLM
         │
  Business Tools
```

---

# 🛠️ LangGraph Tools

The AI agent uses five business tools:

| Tool | Description |
|-------|-------------|
| Log Interaction | Extracts structured interaction data from natural language and stores it in PostgreSQL |
| Edit Interaction | Updates existing interaction records |
| Get HCP History | Retrieves HCP profile and previous interaction history |
| Schedule Follow-up | Creates follow-up reminders |
| Sample Compliance Check | Checks pharmaceutical sample distribution compliance |

---

# 🚀 Getting Started

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-First-HCP-CRM.git

cd AI-First-HCP-CRM
```

---

# 💻 Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

# ⚙️ Backend Setup

Create a virtual environment

Mac/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example`

Example:

```env
DATABASE_URL=your_database_url

GROQ_API_KEY=your_groq_api_key

GROQ_MODEL=llama-3.3-70b-versatile
```

Run the backend

```bash
uvicorn main:app --reload
```

Backend runs on

```
http://127.0.0.1:8000
```

---

# 🗄️ Database

The project uses **PostgreSQL hosted on Supabase**.

Main tables:

- HCP
- Interaction
- FollowUp

SQLAlchemy ORM is used for all database operations.

---

# 🔄 AI Workflow

1. User enters interaction through chat.
2. Frontend sends request to FastAPI.
3. LangGraph determines user intent.
4. Appropriate business tool is executed.
5. LLM extracts structured CRM data.
6. Data is stored in PostgreSQL.
7. Updated information is returned to the frontend.

---

# 📸 Screenshots

Add screenshots here before submission.

Suggested screenshots:

- Home Screen
- AI Assistant
- Logged Interaction
- Interaction History
- Follow-up Creation
- Sample Compliance
- Supabase Database

---

# 📹 Demo Video

The project demonstration video includes:

- Frontend walkthrough
- Backend architecture
- AI interaction flow
- All business tools demonstration
- Database walkthrough

---

# 🎯 Assignment Objectives Covered

✅ AI-first interaction logging

✅ Structured form entry

✅ Conversational interface

✅ React + Redux frontend

✅ FastAPI backend

✅ LangGraph integration

✅ Groq LLM integration

✅ PostgreSQL database

✅ Five AI business tools

---

# 👨‍💻 Author

**Ayush Dhuliya**

B.Tech Computer Science Engineering

Full Stack Developer

GitHub: https://github.com/YOUR_USERNAME

LinkedIn: https://linkedin.com/in/YOUR_PROFILE

---

# 📄 License

This project was developed for technical evaluation purposes.