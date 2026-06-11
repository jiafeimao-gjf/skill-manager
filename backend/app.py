from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import sqlite3
import os
import re
import yaml

app = Flask(__name__)
CORS(app)

DB_FILE = 'skills.db'
SCHEMA_FILE = 'schema.sql'

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_FILE):
        conn = get_db()
        with open(SCHEMA_FILE, 'r') as f:
            conn.executescript(f.read())
        conn.close()

def parse_skill_info(file_path):
    """Parse name and description from SKILL.md or CLAUDE.md"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if yaml_match:
            try:
                data = yaml.safe_load(yaml_match.group(1))
                return data.get('name', ''), data.get('description', '')
            except:
                pass
        lines = content.strip().split('\n')
        return '', lines[0] if lines else ''
    except:
        return '', ''

def get_file_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    types = {
        '.md': 'markdown',
        '.json': 'json',
        '.py': 'python',
        '.js': 'javascript',
        '.sh': 'shell',
        '.txt': 'text',
        '.yml': 'yaml',
        '.yaml': 'yaml'
    }
    return types.get(ext, 'unknown')

@app.route('/api/skills', methods=['GET'])
def get_skills():
    conn = get_db()
    skills = conn.execute('''
        SELECT s.*, COUNT(f.id) as file_count
        FROM skills s
        LEFT JOIN skill_files f ON s.id = f.skill_id
        GROUP BY s.id
        ORDER BY s.name
    ''').fetchall()
    conn.close()
    return jsonify([dict(s) for s in skills])

@app.route('/api/skills', methods=['POST'])
def create_skill():
    data = request.json
    conn = get_db()
    try:
        cursor = conn.execute('''
            INSERT INTO skills (name, description, category, enabled, source_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('name', ''),
            data.get('description', ''),
            data.get('category', 'general'),
            1 if data.get('enabled', True) else 0,
            data.get('source_path', '')
        ))
        conn.commit()
        skill_id = cursor.lastrowid
        skill = conn.execute('SELECT * FROM skills WHERE id = ?', (skill_id,)).fetchone()
        conn.close()
        return jsonify(dict(skill)), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/skills/<int:skill_id>', methods=['GET'])
def get_skill(skill_id):
    conn = get_db()
    skill = conn.execute('SELECT * FROM skills WHERE id = ?', (skill_id,)).fetchone()
    if not skill:
        conn.close()
        return jsonify({'error': 'Skill not found'}), 404
    files = conn.execute('SELECT * FROM skill_files WHERE skill_id = ?', (skill_id,)).fetchall()
    conn.close()
    return jsonify({
        'skill': dict(skill),
        'files': [dict(f) for f in files]
    })

@app.route('/api/skills/<int:skill_id>', methods=['PUT'])
def update_skill(skill_id):
    data = request.json
    conn = get_db()
    conn.execute('''
        UPDATE skills
        SET name = COALESCE(?, name),
            description = COALESCE(?, description),
            category = COALESCE(?, category),
            enabled = COALESCE(?, enabled)
        WHERE id = ?
    ''', (
        data.get('name'),
        data.get('description'),
        data.get('category'),
        1 if data.get('enabled') else 0 if data.get('enabled') is not None else None,
        skill_id
    ))
    conn.commit()
    skill = conn.execute('SELECT * FROM skills WHERE id = ?', (skill_id,)).fetchone()
    conn.close()
    if skill:
        return jsonify(dict(skill))
    return jsonify({'error': 'Skill not found'}), 404

@app.route('/api/skills/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    conn = get_db()
    conn.execute('DELETE FROM skill_files WHERE skill_id = ?', (skill_id,))
    conn.execute('DELETE FROM skills WHERE id = ?', (skill_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Skill deleted'})

@app.route('/api/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    conn = get_db()
    file = conn.execute('SELECT * FROM skill_files WHERE id = ?', (file_id,)).fetchone()
    conn.close()
    if not file:
        return jsonify({'error': 'File not found'}), 404
    filepath = file['filepath']
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found on disk'}), 404
    return send_file(filepath)

@app.route('/api/scan', methods=['POST'])
def scan_directory():
    data = request.json
    source_dir = data.get('source_dir', '')
    if not source_dir or not os.path.isdir(source_dir):
        return jsonify({'error': 'Invalid directory path'}), 400

    conn = get_db()
    imported = []
    skipped = []

    existing = {row['name'] for row in conn.execute('SELECT name FROM skills').fetchall()}

    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        if not os.path.isdir(item_path):
            continue

        skill_file = None
        for fname in ['SKILL.md', 'CLAUDE.md', 'skill.md']:
            fpath = os.path.join(item_path, fname)
            if os.path.exists(fpath):
                skill_file = fpath
                break

        if not skill_file:
            continue

        name, description = parse_skill_info(skill_file)
        skill_name = name if name else item

        if skill_name in existing:
            skipped.append(skill_name)
            continue

        cursor = conn.execute('''
            INSERT INTO skills (name, description, category, enabled, source_path)
            VALUES (?, ?, ?, 1, ?)
        ''', (skill_name, description[:500] if description else '', 'imported', item_path))
        skill_id = cursor.lastrowid

        for root, dirs, files in os.walk(item_path):
            for fname in files:
                if fname.startswith('.'):
                    continue
                fpath = os.path.join(root, fname)
                rel_path = os.path.relpath(fpath, item_path)
                file_type = get_file_type(fname)
                conn.execute('''
                    INSERT INTO skill_files (skill_id, filename, filepath, file_type)
                    VALUES (?, ?, ?, ?)
                ''', (skill_id, fname, fpath, file_type))

        existing.add(skill_name)
        imported.append(skill_name)

    conn.commit()
    conn.close()
    return jsonify({'imported': imported, 'skipped': skipped})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=9529)