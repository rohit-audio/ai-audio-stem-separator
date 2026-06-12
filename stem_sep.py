import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
import warnings
warnings.filterwarnings('ignore')
import tkinter as tk
from tkinter import filedialog
import torchaudio
import torch
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
print("  Type 4 for: drums, bass, vocals, other \n")
print("  Type 6 for: drums, bass, vocals, guitar, piano, other\n")
stem_choice = input("Your choice (4 or 6): ").strip()

if stem_choice == "4":
    model_name = "htdemucs"
    stem_names = ["drums", "bass", "other", "vocals"]
    print("\n✅ Using 4-stem model...")
elif stem_choice == "6":
    model_name = "htdemucs_6s"
    stem_names = ["drums", "bass", "other", "vocals", "guitar", "piano"]
    print("\n⌛ Note: Type 6 may take longer time to process.")
    print("\n✅ Using 6-stem model...\n")

else:
    print("\n❌ Invalid choice. Please type 4 or 6.\n")
    exit()

# --- STEP 3: RUN META'S DEMUCS AI ---
print(f"Initializing Meta Demucs {stem_choice}-Stem AI Engine...")
model = pretrained.get_model(model_name)

print("Loading audio...")
waveform, sample_rate = torchaudio.load(selected_file_path)

print("\n🔁 AI is splitting the track... (this may take a few minutes ⌛)\n")
with torch.no_grad():
    stems = apply_model(model, waveform[None])[0]

# --- STEP 4: SAVE EACH STEM AS A SEPARATE FILE ON DESKTOP ---
desktop_path = os.path.expanduser("~/Desktop")

print("Saving individual stems to Desktop...")

for i, name in enumerate(stem_names):
    output_path = os.path.join(desktop_path, f"{song_name}_{name}.wav")
    torchaudio.save(output_path, stems[i], sample_rate)
    print(f" \n ✅ Saved: {song_name}_{name}.wav")

print(f"\n ✨✨ Done! ✨✨\n")
print("Check your Desktop for your stem files, thanks.\n")