#!/bin/bash

echo "Checking required libraries..."

pip3 show demucs > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing required libraries..."
    pip3 install demucs torchaudio torch
else
    echo "✅ Libraries already installed..."
fi

echo "Launching AI Audio Stem Separator..."
python3 stem_sep.py