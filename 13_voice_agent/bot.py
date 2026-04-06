import speech_recognition as sr
from helpers.Client import GroqClient
import threading
import subprocess

r = sr.Recognizer()
client = GroqClient().client

SYSTEM_PROMPT = """
You are an expert voice agent. If you get multi-language text, respond in the same manner.
"""

VOICE = "en-US-GuyNeural"


def run_shell_command(txt):
    subprocess.run(
        ["edge-playback", "--text", txt, "--voice", VOICE],
        capture_output=True,
        text=True
    )


with sr.Microphone() as source:
    print("🎤 Voice agent started...")

    while True:
        try:
            print("Listening...")
            audio_text = r.listen(source)

            text = r.recognize_google(audio_text)
            print("You said:", text)

            # LLM call
            res = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text},
                ]
            )

            speak_content = res.choices[0].message.content
            print("AI:", speak_content)

            # Run TTS in background
            t = threading.Thread(
                target=run_shell_command,
                args=(speak_content,)
            )
            t.start()

        except Exception as e:
            print("Error:", e)