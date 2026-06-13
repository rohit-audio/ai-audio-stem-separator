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

# --- STEP 1: OPEN NATIVE MAC FILE FINDER ---
root = tk.Tk()
root.withdraw()
root.call('wm', 'attributes', '.', '-topmost', True)

print("\nOpening Mac Finder window... kindly choose an audio file.")

selected_file_path = filedialog.askopenfilename(
    title="Select Your Track",
    filetypes=[("Audio Files", "*.mp3 *.wav")]
)
root.update()

if not selected_file_path:
    print("\n❌--Cancelled--❌ \nNo file selected❗\n")
    exit()

print(f"\n🎯 Selected Track: {os.path.basename(selected_file_path)}")
song_name, extension = os.path.splitext(os.path.basename(selected_file_path))

# --- STEP 2: ASK USER FOR STEM CHOICE ---
print("\nHow many stems do you want?\n")
print("  Type 4 for: drums, bass, vocals, other\n")
print("  Type 6 for: drums, bass, vocals, guitar, piano, other\n")
stem_choice = input("Your choice (4 or 6): ").strip()

if stem_choice == "4":
    model_name = "htdemucs"
    stem_names = ["drums", "bass", "other", "vocals"]
    print("\n✅ Using 4-stem model...")
elif stem_choice == "6":
    model_name = "htdemucs_6s"
    stem_names = ["drums", "bass", "other", "vocals", "guitar", "piano"]
    print("\n⌛ Note: 6-stem model may take longer to process.")
    print("\n✅ Using 6-stem model...")
else:
    print("\n❌ Invalid choice. Please type 4 or 6.\n")
    exit()

# --- STEP 3: ASK USER FOR OUTPUT FORMAT ---
print("\nIn what format do you want your output?\n")
print("  Type 1 for: WAV\n")
print("  Type 2 for: MP3\n")
format_choice = input("Your choice (1 or 2): ").strip()

if format_choice == "1":
    print("\n✅ Stems will be saved as WAV...")
elif format_choice == "2":
    print("\n✅ Stems will be saved as MP3...")
else:
    print("\n❌ Invalid choice. Please type 1 or 2.\n")
    exit()

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
    wav_path = os.path.join(desktop_path, f"{song_name}_{name}.wav")
    torchaudio.save(wav_path, stems[i], sample_rate)

    if format_choice == "2":
        mp3_path = os.path.join(desktop_path, f"{song_name}_{name}.mp3")
        AudioSegment.from_wav(wav_path).export(mp3_path, format="mp3")
        os.remove(wav_path)
        print(f"\n  ✅ Saved: {song_name}_{name}.mp3")
    else:
        print(f"\n  ✅ Saved: {song_name}_{name}.wav")

print(f"\n✨✨ Done! ✨✨\n")
print("Check your Desktop for your stem files, thanks.\n")