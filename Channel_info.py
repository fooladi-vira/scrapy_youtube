from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# تنظیمات API
DEVELOPER_KEY = ''  # کلید API خود را اینجا قرار دهید
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_channel_info(channel_id):
    # ساخت یک شیء سرویس YouTube API
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    try:
        # انجام یک درخواست به YouTube API برای دریافت اطلاعات کانال
        response = youtube.channels().list(
            id=channel_id,
            part='snippet,contentDetails,statistics'
        ).execute()

        return response

    except HttpError as e:
        print("An HTTP error occurred:\n", e)
        return None

# استفاده از تابع برای دریافت اطلاعات یک کانال
channel_id = 'UC_x5XG1OV2P6uZZ5FSM9Ttw'  # شناسه کانال Google Developers
channel_info = get_channel_info(channel_id)
if channel_info:
    print(channel_info)

