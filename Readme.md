# Student Notes App (Flask + MySQL + Selenium)

## Run the app

```powershell
docker compose up --build web mysql
```

Open: `http://localhost:5000`

## Run end-to-end Selenium test

```powershell
docker compose up --build --abort-on-container-exit tests
```

This command starts:
- `mysql` (database)
- `web` (Flask app)
- `selenium` (Chrome browser container)
- `tests` (Selenium runner)

If test passes, the `tests` container exits with code `0`.
