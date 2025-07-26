# AI Box Deployment Instructions

These steps will get the AI Box running on a fresh machine or VM.

## Prerequisites

- Docker & Docker Compose installed
- (Optional) Git, curl

## 1. Clone or Extract Package

If using Git:
```bash
git clone https://github.com/your-org/DEMO-LinkOps.git
cd DEMO-LinkOps
```

If using archive:
```bash
tar -xzf demo-linkops.tar.gz
cd DEMO-LinkOps
```

## 2. Configuration

1. Review `.env.example`, copy to `.env` and adjust as needed:

   ```bash
   cp .env.example .env
   # Edit .env:
   # API_PORT=8000
   # FRONTEND_PORT=3000
   # DB_PATH=/app/db
   ```

2. Ensure folders exist:

   ```bash
   mkdir -p db/mcp_tools db/logs sqlite rag_data
   ```

## 3. Start Services

```bash
./package.sh up
```

This will:

* Build and start all containers
* Expose backend on `http://localhost:8000`
* Expose frontend on `http://localhost:3000`

## 4. Verify

* Visit [http://localhost:3000](http://localhost:3000) to see the GUI
* Use "Tool Execution" and "Execution Logs" tabs
* Check backend health:

  ```bash
  curl http://localhost:8000/api/health
  ```

## 5. Packaging for Distribution

To create a zip/tarball:

```bash
./package.sh bundle
```

This outputs `demo-linkops-<version>.tar.gz`.

## 6. Service Management

### Start Services
```bash
./package.sh up
```

### Stop Services
```bash
./package.sh down
```

### View Logs
```bash
docker-compose logs -f
```

### Restart Services
```bash
./package.sh down
./package.sh up
```

## 7. Configuration Options

### Environment Variables

Create a `.env` file with the following options:

```bash
# API Configuration
API_PORT=8000
API_HOST=0.0.0.0

# Frontend Configuration
FRONTEND_PORT=3000
FRONTEND_HOST=0.0.0.0

# Database Configuration
DB_PATH=/app/db
SQLITE_PATH=/app/db/sqlite

# RAG Configuration
RAG_DATA_PATH=/app/rag_data
RAG_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Logging Configuration
LOG_LEVEL=INFO
LOG_PATH=/app/db/logs

# Security Configuration
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Optional: External Services
# OPENAI_API_KEY=your-openai-key
# ANTHROPIC_API_KEY=your-anthropic-key
```

### Port Configuration

Default ports:
- **Frontend**: 3000
- **Backend API**: 8000
- **RAG Service**: 8001 (internal)

To change ports, edit the `.env` file or pass environment variables:

```bash
API_PORT=9000 FRONTEND_PORT=4000 ./package.sh up
```

## 8. Data Persistence

The AI Box stores data in the following locations:

- **MCP Tools**: `./db/mcp_tools/`
- **Execution Logs**: `./db/logs/`
- **SQLite Database**: `./db/sqlite/`
- **RAG Documents**: `./rag_data/`

These directories are mounted as volumes and persist between container restarts.

## 9. Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   # Change port in .env file
   API_PORT=8001
   ```

2. **Permission Issues**
   ```bash
   # Fix directory permissions
   sudo chown -R $USER:$USER db/
   chmod -R 755 db/
   ```

3. **Container Build Failures**
   ```bash
   # Clean and rebuild
   docker-compose down
   docker system prune -f
   ./package.sh up
   ```

4. **Database Issues**
   ```bash
   # Reset database (WARNING: loses data)
   rm -rf db/sqlite/*
   ./package.sh up
   ```

### Health Checks

Check service health:

```bash
# API Health
curl http://localhost:8000/api/health

# Frontend Health
curl http://localhost:3000

# Container Status
docker-compose ps
```

### Logs

View service logs:

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs unified-api
docker-compose logs frontend
docker-compose logs rag

# Follow logs
docker-compose logs -f
```

## 10. Production Deployment

### Security Considerations

1. **Change Default Secrets**
   ```bash
   # Generate a secure secret key
   openssl rand -hex 32
   # Update .env file
   SECRET_KEY=your-generated-secret
   ```

2. **Network Security**
   ```bash
   # Use reverse proxy (nginx/traefik)
   # Configure SSL/TLS certificates
   # Set up firewall rules
   ```

3. **Data Backup**
   ```bash
   # Backup data directory
   tar -czf ai-box-backup-$(date +%Y%m%d).tar.gz db/
   ```

### Scaling

For production scaling:

1. **Load Balancer**: Use nginx or traefik
2. **Database**: Consider PostgreSQL for larger deployments
3. **Caching**: Add Redis for session management
4. **Monitoring**: Add Prometheus/Grafana

### Environment-Specific Configs

Create environment-specific configuration files:

```bash
# Development
cp .env.example .env.dev

# Production
cp .env.example .env.prod

# Staging
cp .env.example .env.staging
```

## 11. Updates and Maintenance

### Updating the AI Box

1. **Pull Latest Changes**
   ```bash
   git pull origin main
   # or extract new archive
   ```

2. **Rebuild Services**
   ```bash
   ./package.sh down
   ./package.sh up
   ```

### Backup and Restore

1. **Backup Data**
   ```bash
   ./package.sh backup
   ```

2. **Restore Data**
   ```bash
   ./package.sh restore backup-file.tar.gz
   ```

## 12. Support and Documentation

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check `/docs` directory for detailed guides
- **API Documentation**: Available at `http://localhost:8000/docs`

## 13. License and Legal

This AI Box deployment package is provided under the same license as the source code. Please review the LICENSE file for details.

---

**🎉 Your AI Box is now ready for deployment!**

For additional support, please refer to the project documentation or contact the development team. 