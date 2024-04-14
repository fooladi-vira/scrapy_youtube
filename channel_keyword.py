import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# تنظیمات
DEVELOPER_KEY = ''
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query, max_results):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    channels = []

    # جستجو برای کانال‌ها بر اساس کلمه کلیدی
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results,
        type='channel'
    ).execute()

    for search_result in search_response.get('items', []):
        channel_id = search_result['id']['channelId']
        
        # دریافت اطلاعات کانال
        channel_response = youtube.channels().list(
            part='statistics,snippet',
            id=channel_id
        ).execute()

        for channel in channel_response.get('items', []):
            subs = int(channel['statistics']['subscriberCount'])
            if subs > 1000000:
                channels.append({
                    'keyword': query,
                    'title': channel['snippet']['title'],
                    'subscriber_count': subs,
                    'channel_id': channel_id
                })

    return channels

def save_channels_to_csv(channels, filename):
    # ساخت یا باز کردن فایل CSV برای نوشتن
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['keyword', 'title', 'subscriber_count', 'channel_id']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # نوشتن هدرهای ستون فقط اگر فایل خالی است
        if file.tell() == 0:
            writer.writeheader()

        # نوشتن داده‌های کانال
        writer.writerows(channels)

# لیست کلمات کلیدی برای جستجو
keywords = ['technology', 'education', 'travel', 'music', 'cooking']

# حلقه برای جستجو و ذخیره اطلاعات برای هر کلمه کلیدی
for keyword in keywords:
    channels = youtube_search(keyword, 50)
    save_channels_to_csv(channels, 'channels.csv')

print("Data has been saved to 'channels.csv'.")
