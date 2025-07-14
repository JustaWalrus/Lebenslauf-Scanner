# Lebenslauf-Scanner
Lebenslauf-Scanner scannt Lebensläufe nach verschiedene Kriterien in der Terminal um den Auswahlprocess leichter zu machen.

## Installation
Lebenslaufscanner fordert python
### Windows
- repo clonen mit
`git clone https://github.com/JustaWalrus/Lebenslauf-Scanner.git`
- virtual environment erstellen mit
`python -m venv [venv_name]`
- anforderungen installieren mit
`git install -r requirements.txt`
- virtual environment nutzen mit `[venv_name]/Scripts/activate`
### Linux
- repo clonen mit
`git clone https://github.com/JustaWalrus/Lebenslauf-Scanner.git`
- virtual environment erstellen mit
`python -m venv [venv_name]`
- anforderungen installieren mit
`git install -r requirements.txt`
- virtual environment nutzen mit `source [venv_name]/bin/activate`

## Nutzung
mit dem virtual environment aktiviert in die Mappe, wo der Projekt drinnen liegt
`python3 ./main.py [Pfad/zum/Ordner oder Pfad/zum/File]`
um den scanner zu starten. In die "Beispiele" mappe ist bereits ein Lebenslaufmuster inkludiert.
Die Standardkriterien befinden sich im `Kriterien/Kriterien.txt` 

## Noch zu tun
- Die restliche kriterien implementieren
- Support für mehrere Sprachen
- Fehler beheben
