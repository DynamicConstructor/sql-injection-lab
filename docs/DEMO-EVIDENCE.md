# Demonstration Evidence — Isolated SQL Lab

**Scope:** Localhost and three fictional in-memory SQLite records. No external target.

```bash
python lab.py
python -m unittest discover -s tests -v
python web_lab.py --port 8765
```

Visit `http://127.0.0.1:8765` while the final command is running, then click both comparisons. The ordinary `alice` input returns the same fictional account in both paths. The controlled `' OR '1'='1` input matches three fictional records only in the intentionally unsafe path, while parameterization returns zero. **11 cloud tests passed**, including request-size rejection.

The HTTP comparison is deliberately vulnerable and should never be deployed or exposed through tunneling. Alexander must capture his own side-by-side screenshot and explain the vulnerability and its fix before claiming hands-on execution.
