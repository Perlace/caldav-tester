# CalDAV Tester

App web simple pour tester des connexions CalDAV et visualiser des calendriers.

## Prérequis

- Python 3.8+

## Installation

```bash
git clone https://github.com/Perlace/caldav-tester.git
cd caldav-tester
python3 -m venv .venv
source .venv/bin/activate
pip install flask caldav icalendar
```

> Sur Windows : `.venv\Scripts\activate` à la place de `source .venv/bin/activate`

## Lancement

```bash
source .venv/bin/activate
python app.py
```

L'app est accessible sur **http://localhost:5588**

## Utilisation

1. Renseigner l'URL CalDAV, le nom d'utilisateur et le mot de passe
2. Cliquer sur **Se connecter**
3. Cliquer sur un calendrier pour voir ses événements
4. Choisir la période souhaitée

## Exemples d'URL CalDAV

| Serveur | URL |
|---------|-----|
| cPanel / Horde | `https://mail.domaine.com:2083/caldav/` |
| Roundcube | `https://mail.domaine.com/caldav/user@domaine.com/` |
| Nextcloud | `https://cloud.domaine.com/remote.php/dav/calendars/user/` |
| Google | `https://www.google.com/calendar/dav/user@gmail.com/events/` |
| iCloud | `https://caldav.icloud.com/` |

## Dépannage

Si `python3 -m venv` échoue sur Ubuntu/Debian :
```bash
sudo apt install python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
pip install flask caldav icalendar
python app.py
```
