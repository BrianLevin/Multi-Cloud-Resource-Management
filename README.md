
# Multi-Cloud Resource Management

This project implements a web application for managing and viewing resources across multiple cloud platforms (AWS and Azure). It uses a Python backend with Quart for asynchronous request handling and a React frontend for the user interface.

## Table of Contents
1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Project Structure](#project-structure)
4. [Setup and Installation](#setup-and-installation)
5. [Configuration](#configuration)
6. [Running the Application](#running-the-application)
7. [API Endpoints](#api-endpoints)
8. [Testing](#testing)
9. [Error Handling and Logging](#error-handling-and-logging)
10. [Containerization](#containerization)
11. [Future Improvements](#future-improvements)
12. [Contributing](#contributing)
13. [License](#license)

## Features

- Asynchronous fetching of cloud resources for improved performance
- Display of AWS resources:
  - EC2 instances (ID, type, state)
  - Lambda functions (name, memory size, runtime)
  - S3 buckets (names)
- Display of Azure resources:
  - Resource Groups (names)
  - Virtual Machines (name, location, type)
- Simple web interface built with React for viewing multi-cloud resources
- RESTful API for programmatic access to cloud resource information
- Comprehensive error handling and logging
- Containerization support with Docker

## Technologies Used

- Backend:
  - Python 3.12
  - Quart (asynchronous web framework)
  - aiobotocore (asynchronous AWS SDK)
  - azure-identity and azure-mgmt-resource (Azure SDK)
- Frontend:
  - React
  - Axios for API calls
- Testing:
  - unittest for unit and integration tests
  - pytest for additional test running options
- Other:
  - Docker for containerization
  - dotenv for environment variable management

## Project Structure

```
multi-cloud-resource-management/
│
├── app.py                 # Main application file with Quart app and route handlers
├── config.py              # Configuration settings and environment variable management
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation (this file)
├── Dockerfile             # Docker configuration for containerization
├── .env                   # Environment variables (not in version control)
│
├── tests/
│   ├── __init__.py
│   ├── test_app.py        # Tests for main application routes
│   ├── test_aws_resources.py  # Tests for AWS resource fetching
│   ├── test_azure_resources.py  # Tests for Azure resource fetching
│   └── test_integration.py  # Integration tests
│
└── frontend/              # React frontend application (structure may vary)
    ├── package.json
    ├── public/
    └── src/
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/multi-cloud-resource-management.git
   cd multi-cloud-resource-management
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the frontend (assuming you have Node.js and npm installed):
   ```
   cd frontend
   npm install
   ```

## Configuration

1. Create a `.env` file in the project root with your cloud credentials:
   ```
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_DEFAULT_REGION=your_aws_region

   AZURE_SUBSCRIPTION_ID=your_azure_subscription_id
   AZURE_TENANT_ID=your_azure_tenant_id
   AZURE_CLIENT_ID=your_azure_client_id
   AZURE_CLIENT_SECRET=your_azure_client_secret
   ```

2. The `config.py` file manages loading these environment variables. Review and update if necessary.

## Running the Application

1. Start the backend server:
   ```
   python app.py
   ```

2. In a separate terminal, start the frontend development server:
   ```
   cd frontend
   npm start
   ```

3. Access the web interface at `http://localhost:5000`

## API Endpoints

- `GET /`: Serves the React frontend application
- `GET /multi-cloud-resources`: Fetches and returns resources from both AWS and Azure

## Testing

Run the test suite using:

```
python -m unittest discover tests
```

Or with pytest:

```
pytest tests
```

The test suite includes:
- Unit tests for the main application routes
- Unit tests for AWS resource fetching function
- Unit tests for Azure resource fetching function
- Integration tests simulating full application behavior

Tests use mocking to simulate cloud service responses, allowing them to run without actual cloud credentials.

## Error Handling and Logging

- Implemented try-except blocks in cloud resource fetching functions
- Errors are logged for debugging purposes
- API responses include appropriate error messages and status codes

## Containerization

A Dockerfile is provided for containerizing the application. Build and run the Docker container with:

```
docker build -t multi-cloud-app .
docker run -p 5000:5000 multi-cloud-app
```

## Future Improvements

- Implement user authentication and authorization
- Add functionality to manage (create, update, delete) cloud resources
- Expand coverage of cloud resources (e.g., include more AWS and Azure services)
- Implement real-time updates of cloud resource status
- Enhance frontend with more interactive features and detailed resource views

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.