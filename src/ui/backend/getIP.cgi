#!/bin/sh
# LibreSpeed getIP backend
# Replaces getIP.php - returns client IP (and optional ISP info) as JSON
# Called by speedtest.js at startup

ip="${REMOTE_ADDR:-unknown}"

# Strip IPv4-mapped IPv6 prefix (::ffff:x.x.x.x -> x.x.x.x)
case "$ip" in
    ::ffff:*)
        ip="${ip#::ffff:}"
        ;;
esac

printf 'Content-Type: application/json\r\n'
printf 'Cache-Control: no-store, no-cache, must-revalidate, max-age=0\r\n'
printf '\r\n'
printf '{"processedString":"%s","rawIspInfo":{"ip":"%s"}}\n' "$ip" "$ip"
