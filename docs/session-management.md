# Session Management in DEMO-LinkOps

## Overview

DEMO-LinkOps implements a secure, user-friendly session management system with role-based access control. The system uses JWT tokens for authentication and authorization, with a secure refresh token mechanism to maintain sessions.

## Features

- 30-minute access tokens
- Secure refresh tokens (7-day expiry)
- Role-based access control (slim/full demo modes)
- Automatic session extension during activity
- User-friendly expiry warnings
- Token rotation for security

## Session Flow

1. **Initial Login**
   - User logs in with credentials
   - Backend issues:
     - 30-minute access token (JWT)
     - 7-day refresh token (HttpOnly cookie)
   - Frontend stores access token in memory

2. **Session Maintenance**
   - Access token used for API requests
   - Silent refresh on user activity
   - Warning shown 5 minutes before expiry
   - Manual refresh available via UI

3. **Security Measures**
   - Refresh tokens stored in HttpOnly cookies
   - Token rotation on each refresh
   - Secure cookie flags (HttpOnly, Secure, SameSite)
   - Role claims validated on protected routes

## Configuration

### Environment Variables

```env
JWT_SECRET_KEY=your-secure-key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Cookie Settings

```python
response.set_cookie(
    key="refresh_token",
    value=token,
    httponly=True,
    secure=True,
    samesite="strict"
)
```

## Demo Modes

### Slim Demo (`demo-slim/demo`)
- Basic features
- Read-only access
- Standard pipeline view

### Full Demo (`demo-full/arise!`)
- Advanced features
- ML Builder access
- HTC functionality
- Complete pipeline control

## Monitoring

Session metrics are tracked and available in the monitoring dashboard:
- Active sessions
- Login attempts
- Token rotations
- Session durations
- Warning banner displays

## Security Considerations

1. **Token Storage**
   - Access tokens: Memory only
   - Refresh tokens: HttpOnly cookies
   - No sensitive data in localStorage

2. **Token Rotation**
   - New refresh token on each use
   - Old tokens invalidated
   - Prevents token replay attacks

3. **Cookie Security**
   - HttpOnly: Prevents XSS
   - Secure: HTTPS only
   - SameSite=Strict: CSRF protection

## Testing

End-to-end tests cover:
- Login flows
- Session expiry
- Token refresh
- Role-based access
- Security measures

Run tests with:
```bash
# Frontend E2E tests
cd frontend
npm run test:e2e

# Backend tests
cd unified-api
pytest tests/test_auth.py
```

## Common Issues

1. **Session Expired**
   - Clear browser cookies
   - Log in again
   - Check system time sync

2. **Access Denied**
   - Verify correct demo credentials
   - Check role requirements
   - Ensure token is valid

3. **Refresh Failed**
   - Check network connectivity
   - Verify cookie settings
   - Clear browser cache

## Best Practices

1. **Development**
   - Use environment variables
   - Never commit secrets
   - Test both demo modes

2. **Deployment**
   - Secure cookie domain
   - Configure CORS properly
   - Monitor session metrics

3. **Maintenance**
   - Rotate JWT secret regularly
   - Monitor failed refreshes
   - Update dependencies

## API Reference

### Authentication Endpoints

```typescript
POST /auth/login
Body: { username: string, password: string }
Response: { access_token: string, token_type: string, role: string }

POST /auth/refresh
Cookies: refresh_token
Response: { access_token: string, token_type: string, role: string }

POST /auth/logout
Response: { message: string }
```

### Protected Routes
```typescript
// Requires authentication
GET /api/* 

// Requires full demo access
POST /api/ml-builder/*
POST /api/htc/*
``` 