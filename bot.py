import urllib.request
import json
import os

# 1. 설정
shop_url = "https://www.myjoyfuldecisions.com/bottom"
discord_webhook_url = "https://discord.com/api/webhooks/1542020775794446436/bP0FLd4K7nP2bMapscuUGf3J2CatA4Q3GeGPx1bQBxUqi1TjQqH4FwEALLaqFn0YIelF"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# 봇의 기억을 저장할 메모장 이름
memory_file = "memory.txt"

# 이전에 저장해둔 기억(숫자)이 있으면 읽어오고, 처음이면 0으로 시작
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        previous_count = int(f.read().strip())
else:
    previous_count = 0

try:
    # 쇼핑몰 접속 및 글자 수 세기
    req = urllib.request.Request(shop_url, headers=headers)
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    
    current_count = html.count("재입고")
    print(f"이전 기억: {previous_count}개, 현재 화면: {current_count}개")
    
    # 갯수가 늘어났을 때만 알림 전송!
    if current_count > previous_count:
        print("🚨 새로운 재입고 발견! 알림을 보냅니다.")
        message = {
            "content": f"🚨 쇼핑몰에 새로운 바지 재입고 일정이 떴습니다!\n바로가기: {shop_url}"
        }
        data = json.dumps(message).encode('utf-8')
        discord_req = urllib.request.Request(discord_webhook_url, data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(discord_req)
        
    # 현재 갯수를 메모장에 다시 덮어쓰기 (기억 갱신)
    with open(memory_file, "w") as f:
        f.write(str(current_count))
        
except Exception as e:
    print("에러 발생:", e)
