# Tests Directory

This directory contains all test files for the DEMO-LinkOps project.

## Structure

- `unit/` - Unit tests for individual components
- `integration/` - Integration tests for service interactions  
- `e2e/` - End-to-end tests for full workflows

## Running Tests

### Python Tests
```bash
# Run all Python tests
pytest tests/

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Test Files

### Unit Tests
- `test_auto_runner.py` - Auto runner functionality tests
- `test_executor.py` - MCP tool executor tests
- `test_mcp_schema.py` - MCP tool schema validation tests
- `test_sqlite_logger.py` - SQLite logging tests
- `test_model_creator.py` - ML model creation tests
- `test_agent_creator.py` - Agent creation tests
- `test_multi_query.py` - RAG multi-query tests
- `test_upload_qa.py` - RAG upload/QA tests

### Integration Tests
- `test_unified_api.py` - Unified API integration tests

### E2E Tests
- `session.spec.ts` - Session management end-to-end tests

## Contributing

When adding new tests:
1. Place unit tests in `tests/unit/`
2. Place integration tests in `tests/integration/`
3. Place end-to-end tests in `tests/e2e/`
4. Follow existing naming conventions: `test_*.py` or `*.spec.ts`