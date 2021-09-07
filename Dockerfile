FROM ubuntu:20.04

WORKDIR /app


ENV TZ=Asia/Kolkata
ENV DEBIAN_FRONTEND=noninteractive

RUN apt -qq update
RUN apt -qq install -y  git wget curl \
             python3 busybox unzip unrar tar \
             ffmpeg wget \
             rclone python3-pip \
             apt-transport-https gnupg  \
             coreutils jq pv mediainfo aria2
RUN python3 -m pip install --upgrade pip
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
