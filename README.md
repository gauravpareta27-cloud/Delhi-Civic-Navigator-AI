# 🏛️ Delhi Civic Navigator AI

> **Get official document checklists for Delhi government services in seconds — powered by Elasticsearch + Gemini AI.**

[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.x-005571?style=flat&logo=elasticsearch)](https://www.elastic.co/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat&logo=python)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini-AI-4285F4?style=flat&logo=google)](https://ai.google.dev/)

---

## 🎯 Problem Statement

People waste hours searching multiple government websites to find:
- Required documents
- Application fees
- Processing times
- Eligibility criteria
- Official application portals

**Delhi Civic Navigator AI** solves this by providing all this information from **official Delhi government sources** with **citations** — in seconds.

---

## ✨ Features

- 🔍 **Elasticsearch-powered search** — fuzzy multi-match queries on indexed government documents
- 🤖 **Gemini AI** — structures raw data into clean, cited responses
- 🏛️ **10 government services** supported (Birth Certificate, Driving Licence, Income Certificate, and more)
- 📱 **Responsive UI** — dark mode glassmorphism design, works on all devices
- ⚡ **Zero-dependency backend** — runs on pure Python, no heavy frameworks

---

## 🏗️ Architecture

```
User (Browser)
      │
      ▼
  index.html  ──── REST API ────▶  Python HTTP Server (port 8000)
                                          │
                            ┌─────────────┴──────────────┐
                            ▼                            ▼
                   Elastic Cloud                   Gemini AI
                (delhi_services index)         (Summarization)
                            │                            │
                            └──────── Context ───────────┘
                                          │
                                  Structured Answer
                                    + Citations
```

---

## 🗂️ Project Structure

```
delhi-civic-navigator/
├── backend/
│   ├── app.py             # Python HTTP server (no FastAPI needed!)
│   ├── prompts.py         # Gemini system prompts
│   ├── requirements.txt   # Dependencies
│   └── .env               # API keys (not committed)
├── data/
│   └── government_docs/
│       └── services.json  # 5 official Delhi services dataset
├── frontend/
│   └── src/               # React source (optional, see index.html)
├── index.html             # Standalone frontend (no Node.js needed!)
├── START_SERVER.bat        # One-click server start (Windows)
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+ (tested on 3.14)
- An [Elastic Cloud](https://cloud.elastic.co/) account
- A [Gemini API key](https://ai.google.dev/)

### 1. Clone the repository
```bash
git clone https://github.com/gauravpareta27-cloud/Delhi-Civic-Navigator-AI.git
cd Delhi-Civic-Navigator-AI
```

### 2. Set up the backend
```bash
python -m venv backend/venv
# Windows:
backend\venv\Scripts\python.exe -m pip install -r backend/requirements.txt
```

### 3. Configure environment variables
Create `backend/.env`:
```env
ELASTICSEARCH_URL=https://your-cluster.es.io:443
ELASTICSEARCH_API_KEY=your-api-key-here
GEMINI_API_KEY=your-gemini-api-key
```

### 4. Index the data into Elasticsearch
```bash
backend\venv\Scripts\python.exe index_to_elastic.py
```

### 5. Start the server
```bash
# Option A: Double-click START_SERVER.bat
# Option B: Run directly:
backend\venv\Scripts\python.exe backend\app.py
```

### 6. Open the app
Open `index.html` in your browser. That's it! 🎉

---

## 📋 Supported Services

| Service | Department | Official Portal |
|---------|-----------|----------------|
| Birth Certificate | MCD | mcdonline.nic.in |
| Driving Licence | Transport Dept. | parivahan.gov.in |
| Income Certificate | Revenue Dept. | edistrict.delhigovt.nic.in |
| Property Tax | MCD | mcdonline.nic.in |
| Water Connection | Delhi Jal Board | djb.gov.in |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, Vanilla JS (Glassmorphism UI) |
| Backend | Python `http.server` (stdlib, zero deps) |
| Search | **Elasticsearch 8.x on Elastic Cloud** |
| AI | Google Gemini 1.5 Flash |
| Data | JSON (official Delhi Govt sources) |

---

## 🏆 Built For

**Hackathon — 4 Hour Sprint**  
Powered by **Elastic** (event sponsor) + **Google Gemini AI**

---

## 📜 Data Sources

All data sourced from official Delhi Government portals:
- [Delhi e-District](https://edistrict.delhigovt.nic.in)
- [MCD Online](https://mcdonline.nic.in)
- [Parivahan Sewa](https://parivahan.gov.in)
- [Delhi Jal Board](https://djb.gov.in)
