# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Skill Manager is a local web application for managing Claude Code skills with a visual interface. It features:
- **Frontend**: Vue.js 3 with Vite build tool (port 8529)
- **Backend**: Python Flask API server (port 9529)
- **Data Storage**: JSON file-based storage

## Architecture

```
skill_manager/
├── backend/
│   ├── app.py           # Flask API server
│   ├── requirements.txt
│   └── skills/
│       └── skills.json  # Skill data storage
└── frontend/
    ├── index.html
    ├── vite.config.js    # Vite + API proxy config
    ├── package.json
    └── src/
        ├── main.js
        ├── App.vue       # Main component with form & import
        ├── assets/main.css
        └── components/SkillList.vue
```

## Commands

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py        # Starts server on http://localhost:9529
```

### Frontend
```bash
cd frontend
npm install
npm run dev          # Starts dev server on http://localhost:8529
npm run build        # Production build
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/skills | List all skills |
| POST | /api/skills | Create new skill |
| GET | /api/skills/:id | Get single skill |
| PUT | /api/skills/:id | Update skill |
| DELETE | /api/skills/:id | Delete skill |
| POST | /api/import | Import skills from directory |

## Import Feature

POST `/api/import` with `{ "source_dir": "/path/to/skills" }`

Scans directory for subdirectories containing CLAUDE.md, imports as skills.

## Skill Data Model

```json
{
  "id": 1,
  "name": "skill-name",
  "description": "Description text",
  "category": "development|testing|design|general|imported",
  "enabled": true|false,
  "source_path": "/path/to/skill"  // for imported skills
}
```