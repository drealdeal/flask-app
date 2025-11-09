# yt_scraper.py

from flask import Flask, request, jsonify, render_template
from youtube_transcript_api import YouTubeTranscriptApi
from pyngrok import ngrok
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('mario.html')

@app.route('/webhook', methods=['POST'])
def process_url():
    try:
        # Log incoming headers and raw body for debugging
        print("Incoming Request Headers:", request.headers)
        print("Raw Request Body:", request.data.decode('utf-8'))

        # Attempt to parse JSON
        data = request.get_json(force=True, silent=True)
        if not data:
            print("Error: Request body is not valid JSON.")
            return jsonify({"error": "Request body is not valid JSON"}), 400

        print("Parsed JSON:", data)

        # Extract video_url
        video_url = data.get("video_url")
        if not video_url:
            print("Error: No video_url provided")
            return jsonify({"error": "No video_url provided"}), 400

        # Extract video ID
        video_id = video_url.split('v=')[-1].split('&')[0]
        print("Extracted Video ID:", video_id)

        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = '\n'.join([item['text'] for item in transcript])
        print("Transcript fetched successfully.")

        return jsonify({"transcript": full_transcript})

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Check if running locally (not on Render or other cloud platform)
    if os.environ.get('RENDER') or os.environ.get('DYNO'):
        # Running on cloud platform - use Gunicorn
        app.run(host="0.0.0.0", port=5000)
    else:
        # Running locally - use ngrok for easy mobile access
        port = 5000

        # Start ngrok tunnel
        public_url = ngrok.connect(port)
        print("\n" + "="*60)
        print("🎮 SUPER MARIO GAME - READY TO PLAY!")
        print("="*60)
        print(f"\n📱 Open this URL on your iPhone:")
        print(f"\n   {public_url}\n")
        print("="*60 + "\n")

        # Run Flask app
        app.run(host="0.0.0.0", port=port)
