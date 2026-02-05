import requests
import webbrowser
from flask import Flask, render_template_string, request
from bs4 import BeautifulSoup

app = Flask(__name__)

COOKIES = {
    'webp': '1804671467324',
    'avif': '1804671467324',
    'session-secret': '0659ee98a97cb6de9d68ccd3645c18d6c0d0',
    'i18n-activated-languages': 'vi',
    'snowflake': 'OJ9xRidmgUldNvU4aa4%2Fkg%3D%3D',
    'lev': '1',
    'window-height': '793',
    'screen-width': '1692',
    'screen-height': '952',
    'device-pixel-ratio': '1.1354166269302368',
    'time-zone': 'Asia%2FBangkok',
    'js': '1',
    'device-token': 'bXUW%2F8Sp26mb9LeWqkU0WbiX',
    '_gcl_au': '1.1.1797552091.1770111479',
    '_ga': 'GA1.1.674766517.1770111479',
    'window-width': '1033',
    'fingerprint': 'kki6PiFBeu7LtQHZbVGdij8WY1J_36G0D0amv5lQAuPMSap1AASRnQOTCM4CcSjFzmUgAACTCM4DKAikzmFgAACTCM4Dctn-zk8AAACTCM4AgWiJzknAAACTCM4AcCQKzkzgAACTCM4E9JN-znBgAACTCM4Acmd8zhPAAACTCM4Afh_fzjmgAACTCM4De2WmzguAAACTCM4DSxWuzjkgAACTCM4DVAA8ziRAAACTCM4AaV_uzkTgAAA',
    '_ga_LCTR22QQ87': 'GS2.1.s1770111479$o1$g1$t1770111631$j60$l0$h611121615',
}

HEADERS = {
    'accept': '*/*',
    'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://turboscribe.ai',
    'priority': 'u=1, i',
    'referer': 'https://turboscribe.ai/vi/downloader/2025-01-01/youtube/video',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'x-lev-xhr': '',
    'x-turbolinks-loaded': '',
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Downloader</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #0b0f1a; color: #e5e7eb; font-family: 'Inter', sans-serif; }
        .glass { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); }
        .btn-gradient { background: linear-gradient(90deg, #0ea5e9, #2563eb); transition: all 0.3s; }
        .btn-gradient:hover { opacity: 0.9; transform: translateY(-1px); }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center py-12 px-4">
    <div class="w-full max-w-4xl">
        <div class="text-center mb-12">
            <h1 class="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 mb-4">
                YT Tool
            </h1>
            <p class="text-gray-400">Tải Video YouTube & Chép lời tự động</p>
        </div>

        <form method="POST" class="flex flex-col sm:flex-row gap-3 mb-10">
            <input type="text" name="url" placeholder="Dán link YouTube hoặc Shorts vào đây..." required 
                   class="flex-1 bg-gray-900/50 border border-gray-700 rounded-xl px-5 py-4 focus:outline-none focus:ring-2 focus:ring-blue-500 text-white">
            <button type="submit" class="btn-gradient px-8 py-4 rounded-xl font-bold text-white shadow-lg">
                PHÂN TÍCH LINK
            </button>
        </form>

        {% if error %}
        <div class="bg-red-500/10 border border-red-500/50 text-red-400 p-5 rounded-xl mb-8 flex items-center gap-3">
            <i class="fas fa-exclamation-circle"></i> {{ error }}
        </div>
        {% endif %}

        {% if data %}
        <div class="glass rounded-3xl p-8 shadow-2xl animate-fade-in">
            <div class="flex flex-col md:flex-row gap-8">
                <div class="w-full md:w-1/3">
                    <img src="{{ data.thumb }}" class="w-full rounded-2xl shadow-lg border border-white/10">
                </div>
                <div class="flex-1">
                    <h2 class="text-2xl font-bold mb-6 text-white leading-tight">{{ data.title }}</h2>
                    
                    <div class="space-y-4">
                        {% for link in data.links %}
                        <div class="flex items-center justify-between bg-white/5 p-4 rounded-2xl hover:bg-white/10 transition-all border border-transparent hover:border-white/10">
                            <div class="flex items-center gap-4">
                                <div class="bg-blue-500/20 p-3 rounded-xl text-blue-400">
                                    <i class="fas {% if 'mp4' in link.name.lower() %}fa-video{% else %}fa-music{% endif %}"></i>
                                </div>
                                <div>
                                    <p class="font-semibold text-gray-200 text-sm md:text-base truncate max-w-[150px] md:max-w-xs">{{ link.name }}</p>
                                    <p class="text-xs text-gray-500 uppercase tracking-tighter">{{ link.res }} • {{ link.size }}</p>
                                </div>
                            </div>
                            <div class="flex gap-2">
                                <a href="{{ link.url }}" target="_blank" class="bg-emerald-500/20 hover:bg-emerald-500 text-emerald-400 hover:text-white p-3 rounded-xl transition-all" title="Tải xuống">
                                    <i class="fas fa-download"></i>
                                </a>
                                <a href="https://turboscribe.ai/vi/u/transcribe-youtube-video" target="_blank" class="bg-blue-500/20 hover:bg-blue-500 text-blue-400 hover:text-white p-3 rounded-xl transition-all" title="Chép lời">
                                    <i class="fas fa-file-signature"></i>
                                </a>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    error = None
    if request.method == 'POST':
        try:
            target_url = request.form.get('url')
            resp = requests.post(
                'https://turboscribe.ai/_htmx/NCN20gAEkZMBzQPXkQc',
                cookies=COOKIES,
                headers=HEADERS,
                json={'url': target_url},
                timeout=20
            )

            if resp.status_code != 200:
                error = f"Lỗi từ Turboscribe (Mã {resp.status_code}). Cookie có thể đã hết hạn!"
            else:
                soup = BeautifulSoup(resp.text, 'html.parser')
                title_tag = soup.find('h1')
                if not title_tag:
                    error = "Không tìm thấy dữ liệu video. Hãy thử lại hoặc cập nhật Cookie mới."
                else:
                    links = []
                    blocks = soup.find_all('div', class_='block')
                    for block in blocks:
                        dl_link = block.find('a', class_='dui-btn-primary')
                        if dl_link:
                            spans = block.find_all('span')
                            # Lấy tên file
                            file_name_div = block.find('div')
                            file_name = file_name_div.text.strip() if file_name_div else "Unknown File"
                            
                            links.append({
                                'name': file_name,
                                'res': spans[0].text if len(spans) > 0 else "N/A",
                                'size': spans[1].text if len(spans) > 1 else "N/A",
                                'url': dl_link['href']
                            })

                    data = {
                        'title': title_tag.text.strip(),
                        'thumb': soup.find('img')['src'] if soup.find('img') else "",
                        'links': links
                    }
        except Exception as e:
            error = f"Lỗi hệ thống: {str(e)}"

    return render_template_string(HTML_TEMPLATE, data=data, error=error)

if __name__ == '__main__':
    port = 5000
    print(f"--- TOOL ĐANG CHẠY TẠI http://127.0.0.1:{port} ---")
    webbrowser.open(f"http://127.0.0.1:{port}")
    app.run(debug=True, port=port, use_reloader=False)
