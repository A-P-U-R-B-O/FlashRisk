# FlashRisk

**FlashRisk** is an AI-powered, real-time disaster detection and alerting platform. It provides live data on global disasters by integrating with public APIs (such as [ReliefWeb](https://reliefweb.int/help/api)), and robust notification infrastructure for users and systems.

---

## Features

- 🌎 **Global Disaster Monitoring**: Aggregates data from trusted sources like ReliefWeb and USGS.
- 🚨 **Real-Time Alerts**: Pushes instant notifications for new disasters.
- 📈 **Live Dashboard**: Visualize events and trends.
- 🔔 **Flexible Notification System**: Webhooks, email, and more.
- 📦 **API-First**: Well-documented REST API for integration and extension.
- 🛡️ **Observability**: Prometheus metrics, health checks, and logging.
- ⚡ **Modern Stack**: FastAPI backend, React frontend.

---

## Project Structure

```
flashrisk/
├── backend/              # FastAPI backend (see src/)
│   ├── src/
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── fetchers.py
│   │   └── ...
│   ├── requirements.txt
│   └── ...
├── frontend/             # React frontend (see src/)
│   ├── src/
│   │   ├── App.js
│   │   ├── api/
│   │   ├── components/
│   │   └── ...
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── ...
├── render.yaml           # Deployment configuration for Render.com
├── README.md
└── ...
```

---

## Quickstart

### 1. Clone the repo

```sh
git clone https://github.com/A-P-U-R-B-O/flashrisk.git
cd flashrisk
```

### 2. Backend (FastAPI)

```sh
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 10000
```

- Open [http://localhost:10000/docs](http://localhost:10000/docs) for the interactive API docs.

### 3. Frontend (React)

```sh
cd frontend
npm install
npm start
```

- Open [http://localhost:3000](http://localhost:3000) for the dashboard.

---

## Configuration

- **Environment Variables (Backend):**
  - `ALLOWED_ORIGINS`: CORS allowed origins (default: `*`)
  - `ENABLE_METRICS`: Enable Prometheus metrics endpoint (default: `true`)
  - Add your own notification or DB settings as needed.

- **API Endpoints:**
  - `/api/disasters` — Get recent disasters.
  - `/api/notify` — Manage/test notifications.
  - See `/docs` for full OpenAPI docs.

---

## Deployment

- **Render.com:** Use the provided `render.yaml` for easy deployment of both frontend and backend.
- **Docker:** You can add Dockerfiles for containerized deployment.
- **Other Cloud:** Works with most cloud providers supporting Node.js and Python.

---

## Integrations

- [ReliefWeb API](https://reliefweb.int/help/api)  
- [USGS Earthquake Feed](https://earthquake.usgs.gov/fdsnws/event/1/)
- (Extendable: Add more disaster feeds as needed!)

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a pull request

---

## License

[MIT](LICENSE)  
© 2025 [A-P-U-R-B-O](https://github.com/A-P-U-R-B-O)

---

## Acknowledgments

- [ReliefWeb](https://reliefweb.int/)
- [USGS Earthquake Program](https://earthquake.usgs.gov/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)

---
