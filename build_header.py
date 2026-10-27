import json
import urllib.request
from datetime import date
from html import escape
from pathlib import Path

USER = "mt-panda"
CAREER_START = date(2024, 1, 1)
WIDTH = 56
THEMES = {
    "dark_mode.svg": dict(bg="#111111", text="#E6E6E6", ascii="#8B8B8B", key="#FFA500", value="#F5F5F5", dots="#4A4A4A"),
    "light_mode.svg": dict(bg="#F6F8FA", text="#24292F", ascii="#6E7781", key="#C2410C", value="#24292F", dots="#B8BEC6"),
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": USER})) as r:
        return json.load(r)


def since(start):
    today = date.today()
    months = (today.year - start.year) * 12 + today.month - start.month - (today.day < start.day)
    days = (today - date(start.year + (start.month + months - 1) // 12, (start.month + months - 1) % 12 + 1, start.day)).days
    return f"{months // 12} years, {months % 12} months, {days} days"


def row(key, value):
    parts = key.split(".")
    keys = "".join(f'<tspan class="key">{escape(k)}</tspan>{"." if i < len(parts) - 1 else ":"}' for i, k in enumerate(parts))
    dots = " " + "." * max(1, WIDTH - len(key) - len(value) - 5) + " "
    return f'<tspan class="dots">. </tspan>{keys}<tspan class="dots">{dots}</tspan><tspan class="value">{escape(value)}</tspan>'


def title(text):
    return f'{escape(text)} <tspan class="dots">{"-" * (WIDTH - len(text) - 1)}</tspan>'


user = get(f"https://api.github.com/users/{USER}")
repos = get(f"https://api.github.com/users/{USER}/repos?per_page=100")
stars = sum(r["stargazers_count"] for r in repos)

lines = [
    title("muhammad@tahir"),
    row("OS", "Windows 10, Android, iOS"),
    row("Uptime", since(CAREER_START)),
    row("Host", "Techietribe Ltd."),
    row("Kernel", "Software Engineer (MERN)"),
    row("IDE", "VS Code"),
    "",
    row("Languages.Programming", "TypeScript, JavaScript"),
    row("Languages.Computer", "HTML, CSS, SQL, JSON"),
    row("Languages.Real", "English, Urdu"),
    "",
    row("Stack.Frontend", "React, Next.js, Redux, Tailwind"),
    row("Stack.Mobile", "React Native, Expo"),
    row("Stack.Backend", "Node.js, NestJS, Express"),
    row("Stack.Data", "MongoDB, PostgreSQL, Firebase"),
    "",
    title("- Contact"),
    row("Email", "mtahirthedev@gmail.com"),
    row("Portfolio", "mtahir.tech"),
    row("LinkedIn", "m-tahir-309513342"),
    row("Location", "Lahore, Pakistan"),
    "",
    title("- GitHub Stats"),
    row("Repos", str(user["public_repos"])),
    row("Stars", str(stars)),
    row("Followers", str(user["followers"])),
]
art = Path(__file__).with_name("ascii.txt").read_text(encoding="utf-8").splitlines()

for name, c in THEMES.items():
    ascii_rows = "".join(f'<tspan x="20" y="{30 + i * 15}">{escape(l)}</tspan>' for i, l in enumerate(art))
    info_rows = "".join(f'<tspan x="450" y="{36 + i * 19.5}">{l}</tspan>' for i, l in enumerate(lines) if l)
    Path(__file__).with_name(name).write_text(f"""<svg xmlns="http://www.w3.org/2000/svg" font-family="Consolas,Menlo,'DejaVu Sans Mono',monospace" width="1000" height="540">
<style>text,tspan{{white-space:pre}}.key{{fill:{c["key"]}}}.value{{fill:{c["value"]}}}.dots{{fill:{c["dots"]}}}</style>
<rect width="1000" height="540" rx="15" fill="{c["bg"]}"/>
<text font-size="12" fill="{c["ascii"]}">{ascii_rows}</text>
<text font-size="15" fill="{c["text"]}">{info_rows}</text>
</svg>
""", encoding="utf-8")
