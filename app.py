#!/usr/bin/env python3
"""CalDAV Tester — Outil de test calendriers o2switch."""

from flask import Flask, request, jsonify, Response
from datetime import datetime, timedelta
import json

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CalDAV Tester</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', sans-serif; background: #0d1117; color: #e6edf3; min-height: 100vh; }
  header { background: linear-gradient(135deg, #0B3D5C, #0e5a8a); padding: 16px 24px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 8px #0005; }
  header h1 { font-size: 1.2rem; font-weight: 600; }
  header span { font-size: 1.4rem; }
  .container { max-width: 1100px; margin: 0 auto; padding: 24px; }

  .card { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 20px; margin-bottom: 20px; }
  .card h2 { font-size: 0.95rem; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 16px; }

  .form-row { display: flex; gap: 10px; flex-wrap: wrap; align-items: flex-end; }
  .form-group { display: flex; flex-direction: column; gap: 5px; flex: 1; min-width: 180px; }
  label { font-size: 0.8rem; color: #8b949e; }
  input { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 8px 12px; color: #e6edf3; font-size: 0.9rem; outline: none; transition: border-color 0.2s; }
  input:focus { border-color: #1f6feb; }
  input::placeholder { color: #484f58; }

  button { background: #1f6feb; color: #fff; border: none; border-radius: 6px; padding: 9px 18px; cursor: pointer; font-size: 0.9rem; font-weight: 500; transition: background 0.2s; white-space: nowrap; }
  button:hover { background: #388bfd; }
  button.secondary { background: #21262d; border: 1px solid #30363d; }
  button.secondary:hover { background: #30363d; }
  button:disabled { opacity: 0.5; cursor: not-allowed; }

  .status { padding: 8px 14px; border-radius: 6px; font-size: 0.85rem; display: none; }
  .status.ok { background: #0d3321; border: 1px solid #238636; color: #3fb950; display: block; }
  .status.err { background: #3d0f0f; border: 1px solid #f85149; color: #f85149; display: block; }
  .status.info { background: #1c2a3a; border: 1px solid #1f6feb; color: #79c0ff; display: block; }

  .calendars { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 10px; }
  .cal-card { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 14px; cursor: pointer; transition: all 0.2s; }
  .cal-card:hover { border-color: #1f6feb; background: #161b22; }
  .cal-card.active { border-color: #1f6feb; background: #1c2a3a; }
  .cal-name { font-weight: 600; font-size: 0.95rem; margin-bottom: 4px; }
  .cal-url { font-size: 0.7rem; color: #484f58; word-break: break-all; }
  .cal-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 8px; }

  .period-row { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; margin-bottom: 16px; }
  .period-row label { font-size: 0.85rem; color: #8b949e; }

  table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
  th { text-align: left; padding: 10px 12px; border-bottom: 1px solid #30363d; color: #8b949e; font-weight: 500; font-size: 0.8rem; text-transform: uppercase; }
  td { padding: 10px 12px; border-bottom: 1px solid #21262d; vertical-align: top; }
  tr:hover td { background: #1c2128; }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 500; }
  .badge-blue { background: #1c2a3a; color: #79c0ff; }
  .badge-green { background: #0d3321; color: #3fb950; }
  .empty { text-align: center; padding: 40px; color: #484f58; }
  .spinner { display: inline-block; width: 14px; height: 14px; border: 2px solid #30363d; border-top-color: #1f6feb; border-radius: 50%; animation: spin 0.7s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
  .loader { text-align: center; padding: 30px; color: #8b949e; }
</style>
</head>
<body>
<header>
  <span>📅</span>
  <h1>CalDAV Tester</h1>
</header>
<div class="container">

  <!-- Connexion -->
  <div class="card">
    <h2>Connexion</h2>
    <div class="form-row">
      <div class="form-group" style="flex:2; min-width:280px;">
        <label>URL CalDAV</label>
        <input id="url" type="text" placeholder="https://serveur/caldav/user@domain.com/" />
      </div>
      <div class="form-group">
        <label>Utilisateur</label>
        <input id="user" type="text" placeholder="user@domain.com" />
      </div>
      <div class="form-group">
        <label>Mot de passe</label>
        <input id="pass" type="password" placeholder="••••••••" />
      </div>
      <button id="btn-connect" onclick="connect()">Se connecter</button>
    </div>
    <div style="margin-top:12px;">
      <div id="status" class="status"></div>
    </div>
  </div>

  <!-- Calendriers -->
  <div class="card" id="section-cals" style="display:none;">
    <h2>Calendriers disponibles</h2>
    <div id="calendars" class="calendars"></div>
  </div>

  <!-- Événements -->
  <div class="card" id="section-events" style="display:none;">
    <h2 id="events-title">Événements</h2>
    <div class="period-row">
      <label>Du</label>
      <input id="date-start" type="date" style="width:150px;" />
      <label>au</label>
      <input id="date-end" type="date" style="width:150px;" />
      <button onclick="loadEvents()">Actualiser</button>
    </div>
    <div id="events-container"></div>
  </div>

</div>

<script>
let creds = null;
let activeCal = null;
const COLORS = ['#58a6ff','#3fb950','#f78166','#d2a8ff','#ffa657','#79c0ff','#ff7b72'];

function setStatus(msg, type) {
  const s = document.getElementById('status');
  s.textContent = msg;
  s.className = 'status ' + type;
}

async function api(path, body) {
  const r = await fetch(path, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body)
  });
  return r.json();
}

async function connect() {
  const url = document.getElementById('url').value.trim();
  const user = document.getElementById('user').value.trim();
  const pass = document.getElementById('pass').value;
  if (!url || !user || !pass) { setStatus('Tous les champs sont requis.', 'err'); return; }

  const btn = document.getElementById('btn-connect');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>';
  setStatus('Connexion en cours...', 'info');

  const res = await api('/api/connect', {url, user, pass});
  btn.disabled = false;
  btn.textContent = 'Se connecter';

  if (res.error) { setStatus('Erreur : ' + res.error, 'err'); return; }

  creds = {url, user, pass};
  setStatus(`Connecté — ${res.calendars.length} calendrier(s) trouvé(s)`, 'ok');

  const div = document.getElementById('calendars');
  div.innerHTML = '';
  res.calendars.forEach((cal, i) => {
    const color = COLORS[i % COLORS.length];
    const card = document.createElement('div');
    card.className = 'cal-card';
    card.innerHTML = `<div class="cal-name"><span class="cal-dot" style="background:${color}"></span>${cal.name}</div><div class="cal-url">${cal.url}</div>`;
    card.onclick = () => selectCal(cal, color, card);
    div.appendChild(card);
  });

  document.getElementById('section-cals').style.display = '';

  // Période par défaut : mois courant
  const now = new Date();
  const y = now.getFullYear(), m = now.getMonth();
  document.getElementById('date-start').value = new Date(y, m, 1).toISOString().slice(0,10);
  document.getElementById('date-end').value = new Date(y, m+1, 0).toISOString().slice(0,10);
}

function selectCal(cal, color, card) {
  document.querySelectorAll('.cal-card').forEach(c => c.classList.remove('active'));
  card.classList.add('active');
  activeCal = cal;
  document.getElementById('events-title').innerHTML = `<span class="cal-dot" style="background:${color}"></span>${cal.name}`;
  document.getElementById('section-events').style.display = '';
  loadEvents();
}

async function loadEvents() {
  if (!activeCal || !creds) return;
  const start = document.getElementById('date-start').value;
  const end = document.getElementById('date-end').value;
  if (!start || !end) return;

  const container = document.getElementById('events-container');
  container.innerHTML = '<div class="loader"><span class="spinner"></span> Chargement...</div>';

  const res = await api('/api/events', {...creds, cal_url: activeCal.url, start, end});

  if (res.error) { container.innerHTML = `<div class="empty">Erreur : ${res.error}</div>`; return; }
  if (!res.events.length) { container.innerHTML = '<div class="empty">Aucun événement sur cette période.</div>'; return; }

  const rows = res.events.map(e => {
    const start = e.start ? fmtDate(e.start) : '—';
    const end = e.end ? fmtDate(e.end) : '—';
    const allday = e.allday ? '<span class="badge badge-green">Journée</span>' : '';
    const recur = e.recurrent ? '<span class="badge badge-blue">Récurrent</span>' : '';
    return `<tr>
      <td>${start}</td>
      <td>${end}</td>
      <td><strong>${esc(e.summary || '(sans titre)')}</strong>${e.location ? '<br><small style="color:#8b949e">📍 '+esc(e.location)+'</small>' : ''}</td>
      <td>${allday}${recur}</td>
      <td style="color:#8b949e;font-size:0.8rem;">${esc(e.uid || '').slice(0,20)}...</td>
    </tr>`;
  }).join('');

  container.innerHTML = `
    <p style="color:#8b949e;font-size:0.82rem;margin-bottom:12px;">${res.events.length} événement(s)</p>
    <table>
      <thead><tr><th>Début</th><th>Fin</th><th>Titre / Lieu</th><th>Tags</th><th>UID</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>`;
}

function fmtDate(s) {
  if (!s) return '—';
  if (s.length === 8) return s.slice(6,8)+'/'+s.slice(4,6)+'/'+s.slice(0,4);
  try {
    const d = new Date(s);
    return d.toLocaleDateString('fr-FR') + ' ' + d.toLocaleTimeString('fr-FR', {hour:'2-digit',minute:'2-digit'});
  } catch { return s; }
}
function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")


@app.route("/api/connect", methods=["POST"])
def api_connect():
    try:
        import caldav
    except ImportError:
        return jsonify({"error": "Module 'caldav' non installé. Lancer : pip install caldav"})

    data = request.json
    url, user, pwd = data.get("url",""), data.get("user",""), data.get("pass","")
    try:
        client = caldav.DAVClient(url=url, username=user, password=pwd)
        principal = client.principal()
        cals = principal.calendars()
        result = []
        for c in cals:
            try:
                name = str(c.name) if c.name else c.url.path.split("/")[-2]
            except Exception:
                name = str(c.url)
            result.append({"name": name, "url": str(c.url)})
        return jsonify({"calendars": result})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/api/events", methods=["POST"])
def api_events():
    try:
        import caldav
        from icalendar import Calendar
    except ImportError:
        return jsonify({"error": "Modules manquants. Lancer : pip install caldav icalendar"})

    data = request.json
    url, user, pwd = data.get("url",""), data.get("user",""), data.get("pass","")
    cal_url = data.get("cal_url","")
    start_str = data.get("start","")
    end_str = data.get("end","")

    try:
        from datetime import datetime
        start_dt = datetime.strptime(start_str, "%Y-%m-%d")
        end_dt = datetime.strptime(end_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

        client = caldav.DAVClient(url=url, username=user, password=pwd)
        # Récupérer le calendrier via le principal pour éviter les 404
        principal = client.principal()
        cal = None
        for c in principal.calendars():
            if str(c.url) == cal_url or str(c.url).rstrip("/") == cal_url.rstrip("/"):
                cal = c
                break
        if cal is None:
            # Fallback : construction directe
            cal = client.calendar(url=cal_url)
        # expand=True non supporté par tous les serveurs — on filtre côté client
        try:
            events_raw = cal.date_search(start=start_dt, end=end_dt, expand=False)
        except Exception:
            events_raw = cal.events()

        events = []
        for ev in events_raw:
            try:
                ical = Calendar.from_ical(ev.data)
                for comp in ical.walk():
                    if comp.name != "VEVENT":
                        continue
                    summary = str(comp.get("SUMMARY", ""))
                    uid = str(comp.get("UID", ""))
                    location = str(comp.get("LOCATION", ""))
                    dtstart = comp.get("DTSTART")
                    dtend = comp.get("DTEND")
                    rrule = comp.get("RRULE")

                    def fmt(dt_prop):
                        if dt_prop is None:
                            return None
                        val = dt_prop.dt
                        if hasattr(val, 'isoformat'):
                            return val.isoformat()
                        return str(val)

                    allday = False
                    if dtstart:
                        import datetime as dt_mod
                        allday = isinstance(dtstart.dt, dt_mod.date) and not isinstance(dtstart.dt, dt_mod.datetime)

                    events.append({
                        "summary": summary,
                        "uid": uid,
                        "location": location,
                        "start": fmt(dtstart),
                        "end": fmt(dtend),
                        "allday": allday,
                        "recurrent": rrule is not None,
                    })
            except Exception:
                continue

        events.sort(key=lambda x: x.get("start") or "")
        return jsonify({"events": events})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    print("CalDAV Tester — http://localhost:5588")
    app.run(host="0.0.0.0", port=5588, debug=False)
