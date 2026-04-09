# Maintenance Strategy

## CampusEats — Online Food Ordering System

This document outlines how the system should be **operated, monitored, updated, and repaired** after initial delivery, suitable for a **college project handover** or a small deployment.

---

## 1. Objectives

- Keep the application **available** for demos and coursework evaluation.
- Protect **user data** and configuration from loss or accidental exposure.
- Allow **safe updates** to dependencies and code with minimal downtime.
- Document **who does what** (even if the “team” is one student).

---

## 2. Types of Maintenance

### 2.1 Corrective maintenance

**Purpose:** Fix defects after release.

| Activity | Practice |
|----------|----------|
| Bug reports | Use a simple log (spreadsheet or issue list): symptom, steps, severity, fix version. |
| Reproduction | Reproduce on a copy of production data if possible; never experiment on the only backup. |
| Patching | Fix in development branch → run tests/manual TCs from `Test_Cases.md` → deploy. |
| Hotfix | For demo day only: minimal change; document in README or change log. |

### 2.2 Adaptive maintenance

**Purpose:** Adapt to environment changes.

| Trigger | Action |
|---------|--------|
| Python / Django upgrade | Read release notes; run `manage.py check` and migrations; re-run critical test cases. |
| Database switch (SQLite → MySQL/PostgreSQL) | Update `DATABASES` in `settings.py`; run migrations; verify media paths. |
| OS or hosting move | Reinstall `venv`, `pip install -r requirements.txt`, set `ALLOWED_HOSTS`, `SECRET_KEY`, `DEBUG=False` for real hosting. |

### 2.3 Perfective maintenance

**Purpose:** Improve usability or performance without changing required scope.

- Refine templates, messages, or validation messages.
- Add indexes on heavily filtered columns if the DB grows (e.g. `Order.restaurant_id`, `Order.user_id`).
- Optional: add logging for failed logins or payment attempts.

### 2.4 Preventive maintenance

**Purpose:** Avoid failures before they happen.

- **Dependencies:** Periodically `pip list --outdated`; pin versions in `requirements.txt` after testing.
- **Security:** Rotate `SECRET_KEY` if ever exposed; never commit secrets; use environment variables in production.
- **Disk:** Monitor `media/` growth (menu images); plan cleanup or quotas.

---

## 3. Backup and recovery

| Asset | Backup approach | Frequency |
|-------|-----------------|-----------|
| **Database** | Copy `db.sqlite3` (or DB dump for MySQL/PostgreSQL) | Before each demo / weekly |
| **Media files** | Copy `media/` folder | With database |
| **Code** | Git repository (remote: GitHub/GitLab) | Every meaningful change |

**Recovery:** Restore DB file and `media/` to a known good snapshot; redeploy code from tagged commit.

---

## 4. Deployment (production-style checklist)

For coursework, **DEBUG=True** on localhost is acceptable. For any public host:

1. Set `DEBUG = False` and `ALLOWED_HOSTS`.
2. Use a strong `SECRET_KEY` from environment variable.
3. Run `collectstatic` behind a real web server (e.g. Gunicorn + Nginx) if not using `runserver`.
4. Enable HTTPS on the host.
5. Restrict Django Admin exposure (strong passwords, optional IP allowlist).

---

## 5. Monitoring and support

| Area | Recommendation |
|------|----------------|
| **Errors** | Enable Django logging to file or console; check logs after deployment. |
| **Uptime** | For demos, manual check; for servers, optional ping or HTTP health URL. |
| **Support window** | Define “best effort” response (e.g. coursework submission week only). |

---

## 6. Roles and responsibilities (template)

| Role | Responsibility |
|------|----------------|
| Developer / student | Code fixes, migrations, backups before demos. |
| Instructor / evaluator | Read-only access or demo account; report issues via agreed channel. |
| System owner | Holds credentials, server access, and backup storage location. |

---

## 7. Change management

1. **Small change:** Edit locally → `manage.py check` → run selected test cases → commit with clear message.  
2. **Schema change:** Create migration → apply on copy of DB first → document in submission appendix if required.  
3. **Breaking change:** Update SRS appendix or version table; notify stakeholders (evaluator).

---

## 8. Retirement / handover

When the project is archived:

- Export final DB and media zip.
- Store repository URL and commit hash used for submission.
- Document superuser creation steps (`createsuperuser`) without storing passwords in the doc.

---

*End of Maintenance Strategy document*
