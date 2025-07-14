# Lebenslauf-Scanner
Lebenslauf-Scanner scannt Lebensläufe nach verschiedene Kriterien in der Terminal um den Auswahlprocess leichter zu machen.

## Installation
### Windows
### Linux
- git installieren mit
`python -m ensurepip --upgrade`
- repo clonen mit
`git clone `
- virtual environment erstellen mit
`python -m venv [name]`
- anforderungen installieren mit
`git install -r requirements.txt`

## Nutzung
mit dem virtual environment aktiviert in die Mappe, wo der Projekt drinnen liegt
`python3 ./main.py [Pfad/zum/Ordner oder Pfad/zum/File]`
um den scanner zu starten. In die "Beispiele" mappe ist bereits ein Lebenslaufmuster inkludiert.
Die Standardkriterien befinden sich im `Kriterien/Kriterien.txt` 

## Noch zu tun
- Die restliche kriterien implementieren
- Support für mehrere Sprachen
- Fehler beheben
