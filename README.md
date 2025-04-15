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