SYSTEMD_SCRIPT_DIR=$( cd  $(dirname "${BASH_SOURCE:=$0}") && pwd)
cp -f "$SYSTEMD_SCRIPT_DIR/noolite_web_server.service" /lib/systemd/system
chown root:root /lib/systemd/system/noolite_web_server.service

systemctl daemon-reload
systemctl enable noolite_web_server.service