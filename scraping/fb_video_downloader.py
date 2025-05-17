import yt_dlp

def download_facebook_video(url, output_path='fb_video1.mp4'):
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

video_url = 'https://www.facebook.com/reel/1060913925119880'
download_facebook_video(video_url)
