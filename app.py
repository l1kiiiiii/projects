import tkinter as tk
from tkinter import messagebox
import pyaudio
import speech_recognition as sr
import threading
import winsound  # For playing the buzzer sound on Windows

# Initialize the speech recognizer
recognizer = sr.Recognizer()

class SpeechRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("INTONE CHANT")
        self.root.geometry("400x300")  # Set window size

        self.target_sentence = tk.StringVar(value="hello")
        self.match_count = tk.IntVar(value=0)
        self.match_limit = tk.IntVar(value=2)  # Default limit to 2 matches
        self.processing = False

        self.create_widgets()

    def create_widgets(self):
        # Frame for styling
        self.frame = tk.Frame(self.root, bg="lightblue") 
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.sentence_label = tk.Label(self.frame, text="Target Sentence:", font=("Helvetica", 14), bg="lightblue")
        self.sentence_label.pack(pady=5)

        self.sentence_entry = tk.Entry(self.frame, textvariable=self.target_sentence, font=("Helvetica", 14), width=30)
        self.sentence_entry.pack(pady=5)

        self.count_label = tk.Label(self.frame, text="Match Count:", font=("Helvetica", 14), bg="lightblue")
        self.count_label.pack(pady=5)

        self.count_value = tk.Label(self.frame, textvariable=self.match_count, font=("Helvetica", 14), bg="lightblue")
        self.count_value.pack(pady=5)

        self.limit_label = tk.Label(self.frame, text="Match Limit:", font=("Helvetica", 14), bg="lightblue")
        self.limit_label.pack(pady=5)

        self.limit_entry = tk.Entry(self.frame, textvariable=self.match_limit, font=("Helvetica", 14), width=30)
        self.limit_entry.pack(pady=5)

        self.control_button = tk.Button(self.frame, text="Start Listening", font=("Helvetica", 14), bg="green", fg="white", command=self.toggle_listening)
        self.control_button.pack(pady=10)

    def toggle_listening(self):
        if self.processing:
            self.processing = False
            self.control_button.config(text="Start Listening", bg="green")
        else:
            self.processing = True
            self.match_count.set(0)
            self.control_button.config(text="Stop Listening", bg="red")
            self.audio_thread = threading.Thread(target=self.process_audio_stream)
            self.audio_thread.start()

    def process_audio_stream(self):
        with sr.Microphone() as source:
            while self.processing:
                try:
                    audio = recognizer.listen(source, timeout=3)
                    transcription = recognizer.recognize_google(audio)
                    print(f"Transcription: {transcription}")

                    if self.target_sentence.get().lower() in transcription.lower():
                        self.match_count.set(self.match_count.get() + 1)
                        print(f"Match count: {self.match_count.get()}")

                        if self.match_count.get() >= self.match_limit.get():
                            self.trigger_alarm()
                            self.processing = False
                            self.control_button.config(text="Start Listening", bg="green")

                except sr.WaitTimeoutError:
                    print("Listening timed out while waiting for phrase to start")
                except sr.UnknownValueError:
                    print("Could not understand the audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                    messagebox.showerror("Error", f"Could not request results from Google Speech Recognition service; {e}")
                    self.processing = False
                    self.control_button.config(text="Start Listening")

    def trigger_alarm(self):
        # Play a beep sound
        winsound.Beep(950, 1000)  # Frequency 1000 Hz, Duration 1000 ms
        messagebox.showinfo("Limit Reached", "The match limit has been reached.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechRecognitionApp(root)
    root.mainloop()