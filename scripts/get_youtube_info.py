import os
import googleapiclient.discovery
from google.oauth2.credentials import Credentials

# YouTube Data API 密钥
API_KEY = os.getenv("YOUTUBE_API_KEY")  # 请设置您的密钥或在环境变量中设置

# 频道信息
channel_ids = {
    "tvbs": "2mCSYvcfhtc",
    "ttv": "xL0ch83RAK8",
    "set": "FoBfXvlOR6I",
    "ctv": "TCnaIE_SAtM",
    "ftv": "P8DRJChuQQQ",
    "ebc": "R2iMq5LKXco",
    "ebcf": "ABn_ccXn_jc",
    "cti": "_QbRXRnHMVY",
    "gntv": "HXcm22-69Og",
    "cgtn": "FGabkYr-Sfs",
    "nhk": "f0lYkdA-Gtw",
    "fr24": "h3MuIUNCCzI",
    "pinhfr": "8ysjF7BCtRE",
    "cgtnhfr": "oWwQuAN-KZc",
}

# 输出目录
output_directory = "channels"

# 创建输出目录
os.makedirs(output_directory, exist_ok=True)

# 初始化 YouTube Data API
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

# 获取频道信息
for channel_name, channel_id in channel_ids.items():
    # 获取频道的直播视频
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        eventType="live",
        type="video",
        maxResults=1,
    )
    response = request.execute()
    videos = response.get("items", [])

    if videos:
        # 获取视频的直播流信息
        video_id = videos[0]["id"]["videoId"]
        request = youtube.videos().list(
            part="liveStreamingDetails",
            id=video_id,
        )
        response = request.execute()
        live_details = response.get("items", [])[0]["liveStreamingDetails"]
        m3u8_url = live_details["hlsUrl"]

        # 保存到对应的 m3u8 文件
        output_file = os.path.join(output_directory, f"{channel_name}.m3u8")
        with open(output_file, "w") as f:
            f.write(f"#EXTM3U\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=540000\n{m3u8_url}")
