# sample-vulnerable-app (SYNTHETIC — DO NOT RUN, DO NOT DEPLOY)
Intentionally insecure snippets for static-analysis comparison only.
All credentials are fake. No server entrypoint exists.
Expected findings: SQLi (db.py), hardcoded secret (config.py), unsafe pickle/yaml (serialize.py),
missing authz (views.py), insecure tempfile (files.py), command injection / path traversal (handlers.py).
