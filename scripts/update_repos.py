import json
import os
import urllib.request
from pathlib import Path

# GitHub obtiene automáticamente el usuario propietario del repositorio
username = os.environ.get("GITHUB_REPOSITORY_OWNER", "s0k1x")
token = os.environ.get("GITHUB_TOKEN", "")

readme_path = Path("README.md")

url = (
    f"https://api.github.com/users/{username}"
    "/repos?per_page=100&sort=updated&type=owner"
)

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "s0k1x-profile-updater",
}

if token:
    headers["Authorization"] = f"Bearer {token}"

request = urllib.request.Request(url, headers=headers)

with urllib.request.urlopen(request, timeout=30) as response:
    repos = json.load(response)

# Mostrar únicamente repositorios públicos
repos = [
    repo for repo in repos
    if not repo.get("private", False)
]

# Ordenar por nombre
repos.sort(key=lambda repo: repo["name"].lower())

buttons = []

for repo in repos:
    name = repo["name"]
    link = repo["html_url"]

    # Preparar el nombre para la URL de Shields.io
    badge_name = (
        name.replace("-", "--")
        .replace("_", "__")
        .replace(" ", "%20")
    )

    badge_url = (
        f"https://img.shields.io/badge/"
        f"{badge_name}-VIEW-00ff41"
        "?style=for-the-badge&labelColor=050505"
    )

    button = (
        f'<a href="{link}">'
        f'<img src="{badge_url}" alt="{name}" />'
        f'</a>'
    )

    buttons.append(button)

# Crear el bloque de botones
if buttons:
    content = (
        '<div align="center">\n\n'
        + "\n".join(buttons)
        + '\n\n</div>'
    )
else:
    content = "_No public repositories found yet._"

# Leer README
readme = readme_path.read_text(encoding="utf-8")

start_marker = "<!-- REPOS-START -->"
end_marker = "<!-- REPOS-END -->"

if start_marker not in readme or end_marker not in readme:
    raise SystemExit(
        "ERROR: No se encontraron los marcadores "
        "REPOS-START y REPOS-END en README.md"
    )

before, rest = readme.split(start_marker, 1)
_, after = rest.split(end_marker, 1)

updated_readme = (
    before
    + start_marker
    + "\n\n"
    + content
    + "\n\n"
    + end_marker
    + after
)

readme_path.write_text(
    updated_readme,
    encoding="utf-8"
)

print(f"Actualizados {len(repos)} repositorios públicos.")