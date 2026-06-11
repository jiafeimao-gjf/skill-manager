# Skill Manager 🎯

A local web application for managing Claude Code skills with a visual interface.

[English](README.md) | [中文](README_zh.md)

## Features

- **Visual Skill Management** - Card-based grid UI with search and filtering
- **Category System** - 15 functional categories (code, writing, research, image, video, audio, ppt, excel, automation, devops, design, data, communication, learning)
- **File Browser** - View all skill files with markdown rendering
- **Light/Dark Theme** - Toggle between themes
- **Import** - Bulk scan directory or import single skill
- **SQLite Storage** - Fast, reliable JSON file-mapped database

## Tech Stack

- **Frontend**: Vue.js 3 + Vite (port 8529)
- **Backend**: Python Flask (port 9529)
- **Database**: SQLite

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:8529

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/skills | List all skills |
| POST | /api/skills | Create skill |
| GET | /api/skills/:id | Get skill with files |
| PUT | /api/skills/:id | Update skill |
| DELETE | /api/skills/:id | Delete skill |
| GET | /api/categories | Get category counts |
| POST | /api/scan | Bulk scan directory |
| POST | /api/import-single | Import single skill |
| POST | /api/recategorize | Re-detect all categories |
| GET | /api/files/:id | Read file content |

## Categories

| Category | Keywords |
|----------|----------|
| code | code, coding, python, mcp |
| writing | writing, article, pdf, doc |
| research | search, tavily, find, summarize |
| image | image, art, screenshot, vision |
| video | video, podcast, remotion |
| audio | audio, tts, speech, speak |
| ppt | ppt, presentation, slides |
| excel | excel, xlsx, spreadsheet |
| automation | browser, automation, cli |
| devops | deploy, docker, security |
| design | design, canvas, brand, theme |
| data | database, sql, memory, math |
| communication | slack, wechat, chat |
| learning | paper, academic |

## License

MIT