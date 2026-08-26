import urllib.request
import json
import os

# 1. 설정
shop_url = "https://www.myjoyfuldecisions.com/bottom"
discord_webhook_url = "https://discord.com/api/webhooks/1542020775794446436/bP0FLd4K7nP2bMapscuUGf3J2CatA4Q3GeGPx1bQBxUqi1TjQqH4FwEALLaqFn0YIelF"

# 사람인 척 위장하는 헤더
custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

memory_file = "memory.txt"

if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        try:
            previous_count = int(f.read().strip())
        except:
            previous_count = 0
else:
    previous_count = 0

try:
    # 1. 쇼핑몰 페이지 읽어오기
    req = urllib.request.Request(shop_url, headers=custom_headers)
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    
    current_count = html.count("재입고")
    print(f"이전 기억: {previous_count}개, 현재 화면: {current_count}개")
    
    # 2. 재입고 글자 수가 늘어났다면 디스코드로 전송
    if current_count > previous_count:
        print("🚨 새로운 재입고 발견! 알림을 보냅니다.")
        message = {
            "content": f"🚨 쇼핑몰에 새로운 바지 재입고 일정이 떴습니다!\n바로가기: {shop_url}"
        }
        data = json.dumps(message).encode('utf-8')
        
        # 디스코드 전송 시에도 헤더를 넣어 차단(403) 방지
        discord_headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        discord_req = urllib.request.Request(discord_webhook_url, data=data, headers=discord_headers)
        urllib.request.urlopen(discord_req)
        print("디스코드 전송 완료!")
        
    # 3. 메모장 갱신 (에러 방지를 위해 정상 확인 시 항상 저장)
    with open(memory_file, "w") as f:
        f.write(str(current_count))
        
except Exception as e:
    print("에러 발생:", e)
    # 예외 상황에서도 빈 메모장을 만들어 Git 에러를 방지
    if not os.path.exists(memory_file):
        with open(memory_file, "w") as f:
            f.write(str(previous_count))
