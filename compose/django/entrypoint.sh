#!/bin/sh
PUID=${PUID:-0}
PGID=${PGID:-0}
UMASK=${UMASK:-022}

# Check if PUID or PGID is 0, then do not create the musictag user
if [ "$PUID" -eq 0 ] || [ "$PGID" -eq 0 ]; then
  echo "Skipping creation of photozen user because PUID or PGID is set to 0."
else
  if id -u photozen >/dev/null 2>&1 ; then
    echo "user photozen already exists"
  else
    echo "user photozen not exists, creating it"
    useradd -d /app -u "$PUID" photozen
    usermod -o -u "$PUID" photozen
    groupmod -o -g "$PGID" photozen
    chown -R photozen:photozen /app/
    # chmod 644 /app/supervisor.conf
  fi
fi
umask "$UMASK"
# Execute the command as the photozen user if it was created, otherwise as root.
if [ "$PUID" -ne 0 ] && [ "$PGID" -ne 0 ]; then
  export MY_PROGRAM_USER=photozen
  exec gosu photozen "$@"
else
  export MY_PROGRAM_USER=root
  exec "$@"
fi