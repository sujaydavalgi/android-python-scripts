import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        city_name = input(" Enter the CITY name : ").strip()
    else:
        city_name = sys.argv[1]

    # Use curl if available, else fallback to requests
    try:
        result = subprocess.run(["curl", "-4", f"http://wttr.in/{city_name}"], capture_output=True, text=True)
        print(result.stdout)
    except Exception:
        try:
            import requests
            response = requests.get(f"http://wttr.in/{city_name}")
            print(response.text)
        except Exception as e:
            print(f"Failed to fetch weather info: {e}")

if __name__ == "__main__":
    main() 