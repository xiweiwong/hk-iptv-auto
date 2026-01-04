import requests
import re
import datetime
from opencc import OpenCC

# 初始化繁簡轉換器
cc = OpenCC('s2t')

# --- 設定區 ---

# 1. 來源列表 (包含你剛剛要的更多來源)
SOURCE_URLS = [
    "https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u",
    "https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u",
    "https://raw.githubusercontent.com/Kimentanm/aptv/master/m3u/iptv.m3u",
    "https://raw.githubusercontent.com/yuanzl77/IPTV/main/live.m3u",
    "https://iptv-org.github.io/iptv/countries/hk.m3u",
    "https://raw.githubusercontent.com/joevess/IPTV/main/home.m3u8",
    "https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u"
]

# 2. 關鍵字過濾
# 這裡可以用比較寬鬆的寫法，因為後面我們會統一修正名稱
KEYWORDS = [
    "ViuTV", "HOY", "RTHK", "Jade", "Pearl", "J2", "J5", "Now", 
    "无线", "無線", "有线", "有線", "翡翠", "明珠", "港台", 
    "电视", "電視", "高清", "News"
]

# 3. 必備的官方/穩定源
STATIC_CHANNELS = [
    {"name": "RTHK 31", "url": "https://rthklive1-lh.akamaihd.net/i/rthk31_1@167495/index_2052_av-b.m3u8"},
    {"name": "RTHK 32", "url": "https://rthklive2-lh.akamaihd.net/i/rthk32_1@168450/index_2052_av-b.m3u8"}
]

# --- 邏輯區 ---

def check_url(url):
    """檢測鏈接是否有效 (超時 2 秒)"""
    try:
        response = requests.get(url, timeout=2, stream=True)
        return response.status_code == 200
    except:
        return False

def fetch_and_parse():
    found_channels = []
    
    print("正在抓取網路源...")
    for source in SOURCE_URLS:
        try:
            print(f"Processing: {source}")
            r = requests.get(source)
            if r.status_code != 200: continue
            
            lines = r.text.split('\n')
            current_name = ""
            
            for line in lines:
                line = line.strip()
                if not line: continue
                
                if line.startswith("#EXTINF"):
                    # 提取頻道名稱
                    match = re.search(r',(.+)$', line)
                    if match:
                        raw_name = match.group(1).strip()
                        
                        # 1. 先轉為標準繁體
                        converted_name = cc.convert(raw_name)
                        
                        # 2. 【關鍵修正】強制將「臺」替換為「台」
                        current_name = converted_name.replace('臺', '台')
                        
                elif line.startswith("http") and current_name:
                    # 檢查名稱是否包含關鍵字
                    # 將 關鍵字 也做同樣的處理，確保能匹配
                    if any(cc.convert(k).replace('臺', '台').lower() in current_name.lower() for k in KEYWORDS):
                        # 去重
                        if not any(c['url'] == line for c in found_channels):
                            found_channels.append({"name": current_name, "url": line})
                    current_name = "" # 重置
        except Exception as e:
            print(f"Error fetching {source}: {e}")

    return found_channels

def generate_m3u(channels):
    print(f"共找到 {len(channels)} 個潛在頻道，開始檢測有效性...")
    
    final_list = []
    
    # 1. 加入靜態源
    for static in STATIC_CHANNELS:
        final_list.append(static)
        
    # 2. 檢測網路源
    for ch in channels:
        print(f"Checking: {ch['name']}...", end=" ")
        if check_url(ch['url']):
            final_list.append(ch)
            print("OK")
        else:
            print("FAIL")

    # 3. 寫入文件
    content = '#EXTM3U x-tvg-url="https://epg.112114.xyz/pp.xml"\n'
    content += f'# Update: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
    
    for item in final_list:
        # 最後輸出時，再次確認是「台」
        final_name = item["name"].replace('臺', '台')
        content += f'#EXTINF:-1 group-title="Hong Kong" logo="https://epg.112114.xyz/logo/{final_name}.png",{final_name}\n'
        content += f'{item["url"]}\n'

    with open("hk_live.m3u", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"完成！共收錄 {len(final_list)} 個有效頻道。")

if __name__ == "__main__":
    candidates = fetch_and_parse()
    generate_m3u(candidates)
