import requests

def check_connection(url):
    """지정된 URL로 접속을 시도하고 결과를 출력합니다."""
    print(f"--- {url} 접속 테스트 시작 ---")
    try:
        # 접속 시도 (5초 이상 걸리면 실패로 간주)
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # 200번대 상태 코드가 아니면 에러 발생
        
        print(f"✅ 성공: {url} 에 연결할 수 있습니다. (상태 코드: {response.status_code})")

    except requests.exceptions.Timeout:
        print(f"❌ 실패: {url} 접속 시간이 초과되었습니다 (Timeout).")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 실패: {url} 에 연결할 수 없습니다.")
        print("이전 로그에 나왔던 'Network is unreachable' 와 같은 종류의 문제입니다.")
        # print(f"(상세 오류: {e})") # 상세 오류 내용
        
    finally:
        print("-" * 30)
        print() # 줄 띄우기

if __name__ == "__main__":
    print("라즈베리파이에서 파이썬을 이용해 네트워크 연결을 직접 확인합니다.\n")
    
    # 1. 일반적인 인터넷 연결 확인
    check_connection('https://www.google.com')
    
    # 2. 텔레그램 봇 API 서버 연결 확인 (가장 중요)
    check_connection('https://api.telegram.org')
    
    # 3. 주식 정보 다운로드 서버 연결 확인
    check_connection('http://kind.krx.co.kr')
