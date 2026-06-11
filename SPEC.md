# Skill Manager - Design Specification

## Overview

A local web application for managing Claude Code skills with CRUD operations and directory import capability.

## Tech Stack

- **Frontend**: Vue.js 3 + Vite (port 8529)
- **Backend**: Python Flask (port 9529)
- **Storage**: JSON file-based

## Architecture

```
skill_manager/
├── backend/
│   ├── app.py              # Flask REST API
│   ├── requirements.txt
│   └── skills/
│       └── skills.json     # Data storage
└── frontend/
    ├── index.html
    ├── vite.config.js       # Proxy config
    ├── package.json
    └── src/
        ├── main.js
        ├── App.vue          # Main + Import UI
        ├── assets/main.css
        └── components/SkillList.vue
```

## Data Model

```json
{
  "id": 1,
  "name": "skill-name",
  "description": "Description",
  "category": "development|testing|design|general|imported",
  "enabled": true,
  "source_path": "/path/to/skill"  // for imported skills
}
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/skills | List all skills |
| POST | /api/skills | Create skill |
| GET | /api/skills/:id | Get single skill |
| PUT | /api/skills/:id | Update skill |
| DELETE | /api/skills/:id | Delete skill |
| POST | /api/import | Import skills from directory |

## Import Feature

1. User enters directory path (e.g., `~/.claude/skills`)
2. Backend scans for subdirectories containing `CLAUDE.md`
3. First line of CLAUDE.md used as description
4. New skills added with `imported` category
5. Returns list of imported skill names

## Categories

- `development` - Development tools
- `testing` - Testing related
- `design` - Design tools
- `general` - General purpose
- `imported` - Imported from directory

## UI Components

### Header
- Title with emoji: 🎯 Skill Manager

### Form Card
- Name input (text)
- Category dropdown
- Description textarea
- Enabled checkbox
- Submit button (Add/Update)

### Import Card
- Directory path input
- Import button
- Result display

### Skill List Card
- Table with columns: Name, Category, Description, Status, Actions
- Enable/Disable toggle button
- Edit button
- Delete button

## Status Badges

- Enabled: green badge
- Disabled: red badge
- Category: blue badge