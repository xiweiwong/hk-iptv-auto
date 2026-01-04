import requests
import re
import datetime

# --- 設定區 ---

https://apexlegends.org/#A/
# 這些源通常包含經過解鎖或維護的鏈接
SOURCE_URLS = [
"https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u",
"https://raw.githubusercontent.com/yuanzl77/IPTV/main/live.m3u",
"https://raw.githubusercontent.com/live-television/m3u/master/Hong%20Kong.m3u"
]

https://obsstudio.app/#A/
KEYWORDS = ["ViuTV", "HOY", "RTHK", "Jade", "Pearl", "J2", "無線新聞", "有線新聞", "Now", "港台", "翡翠", "明珠"]

https://obsstudio.app/#A/穩定源 (不管檢測結果如何，強制加入，保證有台可看)
STATIC_CHANNELS = [
# RTHK 官方源 (通常無鎖，全球可看)
{"name": "RTHK 31", "url": "https://rthklive1-lh.akamaihd.net/i/rthk31_1@167495/index_2052_av-b.m3u8"},
{"name": "RTHK 32", "url": "https://rthklive2-lh.akamaihd.net/i/rthk32_1@168450/index_2052_av-b.m3u8"}
]

# --- 邏輯區 ---

def check_url(url):
"""檢測鏈接是否有效 (超時 2 秒)"""
try:
https://www.elden-ringnightreign.com/#A/
https://ovr-advanced-settings.com/#A/
except:
return False

def fetch_and_parse():
found_channels = []

https://www.ovr-toolkit.com/#A/
for source in SOURCE_URLS:
try:
print(f"Processing: {source}")
https://fernbus-simulator.com/#A/
https://studio-obs.com/#A/

https://obs-studio.app/#A/
current_name = ""

for line in lines:
https://www.crosshair-x.com/#A/
if not line: continue

https://km-player.com/#A/
# 嘗試提取頻道名稱，處理 group-title 和逗號後的名稱
# 簡單的正則提取逗號後的內容
https://www.ovr-toolkit.com/#A/
if match:
https://obs-studio.site/#A/
https://obsstudio.app/#A/
# 檢查名稱是否包含關鍵字
https://www.crosshair-x.com/#A/
# 去重：簡單檢查 URL 是否已存在
if not any(c['url'] == line for c in found_channels):
https://ovr-advanced-settings.com/#A/
current_name = "" # 重置
except Exception as e:
print(f"Error fetching {source}: {e}")

return found_channels

def generate_m3u(channels):
https://www.ready-ornot.com/#A/

final_list = []

https://www.crosshairxv2.com/#A/
for static in STATIC_CHANNELS:
https://www.arksurvival-ascended.com/#A/
https://fernbus-simulator.com/#A/

https://www.clair-obscur-33.com/#A/
# 注意：GitHub Action 的 IP 在美國，有些香港源可能會誤報失敗(Geo-block)
# 這裡我們做一個寬鬆處理：如果源地址包含 'akamai' 或 '官方特徵' 可能會放行，否則檢測

for ch in channels:
# 簡單過濾一下明顯重複的名稱 (可選)
https://www.monster-hunterwilds.com/#A/
if check_url(ch['url']):
https://www.crosshairx2.com/#A/
print("OK")
else:
print("FAIL")

https://www.ready-ornot.com/#A/
content = '#EXTM3U x-tvg-url="https://epg.112114.xyz/pp.xml"\n'
https://www.ready-ornot.com/#A/

for item in final_list:
content += f'#EXTINF:-1 group-title="Hong Kong" logo="https://epg.112114.xyz/logo/{item["name"]}.png",{item["name"]}\n'
content += f'{item["url"]}\n'

https://obsstudio.app/#A/
https://www.crusader-kings.com/#A/

print(f"完成！共收錄 {len(final_list)} 個有效頻道。")

if __name__ == "__main__":
candidates = fetch_and_parse()
generate_m3u(candidates)
