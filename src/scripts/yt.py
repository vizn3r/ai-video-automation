import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from utils import Error
from meta import VideoMeta

CLIENT_SECRETS_FILE = os.environ["YT_SECRET"] or "./credentials.json"
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"

OUTPUT_DIR = os.environ["OUTPUT_DIR"] or "./"

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, YOUTUBE_UPLOAD_SCOPE)
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_video(video_file, data: VideoMeta):
    youtube = get_authenticated_service()
    body = {
        "snippet": {
            "title": data.video_title,
            "description": data.video_description,
            "tags": data.video_tags,
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": "public",
        },
    }
    print(body)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=googleapiclient.http.MediaFileUpload(video_file)
    )
    response = request.execute()
    print(f"Video uploaded: {response['id']}")

if __name__ == "__main__":
    Error("This script is not meant to run standalone")
    exit(0)
