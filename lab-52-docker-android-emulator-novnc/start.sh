#!/bin/bash

export ANDROID_SDK_ROOT=/opt/android-sdk
export PATH=$ANDROID_SDK_ROOT/platform-tools:$PATH

# Start the Android emulator in the background
emulator -avd Pixel_API_30 -no-window -no-audio -camera-back none -gpu swiftshader &

# Wait for the emulator to start
sleep 30

# Start x11vnc
x11vnc -display :0 -nopw -listen 0.0.0.0 -forever &

# Start noVNC
websockify -v --web=/usr/share/novnc 6080 localhost:5900