# Running Airflow with Docker

This guide will help you run Airflow in Docker using docker-compose.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose installed

## Quick Start

1. **Set environment variables** (optional, already configured):
   ```bash
   export AIRFLOW_UID=50000
   ```

2. **Build and start all services**:
   ```bash
   docker-compose up --build
   ```

3. **Access Airflow UI**:
   - Open your browser and go to: http://localhost:8080
   - Username: `airflow`
   - Password: `airflow`

4. **Stop services**:
   ```bash
   docker-compose down
   ```

## Important Commands

### Start services in detached mode (background):
```bash
docker-compose up -d --build
```

### View logs:
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs airflow-scheduler
docker-compose logs airflow-webserver
```

### Run Airflow CLI commands:
```bash
# List DAGs
docker-compose exec airflow-webserver airflow dags list

# Trigger a DAG run
docker-compose exec airflow-webserver airflow dags trigger Airflow_Lab1

# Check DAG status
docker-compose exec airflow-webserver airflow dags state Airflow_Lab1 2025-11-01
```

### Stop and remove volumes (fresh start):
```bash
docker-compose down -v
```

### Access shell in container:
```bash
docker-compose exec airflow-webserver bash
```

## Troubleshooting

### Port already in use
If port 8080 is already in use, modify the webserver ports in `docker-compose.yml`:
```yaml
ports:
  - "8081:8080"  # Use 8081 instead
```

### Permission issues
Make sure the AIRFLOW_UID environment variable is set:
```bash
export AIRFLOW_UID=50000
```

### View DAG errors
Check the scheduler logs for import errors:
```bash
docker-compose logs airflow-scheduler | grep ERROR
```

## Project Structure

```
airflow/
├── dags/                          # Your DAG files
│   └── MLOps-Airflow-Lab1/
│       ├── ML_airflow.py
│       └── src/
├── logs/                          # Logs directory
├── plugins/                       # Airflow plugins
├── docker-compose.yml             # Docker Compose configuration
├── Dockerfile                     # Custom Airflow image
└── requirements.txt               # Python dependencies
```

