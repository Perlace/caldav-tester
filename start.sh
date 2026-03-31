#!/bin/bash
VENV="/home/user/Documents/claude/curepress-autotester/.venv/bin/python3"
APP="/home/user/Documents/claude/o2switch-tools/caldav-tester/app.py"
URL="http://localhost:5588"

if curl -s -o /dev/null "$URL" 2>/dev/null; then
    xdg-open "$URL" 2>/dev/null &
    exit 0
fi

cd "$(dirname "$APP")"
nohup "$VENV" "$APP" > /tmp/caldav-tester.log 2>&1 &

for i in $(seq 1 10); do
    if curl -s -o /dev/null "$URL" 2>/dev/null; then
        xdg-open "$URL" 2>/dev/null &
        exit 0
    fi
    sleep 0.5
done

echo "Lancé sur $URL"
