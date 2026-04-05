#!/bin/sh
# LibreSpeed upload test and ping/jitter backend
# Replaces empty.php - reads and discards POST body, returns 200

# Consume entire POST body before responding, otherwise browser XHR stalls
if [ "$REQUEST_METHOD" = "POST" ] && [ -n "$CONTENT_LENGTH" ] && [ "$CONTENT_LENGTH" -gt 0 ] 2>/dev/null; then
    dd bs="$CONTENT_LENGTH" count=1 of=/dev/null 2>/dev/null
fi

printf 'Content-Type: text/plain\r\n'
printf 'Cache-Control: no-store, no-cache, must-revalidate, max-age=0\r\n'
printf 'Pragma: no-cache\r\n'
printf '\r\n'
