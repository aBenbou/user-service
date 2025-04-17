# User Profile Service

A microservice for managing user profiles, expertise areas, preferences, and connections as part of the AI Feedback Platform.

## Architecture

This service integrates with the Authentication Service for user validation and implements a comprehensive API for profile management.

## Features

- Profile management (create, update, get, deactivate)
- Expertise areas management (add, update, delete, list)
- User preferences management (set, delete, get)
- Connection management (request, accept/reject, delete)
- Profile search with filters
- Privacy and visibility controls
- Auth Service integration for authentication and authorization

## API Endpoints

### Profile Management
- `GET /api/profiles/{id}`: Get user profile
- `PUT /api/profiles/{id}`: Update user profile
- `GET /api/profiles/me`: Get current user's profile
- `PUT /api/profiles/deactivate`: Soft delete profile
- `GET /api/profiles/search`: Search profiles with filters

### Expertise Management
- `GET /api/profiles/{id}/expertise`: Get user expertise areas
- `POST /api/profiles/{id}/expertise`: Add expertise area
- `PUT /api/profiles/{id}/expertise/{expertise_id}`: Update expertise
- `DELETE /api/profiles/{id}/expertise/{expertise_id}`: Remove expertise

### Preference Management
- `GET /api/profiles/{id}/preferences`: Get all user preferences
- `GET /api/profiles/{id}/preferences/{category}`: Get preferences by category
- `PUT /api/profiles/{id}/preferences/{category}/{key}`: Set preference
- `DELETE /api/profiles/{id}/preferences/{category}/{key}`: Delete preference

### Connection Management
- `POST /api/profiles/{id}/connections`: Request connection
- `GET /api/profiles/{id}/connections`: Get user connections
- `PUT /api/profiles/{id}/connections/{connection_id}`: Update connection status
- `DELETE /api/profiles/{id}/connections/{connection_id}`: Remove connection

## Setup & Installation

### Environment Variables

Copy the sample environment file:
```bash
cp .env.example .env

# API Documentation Guide

The User Profile Service includes comprehensive API documentation using Swagger/OpenAPI. This documentation makes it easy for frontend developers and API users to understand the available endpoints, expected request formats, and response structures.

## Accessing the API Documentation

Once the service is running, you can access the Swagger UI at:

```
http://localhost:5001/api/docs
```

This will present you with an interactive API documentation interface.

## Features of the Swagger UI

1. **Interactive Documentation**: Test API endpoints directly from the browser
2. **Authentication Support**: Easily add your JWT token for authenticated requests
3. **Request/Response Models**: Clear documentation of all data models
4. **Error Handling**: Documentation of possible error responses
5. **Parameter Documentation**: Detailed information about each parameter

## Authentication

Most endpoints require authentication. To use the interactive features of the Swagger UI:

1. Click the "Authorize" button at the top of the page
2. Enter your JWT token in the format: `Bearer your_token_here`
3. Click "Authorize" and close the dialog

## Example Operations

The API documentation provides complete details for all endpoints, including:

### Profile Management
- Get your profile
- Update profile details
- Search for profiles

### Expertise Management
- Add expertise areas
- Update expertise details
- Delete expertise areas

### Preference Management
- Get all preferences
- Set individual preferences
- Delete preferences

### Connection Management
- Request connections with other users
- Accept or reject connection requests
- View your connections

## Development

If you make changes to the API, the documentation will automatically update to reflect these changes. The documentation is generated from the code annotations in the `app/api/restx` directory and the model definitions in `app/api/docs.py`.

## API Versioning

The current API version is 1.0. Future versions will be documented accordingly, ensuring backward compatibility or providing clear migration paths.