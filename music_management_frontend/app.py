from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

class DoublyNode:
    def __init__(self, song):
        self.song = song
        self.prev = None
        self.next = None

class MusicManagementSystem:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def songs(self):
        result, node = [], self.head
        while node:
            result.append(node.song)
            node = node.next
        return result

    def add_song(self, song):
        song = song.strip()
        if not song:
            return False, "Song name cannot be empty."
        node = DoublyNode(song)
        if self.head is None:
            self.head = self.tail = self.current = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        return True, f'"{song}" added to your playlist.'

    def find(self, song):
        node = self.head
        while node:
            if node.song.casefold() == song.strip().casefold():
                return node
            node = node.next
        return None

    def delete_song(self, song):
        node = self.find(song)
        if not node:
            return False, "Song not found."
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        if self.current is node:
            self.current = node.next or node.prev
        if self.head is None:
            self.tail = self.current = None
        return True, f'"{node.song}" removed from your playlist.'

    def move(self, direction):
        if self.current is None:
            return False, "Your playlist is empty."
        target = self.current.next if direction == "next" else self.current.prev
        if target is None:
            return False, "You're already at the " + ("last" if direction == "next" else "first") + " song."
        self.current = target
        return True, f'Now playing: "{self.current.song}"'

    def shuffle(self):
        items = self.songs()
        if not items:
            return False, "Your playlist is empty."
        random.shuffle(items)
        self.head = self.tail = self.current = None
        for song in items:
            node = DoublyNode(song)
            if self.head is None:
                self.head = self.tail = self.current = node
            else:
                node.prev = self.tail
                self.tail.next = node
                self.tail = node
        return True, "Playlist shuffled."

    def reverse_songs(self):
        return list(reversed(self.songs()))

music = MusicManagementSystem()

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/playlist")
def playlist():
    songs = music.songs()
    current_song = music.current.song if music.current else None
    return jsonify({"songs": songs, "current": current_song, "count": len(songs)})

@app.post("/api/add")
def add():
    data = request.get_json(silent=True) or {}
    ok, message = music.add_song(str(data.get("song", "")))
    return jsonify({"ok": ok, "message": message, **state()}), (200 if ok else 400)

@app.post("/api/delete")
def delete():
    data = request.get_json(silent=True) or {}
    ok, message = music.delete_song(str(data.get("song", "")))
    return jsonify({"ok": ok, "message": message, **state()}), (200 if ok else 404)

@app.post("/api/search")
def search():
    data = request.get_json(silent=True) or {}
    node = music.find(str(data.get("song", "")))
    return jsonify({"ok": bool(node), "message": f'Song found: "{node.song}"' if node else "Song not found."})

@app.post("/api/navigate")
def navigate():
    data = request.get_json(silent=True) or {}
    ok, message = music.move(str(data.get("direction", "next")))
    return jsonify({"ok": ok, "message": message, **state()}), (200 if ok else 400)

@app.post("/api/shuffle")
def shuffle():
    ok, message = music.shuffle()
    return jsonify({"ok": ok, "message": message, **state()}), (200 if ok else 400)

@app.post("/api/reverse")
def reverse():
    return jsonify({"songs": music.reverse_songs()})

def state():
    songs = music.songs()
    return {"songs": songs, "current": music.current.song if music.current else None, "count": len(songs)}

if __name__ == "__main__":
    app.run(debug=True)
