# browserAI

A simple UI that uses ChatGPT to control a web browser and WeChat.

## Requirements

- Python 3.12+
- `openai`
- `itchat`
- `selenium` (optional if you only need to open URLs)

Install dependencies:

```bash
pip install openai itchat selenium
```

Set your OpenAI API key in the environment variable `OPENAI_API_KEY` and run `app.py`:

```bash
export OPENAI_API_KEY=your-key
python app.py
```

The app will ask you to scan a QR code to log in to WeChat. After login, type commands in natural language, such as "open the website https://example.com" or "send hello to Alice".
