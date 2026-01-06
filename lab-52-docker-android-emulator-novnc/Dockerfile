FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    openjdk-8-jdk \
    xvfb \
    x11vnc \
    websockify \
    curl \
    git \
    libxkbcommon-x11-0 \
    --no-install-recommends

# Download and install Android SDK Command Line Tools
ENV ANDROID_SDK_ROOT /opt/android-sdk
RUN mkdir -p ${ANDROID_SDK_ROOT}

RUN wget -q https://dl.google.com/android/repository/commandlinetools-linux-7302050_latest.zip -O /tmp/android-sdk.zip \
    && unzip /tmp/android-sdk.zip -d ${ANDROID_SDK_ROOT}

ENV PATH ${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin:${ANDROID_SDK_ROOT}/platform-tools:${PATH}

# Install necessary SDK components
RUN yes | sdkmanager --sdk_root=${ANDROID_SDK_ROOT} "platforms;android-30" \
    && yes | sdkmanager --sdk_root=${ANDROID_SDK_ROOT} "platform-tools" \
    && yes | sdkmanager --sdk_root=${ANDROID_SDK_ROOT} "system-images;android-30;google_apis;x86_64"

# Create and configure AVD (Android Virtual Device)
RUN avdmanager --sdk_root=${ANDROID_SDK_ROOT} create avd -n Pixel_API_30 -k "system-images;android-30;google_apis;x86_64" -f

# Expose noVNC port
EXPOSE 6080

# Start script
COPY start.sh /

CMD ["/start.sh"]