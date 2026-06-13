import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
import warnings
warnings.filterwarnings('ignore')
import tkinter as tk
from tkinter import filedialog
import torchaudio
import torch
from pydub import AudioSegment
from demucs import pretrained
from demucs.apply import apply_model

def is_inaudible(audio_tensor, threshold=0.001):
    return audio_tensor.numpy().__abs__().mean() < threshold

# --- STEP 1: OPEN NATIVE MAC FILE FINDER ---
root = tk.Tk()
root.withdraw()
root.call('wm', 'attributes', '.', '-topmost', True)

print("\nOpening Mac Finder window... kindly choose an audio file.")

# Keep asking until a file is selected or user cancels twice
attempts = 0
while attempts < 2:
    selected_file_path = filedialog.askopenfilename(
        title="Select Your Track",
        filetypes=[("Audio Files", "*.mp3 *.wav")]
    )
    root.update()
    
    if selected_file_path:
        break  # file selected, exit the loop
    
    attempts += 1
    if attempts < 2:
        print("\n⚠️ No file selected. One more chance — please choose an audio file.\n")
    else:
        print("\n❌--Cancelled--❌ \nNo file selected❗\n")
        exit()

print(f"\n🎯 Selected Track: {os.path.basename(selected_file_path)}")
song_name, extension = os.path.splitext(os.path.basename(selected_file_path))

# --- STEP 2: ASK USER FOR STEM CHOICE ---
print("\nHow many stems do you want?\n")
print("  Type 4 for: percussion, bass, vocals, other\n")
print("  Type 6 for: percussion, bass, vocals, guitar/strings, piano, other\n")

stem_choice = input("Your choice (4 or 6): ").strip()

if stem_choice not in ["4", "6"]:
    print("\n⚠️ Incorrect input. One more chance — please type 4 or 6.\n")
    stem_choice = input("Your choice (4 or 6): ").strip()
    if stem_choice not in ["4", "6"]:
        print("\n❌ Incorrect input again. Exiting.\n")
        exit()

if stem_choice == "4":
    model_name = "htdemucs"
    stem_names = ["percussion", "bass", "other", "vocals"]
    print("\n✅ Using 4-stem model...")
elif stem_choice == "6":
    model_name = "htdemucs_6s"
    stem_names = ["percussion", "bass", "other", "vocals", "guitar_strings", "piano"]
    print("\n⌛ Note: 6-stem model may take longer to process.")
    print("\n✅ Using 6-stem model...")


# --- STEP 3: ASK USER FOR OUTPUT FORMAT ---
print("\nIn what format do you want your output?\n")
print("  Type 1 for: WAV\n")
print("  Type 2 for: MP3\n")

format_choice = input("Your choice (1 or 2): ").strip()

if format_choice not in ["1", "2"]:
    print("\n⚠️ Incorrect input. One more chance — please type 1 or 2.\n")
    format_choice = input("Your choice (1 or 2): ").strip()
    if format_choice not in ["1", "2"]:
        print("\n❌ Incorrect input again. Exiting.\n")
        exit()

if format_choice == "1":
    print("\n✅ Stems will be saved as WAV...")
elif format_choice == "2":
    print("\n✅ Stems will be saved as MP3...")

# --- STEP 4: RUN META'S DEMUCS AI ---
print(f"\nInitializing Meta Demucs {stem_choice}-Stem AI Engine...")
model = pretrained.get_model(model_name)

print("Loading audio...")
waveform, sample_rate = torchaudio.load(selected_file_path)

print("\n🔁 AI is splitting the track... (this may take a few minutes ⌛)\n")
with torch.no_grad():
    stems = apply_model(model, waveform[None])[0]

# --- STEP 5: SAVE STEMS ---
desktop_path = os.path.expanduser("~/Desktop")
print("Saving individual stems to Desktop...")

for i, name in enumerate(stem_names):
    if name != "other" and is_inaudible(stems[i]):
        prefix = "(Inaudible)_"
    else:
        prefix = ""

    wav_path = os.path.join(desktop_path, f"{prefix}{song_name}_{name}.wav")
    torchaudio.save(wav_path, stems[i], sample_rate)

    if format_choice == "2":
        mp3_path = os.path.join(desktop_path, f"{prefix}{song_name}_{name}.mp3")
        AudioSegment.from_wav(wav_path).export(mp3_path, format="mp3")
        os.remove(wav_path)
        print(f"\n  ✅ Saved: {prefix}{song_name}_{name}.mp3")
    else:
        print(f"\n  ✅ Saved: {prefix}{song_name}_{name}.wav")

print(f"\n✨✨ Done! ✨✨\n")
print("Check your Desktop for your stem files, thanks.\n")