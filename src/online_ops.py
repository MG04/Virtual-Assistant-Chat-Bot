"""Online services and external API integrations.

Handles weather reports, news headlines, web searches, email dispatch,
WhatsApp messaging, navigation, and cloud to-do applications.
"""

import urllib.parse
import webbrowser
import requests
import smtplib
from email.message import EmailMessage

try:
    from src.config import (
        EMAIL_ADDRESS,
        EMAIL_PASSWORD,
        SMTP_SERVER,
        SMTP_PORT,
        NEWS_API_KEY,
        OPENWEATHER_APP_ID,
        NEWS_COUNTRY,
        has_email_credentials,
        has_weather_credentials,
        has_news_credentials,
    )
except ImportError:
    from config import (
        EMAIL_ADDRESS,
        EMAIL_PASSWORD,
        SMTP_SERVER,
        SMTP_PORT,
        NEWS_API_KEY,
        OPENWEATHER_APP_ID,
        NEWS_COUNTRY,
        has_email_credentials,
        has_weather_credentials,
        has_news_credentials,
    )


def find_my_ip() -> str:
    """Retrieves the public IP address of the user."""
    try:
        response = requests.get('https://api64.ipify.org?format=json', timeout=5)
        response.raise_for_status()
        return response.json().get("ip", "127.0.0.1")
    except Exception as e:
        print(f"Error resolving IP address: {e}")
        return "127.0.0.1"


def search_on_google(query: str) -> None:
    """Opens Google search with the given query in default browser."""
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.google.com/search?q={encoded_query}"
    webbrowser.open(search_url)


def send_whatsapp_message(number: str, message: str) -> tuple[bool, str]:
    """Sends a WhatsApp message via WhatsApp Web.

    Formats phone number with Greek country code (+30) by default if not specified.
    """
    clean_number = number.strip().replace(" ", "").replace("-", "")
    if not clean_number.startswith("+"):
        clean_number = f"+30{clean_number}"

    # Try pywhatkit automation if available
    try:
        import pywhatkit as kit
        import pyautogui
        import time
        from pynput import keyboard
        from pynput.keyboard import Key

        kit.sendwhatmsg_instantly(clean_number, message, wait_time=8, tab_close=False)
        time.sleep(4)
        pyautogui.click()
        time.sleep(1)
        kb = keyboard.Controller()
        kb.press(Key.enter)
        kb.release(Key.enter)
        return True, "WhatsApp message dispatched."
    except Exception as e:
        # Fallback: Open WhatsApp Web direct link in browser
        encoded_msg = urllib.parse.quote(message)
        wa_url = f"https://web.whatsapp.com/send?phone={clean_number}&text={encoded_msg}"
        webbrowser.open(wa_url)
        return True, f"Opened WhatsApp Web with message draft: {e}"


def send_email(receiver_address: str, subject: str, message: str) -> tuple[bool, str]:
    """Sends an email via secure SMTP with TLS encryption."""
    if not has_email_credentials():
        return (
            False,
            "Email credentials not configured. Please set GMAIL_ADDRESS and GMAIL_APP_PASSWORD in .env",
        )

    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL_ADDRESS
        email.set_content(message)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as s:
            s.starttls()
            s.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            s.send_message(email)
        return True, "Email sent successfully."
    except Exception as e:
        print(f"Error sending email: {e}")
        return False, f"Failed to send email: {e}"


def get_latest_news() -> list[str]:
    """Retrieves top 3 news headlines from NewsAPI."""
    if not has_news_credentials():
        return [
            "[!] NEWS_API_KEY is not configured in .env.",
            "Please obtain a free key at https://newsapi.org",
            "and add NEWS_API_KEY=your_key to your .env file.",
        ]

    try:
        url = f"https://newsapi.org/v2/top-headlines?country={NEWS_COUNTRY}&apiKey={NEWS_API_KEY}&category=general"
        res = requests.get(url, timeout=6).json()
        if res.get("status") == "ok":
            articles = res.get("articles", [])
            headlines = [a["title"] for a in articles if a.get("title")]
            return headlines[:3] if headlines else ["No current headlines found."]
        else:
            msg = res.get("message", "API request failed.")
            return [f"News API error: {msg}"]
    except Exception as e:
        return [f"Could not retrieve news headlines: {e}"]


def get_weather_report(city: str) -> tuple[str, str, str]:
    """Fetches weather conditions, temperature, and feels-like values for a city."""
    if not has_weather_credentials():
        return (
            "API Key Missing (Configure OPENWEATHER_APP_ID in .env)",
            "--",
            "--",
        )

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(city)}&appid={OPENWEATHER_APP_ID}&units=metric"
        res = requests.get(url, timeout=6).json()
        if res.get("cod") == 200:
            weather = res["weather"][0]["description"].capitalize()
            temp = f"{res['main']['temp']:.1f}°C"
            feels_like = f"{res['main']['feels_like']:.1f}°C"
            return weather, temp, feels_like
        else:
            err_msg = res.get("message", "City not found").capitalize()
            return err_msg, "--", "--"
    except Exception as e:
        return f"Error: {e}", "--", "--"


def open_to_do_app() -> None:
    """Opens Microsoft To-Do web app in browser."""
    webbrowser.open('https://todo.microsoft.com/tasks/')


def navigate(origin: str, destination: str, travel_mode: str = "driving") -> None:
    """Opens Google Maps route directions in browser."""
    origin_enc = urllib.parse.quote(origin)
    dest_enc = urllib.parse.quote(destination)
    mode_enc = urllib.parse.quote(travel_mode)
    url = f"https://www.google.com/maps/dir/?api=1&origin={origin_enc}&destination={dest_enc}&travelmode={mode_enc}"
    webbrowser.open(url)
