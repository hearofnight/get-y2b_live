import requests
import sys

def get_youtube_live_info(api_key, video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=liveStreamingDetails&key={api_key}'
    response = requests.get(url)
    data = response.json()
    
    if 'items' in data and data['items']:
        live_info = data['items'][0]['liveStreamingDetails']
        return live_info
    else:
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_youtube_info.py <API_KEY>")
        sys.exit(1)

    youtube_api_key = sys.argv[1]
    video_id = '2dfAzcDf8Zg'  # Replace with the actual YouTube video ID

    live_info = get_youtube_live_info(youtube_api_key, video_id)

    if live_info:
        print(f"Live Broadcast started at: {live_info['actualStartTime']}")
        print(f"Live Broadcast ended at: {live_info['actualEndTime']}")
    else:
        print("Unable to retrieve live broadcast information.")
