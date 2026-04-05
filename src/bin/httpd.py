#!/usr/bin/env python3
"""
Minimal CGI HTTP server for Synology LibreSpeedtest package.
Uses NoDemoteCGIHandler to prevent Python dropping to nobody before
executing CGI scripts (which need root to run on Synology).
"""
import os
import sys
from http.server import HTTPServer, CGIHTTPRequestHandler


class NoDemoteCGIHandler(CGIHTTPRequestHandler):
    def run_cgi(self):
        # Prevent Python from dropping privileges to nobody before executing CGI
        old_setuid = os.setuid
        os.setuid = lambda uid: None
        try:
            super().run_cgi()
        finally:
            os.setuid = old_setuid

    def log_message(self, format, *args):
        log_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../var/httpd.log'
        )
        try:
            with open(log_path, 'a') as f:
                f.write(self.address_string() + ' - ' + format % args + '\n')
        except Exception:
            pass


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 39878
    webroot = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else '.')
    os.chdir(webroot)
    HTTPServer(('', port), NoDemoteCGIHandler).serve_forever()
