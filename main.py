from telethon.sync import TelegramClient
import customtkinter as ctk

import os
import dotenv
import json

dotenv.load_dotenv()

api_id = os.environ.get("api_id")
api_hash = os.environ.get("api_hash")

client = TelegramClient("session_name", api_id, api_hash)

root = ctk.CTk()
root.title("Telegram Chat Fetcher")
root.geometry("350x200")
root.resizable(width=False, height=False)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


def run(chat_username: str):
    confirmation_label = ctk.CTkLabel(root, text="")
    confirmation_label.pack()

    if chat_username != "":
        try:
            with client:
                client.loop.run_until_complete(fetch_messages(chat_username))

            confirmation_label.configure(
                text="Operation successful", text_color="green"
            )
        except Exception as e:
            confirmation_label.configure(text=f"Error: {str(e)}", text_color="red")

            return
    else:
        confirmation_label.configure(text=f"Username cannot be empty", text_color="red")


async def fetch_messages(chat_username: str) -> None:
    messages = []

    async for message in client.iter_messages(chat_username, limit=100):
        sender = await message.get_sender()

        messages.append(
            {
                "sender_id": sender.id if sender else "Unknown",
                "sender_firstname": (
                    sender.first_name if sender and sender.first_name else "Unknown"
                ),
                "sender_lastname": (
                    sender.last_name if sender and sender.last_name else "Unknown"
                ),
                "message": message.text if message.text else "",
                "date": str(message.date),
            }
        )

    with open("messages.json", "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4, ensure_ascii=False)


username_label = ctk.CTkLabel(
    root, text="Please provide users' username (format: @abcdefg):"
)
username_label.pack()

username_entry = ctk.CTkEntry(root)
username_entry.pack()


submit = ctk.CTkButton(root, text="Submit", command=lambda: run(username_entry.get()))
submit.pack(pady=6)

root.mainloop()
