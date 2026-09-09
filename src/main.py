"""Virtual Personal Assistant - Main Application GUI.

Built using Tkinter for the Human-Computer Interaction course at the
University of West Attica (UNIWA), Department of Informatics and Computer Engineering.
"""

import os
import sys
from datetime import datetime
from random import choice
from tkinter import Tk, IntVar, NORMAL, DISABLED, END, Label, Text, Scrollbar, Entry, Button
import requests

# Handle both direct execution and package execution
try:
    from src.config import USERNAME, BOT_NAME, BG_GRAY, BG_COLOR, TEXT_COLOR, ENTRY_BG, FONT, FONT_BOLD
    from src.online_ops import (
        get_latest_news,
        get_weather_report,
        search_on_google,
        send_email,
        send_whatsapp_message,
        open_to_do_app,
        find_my_ip,
        navigate,
    )
    from src.offline_ops import open_clock, open_calendar, open_settings, open_media_player
    from src.utils import opening_text, help_text
except ImportError:
    # If running directly inside the src/ folder or via fallback
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from config import USERNAME, BOT_NAME, BG_GRAY, BG_COLOR, TEXT_COLOR, ENTRY_BG, FONT, FONT_BOLD
    from online_ops import (
        get_latest_news,
        get_weather_report,
        search_on_google,
        send_email,
        send_whatsapp_message,
        open_to_do_app,
        find_my_ip,
        navigate,
    )
    from offline_ops import open_clock, open_calendar, open_settings, open_media_player
    from utils import opening_text, help_text

user_input = ""


def greet_user() -> None:
    """Generates an initial greeting based on the current time of day."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    _insert_message(f"{greeting}. I am your virtual personal assistant. How may I assist you?", BOT_NAME)


def _insert_message(msg: str, sender: str) -> None:
    """Appends a message to the chat display widget."""
    if not msg:
        return
    user_input_entry.delete(0, END)
    formatted_msg = f"{sender}: {msg}\n\n"
    text_widget.configure(state=NORMAL)
    text_widget.insert(END, formatted_msg)
    text_widget.configure(state=DISABLED)
    text_widget.see(END)


def decider() -> None:
    """Evaluates user input and routes to the appropriate operation handler."""
    global user_input
    cmd = user_input.lower().strip()

    if not cmd:
        return

    try:
        if 'exit' in cmd or 'quit' in cmd or 'bye' in cmd:
            _insert_message("Goodbye! Have a great day!", BOT_NAME)
            root.after(800, root.destroy)
            return

        # System / Desktop automation commands
        if 'open clock' in cmd or 'clock' in cmd:
            _insert_message(choice(opening_text), BOT_NAME)
            success, status = open_clock()
            if not success:
                _insert_message(status, BOT_NAME)

        elif 'open calendar' in cmd or 'calendar' in cmd:
            _insert_message(choice(opening_text), BOT_NAME)
            success, status = open_calendar()
            if not success:
                _insert_message(status, BOT_NAME)

        elif 'open to do list' in cmd or 'todo' in cmd or 'to-do' in cmd:
            _insert_message(choice(opening_text), BOT_NAME)
            open_to_do_app()

        elif 'open settings' in cmd or 'settings' in cmd:
            _insert_message(choice(opening_text), BOT_NAME)
            success, status = open_settings()
            if not success:
                _insert_message(status, BOT_NAME)

        elif 'media player' in cmd or 'music' in cmd or 'play music' in cmd:
            _insert_message(choice(opening_text), BOT_NAME)
            success, status = open_media_player()
            if not success:
                _insert_message(status, BOT_NAME)

        # Web search
        elif 'search on google' in cmd or 'google' in cmd or 'search' in cmd:
            _insert_message("What do you want to search on Google?", BOT_NAME)
            send_button.wait_variable(var)
            query = user_input
            if query:
                search_on_google(query)
                _insert_message(f"Searching Google for: '{query}'. Check your browser.", BOT_NAME)

        # WhatsApp messaging
        elif 'whatsapp' in cmd:
            _insert_message("On what number should I send the message? (e.g. 69XXXXXXXX)", BOT_NAME)
            send_button.wait_variable(var)
            number = user_input
            _insert_message("What is your message?", BOT_NAME)
            send_button.wait_variable(var)
            message = user_input
            success, status_msg = send_whatsapp_message(number, message)
            _insert_message(status_msg, BOT_NAME)

        # News
        elif 'news' in cmd:
            _insert_message(choice(opening_text), BOT_NAME)
            _insert_message("The latest news headlines are:", BOT_NAME)
            headlines = get_latest_news()
            for item in headlines:
                _insert_message(f"• {item}", BOT_NAME)

        # Email
        elif 'email' in cmd or 'send mail' in cmd:
            _insert_message("On what email address do I send?", BOT_NAME)
            send_button.wait_variable(var)
            receiver = user_input
            _insert_message("What should be the subject?", BOT_NAME)
            send_button.wait_variable(var)
            subject = user_input
            _insert_message("What is the message?", BOT_NAME)
            send_button.wait_variable(var)
            body = user_input
            success, status_msg = send_email(receiver, subject, body)
            _insert_message(status_msg, BOT_NAME)

        # Weather
        elif 'weather' in cmd:
            _insert_message(choice(opening_text), BOT_NAME)
            ip_addr = find_my_ip()
            city = "Athens"
            try:
                res = requests.get(f"https://ipapi.co/{ip_addr}/city/", timeout=4)
                if res.status_code == 200 and res.text.strip():
                    city = res.text.strip()
            except Exception:
                pass
            _insert_message(f"Fetching weather report for {city}...", BOT_NAME)
            condition, temp, feels_like = get_weather_report(city)
            _insert_message(f"Current Temperature: {temp} (Feels like: {feels_like})", BOT_NAME)
            _insert_message(f"Forecast: {condition}", BOT_NAME)

        # Navigation & Maps
        elif 'navigate' in cmd or 'maps' in cmd or 'directions' in cmd:
            _insert_message("Where are you navigating from? (Origin)", BOT_NAME)
            send_button.wait_variable(var)
            origin = user_input
            _insert_message("Where are you navigating to? (Destination)", BOT_NAME)
            send_button.wait_variable(var)
            destination = user_input
            _insert_message("What is your travel mode? (driving, walking, bicycling, transit)", BOT_NAME)
            send_button.wait_variable(var)
            travel_mode = user_input.strip().lower() or "driving"
            navigate(origin, destination, travel_mode)
            _insert_message(f"Opening route from '{origin}' to '{destination}'. Check your browser.", BOT_NAME)

        # Online Help
        elif 'help' in cmd or 'commands' in cmd:
            _insert_message(help_text, BOT_NAME)

        else:
            _insert_message("Sorry, I didn't recognize that command. Type 'help' to see all available operations.", BOT_NAME)

    except Exception as e:
        _insert_message(f"An unexpected error occurred: {e}. Please try again.", BOT_NAME)


def process_user_input(event=None) -> None:
    """Handles submission of user input from entry box or Enter key."""
    global user_input
    var.set(1)
    user_input = user_input_entry.get().strip()
    if user_input:
        _insert_message(user_input, USERNAME)
        decider()


# Initialize Main Window
root = Tk()
var = IntVar()
root.title("Virtual Personal Assistant - UNIWA HCI")
root.resizable(width=True, height=True)
root.configure(width=1000, height=700, bg=BG_COLOR)

# Header Title Label
head_label = Label(
    root,
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    text="Virtual Personal Assistant",
    font=FONT_BOLD,
    pady=10,
)
head_label.place(relwidth=1)

# Subtle Divider Line
line = Label(root, width=450, bg=BG_GRAY)
line.place(relwidth=1, rely=0.07, relheight=0.008)

# Chat Conversation Text Widget
text_widget = Text(
    root,
    width=20,
    height=2,
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    font=FONT,
    padx=12,
    pady=12,
    wrap="word",
)
text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
text_widget.configure(cursor="arrow", state=DISABLED)

# Scrollbar for Chat Conversation
scrollbar = Scrollbar(text_widget)
scrollbar.place(relheight=1, relx=0.978)
scrollbar.configure(command=text_widget.yview)

# Bottom Input Container
bottom_label = Label(root, bg=BG_GRAY, height=80)
bottom_label.place(relwidth=1, rely=0.825)

# User Input Entry Box
user_input_entry = Entry(bottom_label, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT)
user_input_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.015)
user_input_entry.focus()
user_input_entry.bind("<Return>", process_user_input)

# Send Command Button
send_button = Button(
    bottom_label,
    text="Send",
    font=FONT_BOLD,
    width=20,
    bg=BG_GRAY,
    command=process_user_input,
)
send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.21)

greet_user()

if __name__ == '__main__':
    root.mainloop()
