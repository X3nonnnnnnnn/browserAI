import os
import json
import webbrowser
import itchat
import openai
from tkinter import Tk, Text, Scrollbar, Button, END, RIGHT, Y

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Please set the OPENAI_API_KEY environment variable.")
openai.api_key = OPENAI_API_KEY

# Login to WeChat (will require scanning a QR code)
itchat.auto_login(hotReload=True)

# Build simple UI
root = Tk()
root.title("Browser & WeChat Controller")

text = Text(root, height=20, width=80)
text.pack()

scroll = Scrollbar(root, command=text.yview)
scroll.pack(side=RIGHT, fill=Y)
text.config(yscrollcommand=scroll.set)

entry = Text(root, height=2, width=60)
entry.pack()


def send_command():
    user_input = entry.get("1.0", END).strip()
    if not user_input:
        return
    entry.delete("1.0", END)
    text.insert(END, f"You: {user_input}\n")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You translate user requests into JSON commands to control browser and WeChat. Output JSON only."},
            {"role": "user", "content": user_input}
        ]
    )
    reply = response.choices[0].message.content.strip()
    text.insert(END, f"ChatGPT: {reply}\n")
    try:
        data = json.loads(reply)
        action = data.get("action")
        if action == "open_url":
            url = data.get("url")
            if url:
                webbrowser.open(url)
        elif action == "wechat_send":
            user = data.get("user")
            msg = data.get("text")
            if user and msg:
                friends = itchat.search_friends(name=user)
                if friends:
                    itchat.send_msg(msg, toUserName=friends[0]["UserName"])
        else:
            text.insert(END, f"Unrecognized action: {action}\n")
    except Exception as e:
        text.insert(END, f"Error: {e}\n")


button = Button(root, text="Send", command=send_command)
button.pack()

root.mainloop()
