# Study Material Analyzer

A web application that analyzes study materials (PDFs, images, and text files) to extract important topics and find relevant YouTube videos for learning.

## Features

- Upload PDFs, images (with OCR), or plain text files
- Automatic keyword/topic extraction
- Dynamic YouTube video search based on extracted topics
- Modern, responsive UI with drag-and-drop file upload

## Prerequisites

- Python 3.7 or higher
- Tesseract OCR (for image processing)
- YouTube Data API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd study-material-analyzer
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR:
- Windows: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- Linux: `sudo apt-get install tesseract-ocr`
- macOS: `brew install tesseract`

4. Set up YouTube API key:
- Create a project in [Google Cloud Console](https://console.cloud.google.com/)
- Enable YouTube Data API v3
- Create an API key
- Set the API key as an environment variable:
```bash
export YOUTUBE_API_KEY='your-api-key-here'
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload a file (PDF, image, or text) using the drag-and-drop interface or file picker

4. The application will:
   - Extract text from your file
   - Identify important keywords/topics
   - Search YouTube for relevant videos
   - Display the results with video thumbnails and descriptions

## Supported File Types

- PDF files
- Images (JPG, PNG) with OCR
- Plain text files (.txt)

## License

MIT License 