# HubSpot Integration Backend

A backend service for HubSpot integration.

## Features

- HubSpot OAuth 2.0 integration
- Contact and Company data management
- Automatic token refresh
- File-based OAuth data storage
- Type-safe API with Pydantic models

## Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- uv package manager

## Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd hs-backend-demo
   ```

2. Create a `.env` file with HubSpot credentials:

   ```env
   HUBSPOT_CLIENT_ID=your_client_id
   HUBSPOT_CLIENT_SECRET=your_client_secret
   HUBSPOT_REDIRECT_URI=your_redirect_uri
   HUBSPOT_SCOPES=contacts companies
   ```

3. Install dependencies:
   ```bash
   uv pip install .
   ```

## Development

### Running the Application

You can run the application in two ways:

1. Using Python directly:

   ```bash
   make run
   ```

2. Using Docker:

   ```bash
   # Build the container
   make docker-build

   # Start the container
   make docker-up

   # Stop the container
   make docker-down
   ```

The API will be available at http://localhost:8000

### Running Tests

Run all tests:

```bash
make test
```

Run tests with coverage:

```bash
make coverage
```

### Cleanup

Clean up generated files:

```bash
make clean
```

## API Endpoints

### Authentication

- `GET /auth/install` - Redirects to HubSpot OAuth login
- `GET /auth/callback` - Handles OAuth callback and stores tokens

### Contacts

- `GET /contacts` - Get list of contacts

  - Query Parameters:
    - `portal_id` (required): HubSpot portal ID
    - `limit` (optional): Number of contacts to return (default: 10)
    - `after` (optional): Pagination cursor

- `GET /contacts/{contact_id}/companies` - Get companies associated with a contact
  - Query Parameters:
    - `portal_id` (required): HubSpot portal ID

## API Documentation

Once the application is running, you can access:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Health Check

The application provides a health check endpoint:

```bash
curl http://localhost:8000/healthcheck
```

Expected response:

```json
{
  "status": "healthy"
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 400: Bad Request - Invalid input or HubSpot operation failed
- 401: Unauthorized - Missing or invalid OAuth data
- 500: Internal Server Error - Unexpected errors

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests: `make test`
4. Submit a pull request
