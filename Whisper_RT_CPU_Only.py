import pyaudio
import wave
import numpy as np
import whisper
import time
import queue
import threading
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def get_unique_devices(p):
    devices = {}
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev['name'] not in devices:
            devices[dev['name']] = i
    return devices

def save_microphone_index(mic_index):
    with open("microphones_setting.txt", "w") as f:
        f.write(str(mic_index))

def load_microphone_index():
    if not os.path.exists("microphones_setting.txt"):
        return None

    with open("microphones_setting.txt", "r") as f:
        mic_index = int(f.read())
    return mic_index

def record_audio(threshold, audio_queue):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    while True:
        frames = []
        silent_frames = 0
        recording_started = False

        while True:
            audio_data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
            if np.abs(audio_data).mean() < threshold:
                silent_frames += 1
            else:
                silent_frames = 0
                if not recording_started:
                    recording_started = True
            if recording_started:
                frames.append(audio_data)
            if silent_frames > 0.6 * RATE / CHUNK:  # stop recording after 0.5 seconds of silence
                if recording_started:
                    break

        # save the recorded audio to a file
        filename = f"output_{int(time.time())}.wav"   # Change the file extension here (wav or mp3)
        wf = wave.open(filename, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        audio_queue.put(filename)

def process_audio_queue(audio_queue, language):
    model = whisper.load_model("tiny")
    print(f"Language set to [{language if language != 'auto' else 'auto-detect'}] Please give a minute to load the model")  # show the model is working and language it selects
    while True:
        if not audio_queue.empty():
            audio_file = audio_queue.get()
            try:
                result = model.transcribe(audio_file, language=language if language != "auto" else None)  # Handle the "auto" option
                print(result["text"])
            except RuntimeError as e:
                print(f"Error processing audio file {audio_file}: {e}")
            except Exception as e:
                print(f"Unexpected error processing audio file {audio_file}: {e}")
            finally:
                try:
                    os.remove(audio_file)
                except Exception as e:
                    print(f"Error removing audio file {audio_file}: {e}")


def measure_threshold():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Please be quiet for 5 seconds while we measure the background noise...")

    frames = []
    for i in range(0, int(RATE / CHUNK * 5)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Please speak for 5 seconds...")

    frames2 = []
    for i in range(0, int(RATE / CHUNK * 5)):
        data = stream.read(CHUNK)
        frames2.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
    background = np.abs(audio_data).mean()
    print(f"Background noise set to {background}")

    audio_data = np.frombuffer(b''.join(frames2), dtype=np.int16)
    speech = np.abs(audio_data).mean()
    print(f"Speech volume set to {speech}")

    threshold = (background + speech) / 2
    print(f"Threshold set to {threshold}")

    return threshold


def save_threshold(threshold):
    with open("threshold.txt", "w") as f:
        f.write(str(threshold))

def load_threshold():
    if not os.path.exists("threshold.txt"):
        return None

    with open("threshold.txt", "r") as f:
        threshold = float(f.read())
    return threshold

def choose_threshold():
    while True:
        print("Choose an option to set the threshold:")
        print("0. Use old calibration number")
        print("1. Start calibration")
        print("2. Type in threshold")

        try:
            choice = int(input("Enter the number of the option you want to use: "))
            if choice == 1:
                threshold = measure_threshold()
                save_threshold(threshold)
                break
            elif choice == 0:
                old_calibration = load_threshold()
                if old_calibration is None:
                    print("No previous calibration found. Starting calibration...")
                    threshold = measure_threshold()
                    save_threshold(threshold)
                else:
                    threshold = old_calibration
                break
            elif choice == 2:
                while True:
                    try:
                        custom_threshold = float(input("Enter the threshold value: "))
                        threshold = custom_threshold
                        break
                    except ValueError:
                        print("Wrong option, please enter again.")
                break  # Add this line to break the loop after setting a custom threshold value
            else:
                print("Wrong option, please enter again.")
        except ValueError:
            print("Wrong option, please enter again.")
    return threshold


def save_language(language):
    with open("language_settings.txt", "w") as f:
        if language is None:
            f.write('')
        else:
            f.write(language)

def load_language():
    if not os.path.exists("language_settings.txt"):
        return None

    with open("language_settings.txt", "r") as f:
        language = f.read().strip()
    return language

def choose_language():
    # Define the supported_languages list at the beginning of the function
    supported_languages = [
        "auto",  # Changed from None to "auto"
        "af", "ar", "hy", "az", "bs", "bg", "ca", "zh", "hr", "cs", "da", "nl", "en", "et", "fi", "fr", "gl", "de",
        "el", "he", "hi", "hu", "is", "id", "it", "ja", "kn", "kk", "ko", "lv", "lt", "mk", "ms", "mi", "mr", "ne",
        "no", "fa", "pl", "pt", "ro", "ru", "sr", "sk", "sl", "es", "sw", "sv", "tl", "ta", "th", "uk", "ur", "vi",
        "cy"
    ]

    # Define the language_names list
    language_names = [
        "Last selection", "Auto detect", "Afrikaans", "Arabic", "Armenian", "Azerbaijani", "Bosnian", "Bulgarian",
        "Catalan", "Chinese", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Finnish", "French",
        "Galician", "German", "Greek", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian",
        "Japanese", "Kannada", "Kazakh", "Korean", "Latvian", "Lithuanian", "Macedonian", "Malay", "Maori", "Marathi",
        "Nepali", "Norwegian", "Persian", "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak",
        "Slovenian", "Spanish", "Swahili", "Swedish", "Tagalog", "Tamil", "Thai", "Ukrainian", "Urdu", "Vietnamese",
        "Welsh"
    ]

    while True:
        print("Choose the input language:")
        for i, lang in enumerate(language_names):
            print(f"{i}. {lang}")

        try:
            choice = int(input("Enter the number of the language you want to use: "))
            if choice == 0:
                last_language = load_language()
                if last_language is None:
                    print("No previous language selection found. Please choose a language.")
                else:
                    language = last_language
                    break
            elif 1 <= choice < len(language_names):
                language = supported_languages[choice - 1]
                save_language(language)  # Save the selected language to settings.txt
                break
            else:
                print("Wrong option, please enter again.")
        except ValueError:
            print("Wrong option, please enter again.")
    return language


if __name__ == "__main__":
    print("Available microphones:")
    p = pyaudio.PyAudio()
    unique_devices = get_unique_devices(p)
    print("0. Use previous microphone")
    for name, index in unique_devices.items():
        print(f"{index + 1}: {name}")  # Add 1 to the index displayed
    p.terminate()

    while True:
        try:
            mic_index_input = int(input("Enter the number of the microphone you want to use: "))
            if mic_index_input == 0:
                last_mic_index = load_microphone_index()
                if last_mic_index is None:
                    print("No previous microphone selection found. Please choose a microphone.")
                else:
                    mic_index = last_mic_index
                    break
            elif mic_index_input - 1 in unique_devices.values():  # Subtract 1 from the input
                mic_index = mic_index_input - 1  # Subtract 1 from the input to get the actual index
                save_microphone_index(mic_index)
                break
            else:
                print("Wrong option, please enter again.")
        except ValueError:
            print("Wrong option, please enter again.")

    threshold = choose_threshold()
    language = choose_language()

    audio_queue = queue.Queue(maxsize=0)

    record_thread = threading.Thread(target=record_audio, args=(threshold, audio_queue))
    process_thread = threading.Thread(target=process_audio_queue, args=(audio_queue, language))

    record_thread.start()
    process_thread.start()

    record_thread.join()
    process_thread.join()
