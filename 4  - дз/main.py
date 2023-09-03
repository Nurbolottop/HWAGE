import schedule
import time
import requests

url = ""
def perform_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        print(f"Request successful. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
def main():
    initial_delay = 10
    interval = 60
    schedule.every(initial_delay).seconds.do(perform_request, url)
    while True:
        schedule.run_pending()
        time.sleep(interval)


main()