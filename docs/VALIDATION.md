# Cloud Validation — November 8, 2026

**Execution:** ChatGPT-managed Linux environment, Python 3.12.14. AI-assisted preparation and testing; not an independent Alexander-run assessment.

## Reproduce

```bash
python -m unittest discover -s tests -v
python lab.py
```

**Result:** 5/5 unit tests passed; sample demonstration passed.

The unsafe lookup returned all three fictional user rows for the controlled predicate input. The parameterized lookup returned no rows for the same input. A separate parameterized role lookup returned the intended engineer row.

## Scope

The database is created in memory during execution. This is a deliberately vulnerable educational query and a safe comparison; no external website or database was tested. There is no production severity score or evidence of a third-party vulnerability.

## Personal verification still required

- [ ] Alexander runs the two commands independently
- [ ] Explains SQL structure versus bound data
- [ ] Records genuine screenshots of results
- [ ] Adds an original regression case or safe-query feature
