# 📊 Streamlit DB Viewer & File Manager

A **production-ready web application** to browse MySQL database tables and import files — all through a clean browser UI. Built with Python + Streamlit, containerized with Docker Compose.

---

## 🖥️ What It Does

| Feature | Description |
|---------|-------------|
| **Database Viewer** | Select any table → see all records in a sortable, scrollable grid |
| **File Uploader** | Upload any file from your Mac via the browser |
| **Volume Import** | Drop files into `uploads/` folder → click Import in the UI |
| **File Manager** | View and delete imported files inside the container |

---

## 🏗️ Architecture

```
Your Mac (Browser: http://localhost:8501)
      │
      ├──► streamlit_app container (Python/Streamlit, port 8501, 256MB RAM)
      │         │
      │         └──► mysql_db container (MySQL 8.0, port 3306, 512MB RAM)
      │
      └──► uploads/ folder on Mac → mounted into container at /app/uploads
```

---

## 📁 Project Structure

```
streamlit-db-viewer-file-manager/
├── app/
│   ├── app.py              # Streamlit application (all UI logic)
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # App container build instructions
├── db/
│   └── init.sql            # Auto-creates tables + inserts sample data on first start
├── uploads/                # Drop files here → appear in app instantly
├── docker-compose.yml      # Orchestrates both containers
├── .gitignore
└── README.md
```

---

## ⚙️ Prerequisites

| Tool | Check | Install |
|------|-------|---------|
| Docker | `docker --version` | [docker.com](https://www.docker.com/products/docker-desktop/) |
| Docker Compose | `docker-compose --version` | Included with Docker Desktop |
| Git | `git --version` | [git-scm.com](https://git-scm.com/) |

> **Mac + Homebrew alternative (no Docker Desktop needed):**
> ```bash
> brew install colima docker docker-compose && colima start
> ```

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/mounikakompalli/streamlit-db-viewer-file-manager.git
cd streamlit-db-viewer-file-manager

# Start all containers (first run ~2-3 min to download images)
docker-compose up --build -d

# Open in browser (wait ~30 sec for MySQL to initialize)
open http://localhost:8501

# Stop when done
docker-compose down
```

---

## 🗄️ Database Details

Auto-created on first start via `db/init.sql`. Database name: `appdb`

**employees table** — 6 sample records
| Column | Type |
|--------|------|
| id | INT AUTO_INCREMENT PRIMARY KEY |
| name | VARCHAR(100) |
| department | VARCHAR(100) |
| salary | DECIMAL(10,2) |
| hire_date | DATE |

**products table** — 6 sample records
| Column | Type |
|--------|------|
| id | INT AUTO_INCREMENT PRIMARY KEY |
| product_name | VARCHAR(100) |
| category | VARCHAR(100) |
| price | DECIMAL(10,2) |
| stock | INT |

```bash
# Query MySQL directly
docker exec mysql_db mysql --socket=/var/run/mysqld/mysqld.sock \
  -u appuser -papppassword appdb -e "SELECT * FROM employees;"
```

---

## 📁 File Import

**Method 1 — Browser:** Go to app → File Importer → Browse files → file saves to `/app/imported_files`

**Method 2 — Volume Mount:** Copy files to local `uploads/` folder → appear in app instantly → click "Import →"

---

## 🔧 Key Configuration (docker-compose.yml)

| Setting | Default | Notes |
|---------|---------|-------|
| App port | `8501` | Change `"8501:8501"` to e.g. `"8080:8501"` |
| DB password | `apppassword` | Change `MYSQL_PASSWORD` AND `DB_PASS` together |
| DB name | `appdb` | Change `MYSQL_DATABASE` AND `DB_NAME` together |
| App RAM | `256m` | Adjust `mem_limit` under `app` |
| MySQL RAM | `512m` | Adjust `mem_limit` under `db` |

---

## 🛠️ Development

```bash
# After editing app/app.py — rebuild:
docker-compose up --build -d

# After editing db/init.sql — full reset:
docker-compose down -v && docker-compose up --build -d

# After adding packages to requirements.txt — rebuild:
docker-compose up --build -d

# Live logs
docker-compose logs -f app

# Shell into containers
docker exec -it streamlit_app /bin/bash
docker exec -it mysql_db bash
```

---

## 📋 Commands Cheatsheet

| Action | Command |
|--------|---------|
| Start with rebuild | `docker-compose up --build -d` |
| Start no rebuild | `docker-compose up -d` |
| Stop, keep data | `docker-compose down` |
| Stop + wipe data | `docker-compose down -v` |
| Check status | `docker-compose ps` |
| App logs | `docker-compose logs -f app` |
| List imported files | `docker exec streamlit_app ls /app/imported_files` |

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Database connection error" | Wait 30 sec, refresh. Check: `docker-compose ps` |
| Port 8501 in use | Run `lsof -i :8501` or change port in docker-compose.yml |
| Need full reset | `docker-compose down -v && docker-compose up --build -d` |
| Docker not running (Mac) | Open Docker Desktop OR run `colima start` |

---

## 🔮 Ideas to Extend This Project

- [ ] Search/filter records within tables
- [ ] Export any table to CSV download
- [ ] Add/Edit/Delete records (full CRUD UI)
- [ ] User authentication / login page
- [ ] Charts and graphs with Plotly
- [ ] AI natural language queries ("Show employees in HR")
- [ ] Pagination for large tables (1000+ rows)

---

## 🤝 Contributing

1. Fork → `git checkout -b feature/your-feature`
2. Make changes → test with `docker-compose up --build -d`
3. Commit → `git commit -m "Add: description"`
4. Push → PR on GitHub

---

## 📄 License

MIT — free to use, modify, and distribute.

*Built with ❤️ using Streamlit, MySQL, and Docker*
