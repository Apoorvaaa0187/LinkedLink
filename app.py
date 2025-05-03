from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import PyPDF2
import pytesseract
from PIL import Image
import io
from collections import Counter
from googleapiclient.discovery import build
import mimetypes
import re
import traceback
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# YouTube API setup
YOUTUBE_API_KEY = "AIzaSyDQC4jLL0mnwcS96uU3qfk50t-CqLjiWrs"
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {str(e)}")
        raise

def extract_text_from_image(file):
    try:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error extracting image text: {str(e)}")
        raise

def extract_keywords(text):
    try:
        # Basic stop words list
        stop_words = set([
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
            'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
            'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
            'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other',
            'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
            'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way',
            'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us'
        ])
        
        # Convert to lowercase and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out stop words and short words
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Get most common keywords
        keyword_counts = Counter(keywords)
        return [word for word, _ in keyword_counts.most_common(10)]
    except Exception as e:
        print(f"Error extracting keywords: {str(e)}")
        raise

def search_youtube(query):
    try:
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=5,
            relevanceLanguage="en",
            videoDuration="medium"  # Filter for medium-length videos
        )
        response = request.execute()
        
        videos = []
        for item in response['items']:
            video = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'videoId': item['id']['videoId'],
                'thumbnail': item['snippet']['thumbnails']['default']['url']
            }
            videos.append(video)
        return videos
    except Exception as e:
        print(f"Error searching YouTube: {str(e)}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No selected file'}), 400
        
        # Get file type using mimetypes
        file_type, _ = mimetypes.guess_type(file.filename)
        
        # Process file based on type
        if file_type == 'application/pdf':
            text = extract_text_from_pdf(file)
        elif file_type and file_type.startswith('image/'):
            text = extract_text_from_image(file)
        else:
            text = file.read().decode('utf-8')
        
        if not text.strip():
            return jsonify({'status': 'error', 'message': 'No text could be extracted from the file'}), 400
        
        # Extract keywords
        keywords = extract_keywords(text)
        
        if not keywords:
            return jsonify({'status': 'error', 'message': 'No keywords could be extracted from the text'}), 400
        
        # Search YouTube for each keyword
        videos = []
        for keyword in keywords:
            videos.extend(search_youtube(keyword))
        
        # Remove duplicates based on videoId
        unique_videos = {video['videoId']: video for video in videos}.values()
        
        return jsonify({
            'status': 'success',
            'message': 'File processed successfully',
            'filename': file.filename,
            'keywords': keywords,
            'videos': list(unique_videos)
        })
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 