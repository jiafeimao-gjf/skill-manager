# Skill Manager 🎯

本地 Claude Code 技能可视化管理系统。

[English](README.md) | [中文](README_zh.md)

## 功能特性

- **可视化技能管理** - 卡片网格布局，支持搜索和分类过滤
- **分类系统** - 15个功能分类（代码、写作、研究、图片、视频、音频、PPT、Excel、自动化、运维、设计、数据、通讯、学习）
- **文件浏览器** - 查看所有技能文件，支持 Markdown 渲染
- **浅色/深色主题** - 一键切换
- **导入功能** - 批量扫描目录或导入单个技能
- **SQLite 存储** - 快速可靠的数据库

## 技术栈

- **前端**: Vue.js 3 + Vite (端口 8529)
- **后端**: Python Flask (端口 9529)
- **数据库**: SQLite

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:8529

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/skills | 获取所有技能 |
| POST | /api/skills | 创建技能 |
| GET | /api/skills/:id | 获取技能及文件 |
| PUT | /api/skills/:id | 更新技能 |
| DELETE | /api/skills/:id | 删除技能 |
| GET | /api/categories | 获取分类统计 |
| POST | /api/scan | 批量扫描目录 |
| POST | /api/import-single | 导入单个技能 |
| POST | /api/recategorize | 重新分类所有技能 |
| GET | /api/files/:id | 读取文件内容 |

## 技能分类

| 分类 | 关键词 |
|------|--------|
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

## 许可证

MIT