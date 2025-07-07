# Whis Enhance Service

This is the whis_enhance microservice in the LinkOps MLOps platform.

## Responsibilities
- Enhance and optimize Orbs/Runes for improved ML performance and agent logic
- **Loopback Logic**: Process repeated/failed tasks to improve rune quality
- **Version Control**: Track changes and maintain version history for runes and orbs
- **Quality Assessment**: Evaluate and improve content quality across the pipeline

## 🔁 Loopback Logic

The Whis Loopback Logic processes repeated tasks and failures to continuously improve the system:

### Flow
```
Failed/Repeated Input → Stored in history.csv → Sent to whis_enhance → 
Re-evaluated and used to:
- Improve existing Runes
- Replace bad Orbs  
- Retrain model context
```

### API Endpoints

- `POST /loopback?threshold=2` - Trigger loopback refinement process
- `GET /loopback/stats` - Get loopback processing statistics

### Usage Example

```bash
# Trigger loopback refinement
curl -X POST "http://localhost:8006/loopback?threshold=2"

# Get statistics
curl -X GET "http://localhost:8006/loopback/stats"
```

## 🧬 Enhancement Types

- **Content Enhancement**: Improve text, image, audio, video quality
- **Metadata Enhancement**: Add context, classification, sentiment analysis
- **Quality Assessment**: Evaluate readability, accuracy, completeness
- **Loopback Refinement**: Learn from repeated/failed tasks

## 📊 Version Control

- Automatic versioning of enhanced runes and orbs
- Backup creation before modifications
- Version history tracking
- Rollback capabilities 