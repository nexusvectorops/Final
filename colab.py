# ================== GOOGLE COLAB APK BUILDER ==================
# Run this cell in a fresh Colab runtime (Runtime → Run all)

!apt update
!apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Install Buildozer
!pip install buildozer cython virtualenv

# Clone your GitHub repository
!git clone https://github.com/YOUR_USERNAME/android-system-update-rat.git
%cd android-system-update-rat

# Set up Android SDK/NDK (Buildozer will download them)
!buildozer init
!cp buildozer.spec buildozer.spec.bak
# (Replace buildozer.spec with the one above if needed)

# Fix for Colab: set necessary environment variables
import os
os.environ['PATH'] += ':/root/.buildozer/android/platform/android-sdk/tools/bin'
os.environ['ANDROID_SDK_ROOT'] = '/root/.buildozer/android/platform/android-sdk'
os.environ['ANDROID_NDK_ROOT'] = '/root/.buildozer/android/platform/android-ndk'

# Build the APK (this will take 20‑40 minutes)
!buildozer android debug

# After build completes, download the APK
from google.colab import files
files.download('bin/SystemUpdate‑1.0‑debug.apk')
