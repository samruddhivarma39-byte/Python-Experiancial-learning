# Soundwave — Music Management System

A modern Tailwind CSS frontend for the linked-list music playlist app, backed by Flask.

## Requirements
- Python 3.9+
- Flask

## Run locally
1. Open a terminal in this folder.
2. Install Flask:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python app.py
   ```
4. Open http://127.0.0.1:5000 in your browser.

## Files
- `app.py` — Flask server and doubly linked-list playlist operations
- `templates/index.html` — responsive frontend using Tailwind CSS CDN
- `requirements.txt` — Python dependency list

Note: this is a playlist manager, not an audio streaming player. Playlist data is held in memory and resets when the server restarts.
