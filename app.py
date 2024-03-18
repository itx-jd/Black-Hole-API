import requests
import yt_dlp
import requests
import re
import json
from flask import Flask, jsonify


RapidAPI_Key = "71170096d0mshaeba07d8177372ep1813bbjsnde293edbcc48"
RapidAPI_Host = "all-media-downloader1.p.rapidapi.com"


app = Flask(__name__)

def get_instagram_video(url):
    try:
        api_url = "https://all-media-downloader1.p.rapidapi.com/Instagram"
        payload = {"url": url}
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": RapidAPI_Key,
            "X-RapidAPI-Host": RapidAPI_Host
        }
        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'result' in data and data['result']:
                video_url = data['result'][0].get('_url')
                if video_url:
                    return {'success': True, 'video_url': video_url}
            return {'success': False, 'error_message': 'Failed to retrieve Instagram video information'}
        else:
            return {'success': False, 'error_message': 'Failed to retrieve Instagram video information'}

    except requests.exceptions.RequestException as e:
        return {'success': False, 'error_message': str(e)}


def get_tiktok_video(url):
    try:
        api_url = "https://all-media-downloader1.p.rapidapi.com/tiktok"
        payload = {"url": url}
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": RapidAPI_Key,
            "X-RapidAPI-Host": RapidAPI_Host
        }
        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'result' in data and 'data' in data['result']:
                video_url = data['result']['data'].get('play')
                if video_url:
                    return {'success': True, 'video_url': video_url}
            return {'success': False, 'error_message': 'Failed to retrieve TikTok video information'}
        else:
            return {'success': False, 'error_message': 'Failed to retrieve TikTok video information'}

    except requests.exceptions.RequestException as e:
        return {'success': False, 'error_message': str(e)}


def get_threads_video(url):
    try:
        api_url = "https://all-media-downloader1.p.rapidapi.com/threads"
        payload = {"url": url}
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": RapidAPI_Key,
            "X-RapidAPI-Host": RapidAPI_Host
        }
        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'result' in data and 'video_urls' in data['result'] and data['result']['video_urls']:
                video_url = data['result']['video_urls'][0].get('download_url')
                if video_url:
                    return {'success': True, 'video_url': video_url}
            return {'success': False, 'error_message': 'Failed to retrieve video URL from Threads'}
        else:
            return {'success': False, 'error_message': 'Failed to retrieve video URL from Threads'}

    except requests.exceptions.RequestException as e:
        return {'success': False, 'error_message': str(e)}

def get_douyin_video(url):
    try:
        api_url = "https://all-media-downloader1.p.rapidapi.com/douyin"
        payload = {"url": url}
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": RapidAPI_Key,
            "X-RapidAPI-Host": RapidAPI_Host
        }
        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'douyinResults' in data and 'result' in data['douyinResults'] and 'data' in data['douyinResults']['result']:
                video_url = data['douyinResults']['result']['data'].get('play')
                if video_url:
                    return {'success': True, 'video_url': video_url}
            return {'success': False, 'error_message': 'Failed to retrieve Douyin video information'}
        else:
            return {'success': False, 'error_message': 'Failed to retrieve Douyin video information'}

    except requests.exceptions.RequestException as e:
        return {'success': False, 'error_message': str(e)}


def get_facebook_video(url):
    try:
        api_url = "https://facebook-reel-and-video-downloader.p.rapidapi.com/app/main.php"
        querystring = {"url": url}
        headers = {
            "X-RapidAPI-Key": "71170096d0mshaeba07d8177372ep1813bbjsnde293edbcc48",
	        "X-RapidAPI-Host": "facebook-reel-and-video-downloader.p.rapidapi.com"
        }
        response = requests.get(api_url, headers=headers, params=querystring)

        if response.status_code == 200:
            data = response.json()
            if data['success'] and 'links' in data and 'Download High Quality' in data['links']:
                video_url = data['links']['Download High Quality']
            elif 'links' in data and 'Download Low Quality' in data['links']:
                video_url = data['links']['Download Low Quality']
            else:
                return {'success': False, 'error_message': 'No download links available'}

            return {'success': True, 'video_url': video_url}
        else:
            return {'success': False, 'error_message': 'Failed to retrieve Facebook video information'}

    except requests.exceptions.RequestException as e:
        return {'success': False, 'error_message': str(e)}


def get_ytdlp_video(url):
    ydl_opts = {
        'format': 'best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict.get('url')
           
            return {'success': True,'video_url': video_url, }

        except yt_dlp.utils.DownloadError as e:
            return {'success': False, 'error_message': str(e)}
        

def clean_str(s):
    return json.loads('{"text": "' + s + '"}')['text']

def get_hd_link(content):
    regex_rate_limit = r'browser_native_hd_url":"([^"]+)"'
    match = re.search(regex_rate_limit, content)
    return clean_str(match.group(1)) if match else None

def get_facebook_com_video(url):
    headers = {
        'sec-fetch-user': '?1',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-site': 'none',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'cache-control': 'max-age=0',
        'authority': 'www.facebook.com',
        'upgrade-insecure-requests': '1',
        'accept-language': 'en-GB,en;q=0.9,tr-TR;q=0.8,tr;q=0.7,en-US;q=0.6',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()

        video_url = get_hd_link(response.text)
        video_url = video_url + '&dl=1'

        return {'success': True, 'video_url': video_url}

    except requests.exceptions.RequestException as e:
        return {'success': False, 'message': str(e)}
    


@app.route('/<path:video_url>', methods=['GET'])
def get_video_info_endpoint(video_url):
    
    if video_url.lower() == 'favicon.ico':
        # Handle favicon.ico request (return an empty response or your favicon)
        return ''

    if 'facebook.com' in video_url:
        result = get_facebook_com_video(video_url)
    elif 'fb.watch' in video_url or 'startTimeMs' in video_url:
        result = get_facebook_video(video_url)
    elif 'instagram.com' in video_url:
        result = get_instagram_video(video_url)
    elif 'tiktok.com' in video_url:
        result = get_tiktok_video(video_url)
    elif 'threads' in video_url:
        result = get_threads_video(video_url)
    elif 'douyin' in video_url:
        result = get_douyin_video(video_url)
    else:
        result = get_ytdlp_video(video_url)

    if(result.__contains__('error_message')):
        response_data = {
            'success': False,
            'error_message': result['error_message']
        }
    else:
        response_data = {
            'success': True,
            'video_url': result['video_url']
        }

    return jsonify(response_data)

# Run the Flask app

if __name__ == '__main__':

    app.run(debug=True)
