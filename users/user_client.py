import requests

def main():
    server = "http://127.0.0.1:8000"
    topics = ["lab/gnss/DAEJ00KOR_R_20240010000_01D_30S_MO.rnx"]

    for topic in topics:
        response = requests.get(f"{server}/subscribe/{topic}")
        if response.status_code == 200:
            print(f"Subscribed to {topic}")
        else:
            print(f"Failed to subscribe to {topic}")

if __name__ == "__main__":
    main()

