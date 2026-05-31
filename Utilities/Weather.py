import os
import csv
from datetime import datetime
import requests

FILENAME = "weather_data.csv"
API_KEY = ""


def initialize_csv():
    """Create CSV file with headers if it doesn't exist or is empty."""
    if not os.path.exists(FILENAME) or os.path.getsize(FILENAME) == 0:
        with open(FILENAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["City", "Temperature", "Description", "Date"])


def log_weather():
    city = input("Enter city name: ").strip()

    if not city:
        print("City name cannot be empty.")
        return

    today = datetime.now().strftime("%Y-%m-%d")

    
    try:
        with open(FILENAME, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

           
            if reader.fieldnames:
                for row in reader:
                    if not row.get("City") or not row.get("Date"):
                        continue

                    logged_date = row["Date"][:10]

                    if (
                        row["City"].lower() == city.lower()
                        and logged_date == today
                    ):
                        print(
                            f"Weather for {city.title()} has already been logged today."
                        )
                        return
    except FileNotFoundError:
        initialize_csv()

    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            print(f"API Error: {data.get('message', 'Unknown error')}")
            return

        temperature = data["main"]["temp"]
        description = data["weather"][0]["main"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(FILENAME, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    city.title(),
                    temperature,
                    description,
                    timestamp,
                ]
            )

        print(
            f"\nLogged Successfully!"
            f"\nCity: {city.title()}"
            f"\nTemperature: {temperature}°C"
            f"\nCondition: {description}"
            f"\nTime: {timestamp}\n"
        )

    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")

    except Exception as e:
        print(f"Unexpected Error: {e}")

def view_logs():
    with open(FILENAME, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        if len(reader) == 0:
            print("No weather data logged yet.")
            return
        for row in reader:
            print(
                f"City: {row['City']}, "
                f"Temperature: {row['Temperature']}°C, "
                f"Condition: {row['Description']}, "
                f"Logged At: {row['Date']}"
            )
        

def main():
    initialize_csv()

    while True:
        print("\n===== Real-Time Weather Logger =====")
        print("1. Log Weather Data")
        print("2. Exit")

        choice = input("Choose an option: ").strip()

        match choice:
            case "1":
                log_weather()

            case "2":
                print("Goodbye!")
                break

            case _:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
