# api/download.py
from http.client import responses
from flask import Flask, request, jsonify
from pytube import YouTube
import os
import json

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download():
    try:
        data = json.loads(request.data)
        url = data.get('url')
        format_type = data.get('format')
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        yt = YouTube(url)
        
        if format_type == 'mp4':
            stream = yt.streams.get_highest_resolution()
            file_extension = 'mp4'
        else:  # mp3
            stream = yt.streams.filter(only_audio=True).first()
            file_extension = 'mp3'
        
        return jsonify({
            "title": yt.title,
            "author": yt.author,
            "length": yt.length,
            "url": stream.url,
            "filename": f"{yt.title}.{file_extension}"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok"})
