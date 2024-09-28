import os
import google.auth
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Constants
CLIENT_SECRETS_FILE = "./credentials.json"
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"

OUTPUT_DIR = os.environ["OUTPUT_DIR"] or "./"

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, YOUTUBE_UPLOAD_SCOPE)
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_video(youtube, video_file, title):
    body = {
        "snippet": {
            "title": title,
            #"description": description,
            #"tags": tags,
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": "public",
        },
    }

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=googleapiclient.http.MediaFileUpload(video_file)
    )
    response = request.execute()
    print(f"Video uploaded: {response['id']}")

if __name__ == "__main__":
    youtube = get_authenticated_service()
    video_file = OUTPUT_DIR + input("Video name: ") + ".mp4"
    title = input("YT Video title: ")

    upload_video(youtube, video_file, title)
