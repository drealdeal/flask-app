# yt_scraper.py

from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
# from pyngrok import ngrok  # <- Not needed on Render

app = Flask(__name__)

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
    # For local dev only; Render uses Gunicorn
    # If you are testing locally, you can do:
    #   python yt_scraper.py
    # and it will run on http://localhost:5000
    app.run(host="0.0.0.0", port=5000)
