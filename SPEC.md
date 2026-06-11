# Skill Manager - Design Specification

## Overview

A local web application for managing Claude Code skills with a visual interface.

## Tech Stack

- **Frontend**: Vue.js 3 + Vite (port 8529)
- **Backend**: Python Flask (port 9529)
- **Database**: SQLite (file-mapped from skill directories)

## Architecture

```
skill_manager/
├── backend/
│   ├── app.py           # Flask REST API
│   ├── schema.sql       # SQLite schema
│   ├── skills.db        # SQLite database
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── vite.config.js   # API proxy config
    ├── package.json
    └── src/
        ├── main.js
        ├── App.vue
        ├── router/index.js
        ├── views/
        │   ├── Home.vue       # Card grid + search + category filters
        │   └── SkillDetail.vue  # File browser
        ├── components/
        │   └── SkillCard.vue
        └── assets/main.css   # Light/dark theme CSS variables
```

## Database Schema

### skills table
| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key |
| name | TEXT | Skill name (unique) |
| description | TEXT | Description |
| category | TEXT | Legacy category (default: 'general') |
| func_category | TEXT | Functional category for filtering |
| enabled | INTEGER | 1=enabled, 0=disabled |
| source_path | TEXT | Original skill directory path |
| created_at | DATETIME | Creation timestamp |

### skill_files table
| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key |
| skill_id | INTEGER | Foreign key to skills |
| filename | TEXT | File name |
| filepath | TEXT | Full file path |
| file_type | TEXT | markdown, json, python, etc. |

## Functional Categories

15 functional categories with auto-detection from skill name:

| Category | Keywords |
|----------|----------|
| code | code, coding, python, mcp, debug, programming |
| writing | writing, article, pdf, doc, md, document |
| research | research, search, tavily, find, summarize |
| image | image, art, screenshot, vision, ollama-image, plantuml |
| video | video, podcast, remotion |
| audio | audio, tts, speech, voice, speak |
| ppt | ppt, presentation, slides |
| excel | excel, xlsx, spreadsheet |
| automation | automation, workflow, browser, cli, testing, playwright |
| devops | devops, deploy, docker, ci, security, vetter |
| design | design, canvas, brand, theme, artifact |
| data | data, database, sql, memory, lancedb, math, plot |
| communication | slack, wechat, chat, recap, evaluation, self-improvement |
| learning | paper, academic, research, content |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/skills | List all skills (with file_count) |
| POST | /api/skills | Create new skill |
| GET | /api/skills/:id | Get skill with all files |
| PUT | /api/skills/:id | Update skill |
| DELETE | /api/skills/:id | Delete skill (cascades to files) |
| GET | /api/categories | Get category counts |
| POST | /api/scan | Scan directory, import all skills |
| POST | /api/import-single | Import single skill from path |
| POST | /api/recategorize | Re-detect all skill categories |
| GET | /api/files/:id | Read file content |

## UI Features

### Home Page (/)
- Header with title, stats (total/enabled), theme toggle
- Search bar for name/description filtering
- Category filter buttons with counts
- Responsive card grid (auto-fill, min 320px)
- Import modal (bulk scan / single skill tabs)

### Skill Card
- Name, description (truncated 2 lines)
- Color-coded func_category badge
- Enabled/Disabled status badge
- File count
- Click to navigate to detail page

### Skill Detail Page (/skill/:id)
- Back button, skill name, description
- Theme toggle
- File list sidebar (300px width)
- File preview panel with markdown rendering
- File type icons

### Theme System
- Light/Dark mode via CSS variables
- Persisted in localStorage
- Toggle button (☀️/🌙) in header

## Import Feature

1. **Bulk Scan** (`POST /api/scan`)
   - Takes `source_dir` path
   - Scans all subdirectories for SKILL.md/CLAUDE.md
   - Auto-detects func_category from name
   - Imports all files into skill_files table

2. **Single Import** (`POST /api/import-single`)
   - Takes `path` to skill directory
   - Same parsing as bulk scan
   - Returns created skill with files

## File Type Detection

By extension:
- `.md` → markdown
- `.json` → json
- `.py` → python
- `.js` → javascript
- `.sh` → shell
- `.txt` → text
- `.yml/yaml` → yaml
- Other → unknown

## Color Palette

### Dark Theme (default)
- Background: #0a0a0f
- Card: #1a1a24
- Accent: #7c3aed
- Text: #ffffff

### Light Theme
- Background: #f5f7fa
- Card: #ffffff
- Accent: #7c3aed
- Text: #1a1a2e

### Category Colors
- code: blue
- writing: purple
- research: pink
- image: green
- video: yellow
- audio: orange
- ppt: indigo
- excel: teal
- automation: amber
- devops: red
- design: fuchsia
- data: cyan
- communication: teal
- learning: lime