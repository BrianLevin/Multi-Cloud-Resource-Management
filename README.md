# Multi-Cloud Resource Management

This project implements a full-stack web application for managing and viewing resources across multiple cloud platforms (AWS and Azure). It features a Python backend with Quart for asynchronous request handling and a React frontend for an interactive user interface.

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
11. [Security](#security)
12. [Future Improvements](#future-improvements)
13. [Contributing](#contributing)
14. [License](#license)

## Features

- Asynchronous fetching of cloud resources for improved performance
- Display of AWS resources:
  - EC2 instances (ID, type, state)
  - Lambda functions (name, memory size, runtime)
  - S3 buckets (names)
- Display of Azure resources:
  - Resource Groups (names)
  - Virtual Machines (name, location, type)
- Interactive web interface built with React for viewing multi-cloud resources
- RESTful API for programmatic access to cloud resource information
- Comprehensive error handling and logging
- Containerization support with Docker
- Secure credential management using Azure Key Vault

## Technologies Used

Backend:
- Python 3.12
- Quart (asynchronous web framework)
- aiobotocore (asynchronous AWS SDK)
- azure-identity and azure-mgmt-resource (Azure SDK)
- azure-keyvault-secrets (Azure Key Vault SDK)

Frontend:
- React
- Material-UI (@mui/material)
- Axios for API calls

Testing:
- unittest for backend unit and integration tests
- pytest for additional test running options
- React Testing Library for frontend tests

Other:
- Docker for containerization
- dotenv for environment variable management

## Project Structure

```
multi-cloud-resource-management/
│
├── app.py                 # Main backend application file
├── config.py              # Configuration and secret management
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── Dockerfile             # Docker configuration
├── .env                   # Environment variables (not in version control)
│
├── tests/                 # Backend tests
│   ├── __init__.py
│   ├── test_app.py
│   ├── test_aws_resources.py
│   ├── test_azure_resources.py
│   └── test_integration.py
│
└── multi-cloud-dashboard/ # Frontend React application
    ├── public/
    ├── src/
    │   ├── components/
    │   │   └── MultiCloudDashboard.js
    │   ├── App.js
    │   ├── App.css
    │   └── index.js
    ├── package.json
    └── README.md
```

## Setup and Installation

### Backend
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

### Frontend
1. Navigate to the frontend directory:
   ```
   cd multi-cloud-dashboard
   ```

2. Install the required npm packages:
   ```
   npm install
   ```

## Configuration

1. Create a `.env` file in the project root with your Azure Key Vault information:
   ```
   KEY_VAULT_NAME=your_key_vault_name
   ```

2. Ensure all sensitive credentials are stored as secrets in your Azure Key Vault:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION
   - AZURE_SUBSCRIPTION_ID
   - AZURE_TENANT_ID
   - AZURE_CLIENT_ID
   - AZURE_CLIENT_SECRET

3. The `config.py` file manages loading these secrets from Azure Key Vault. Review and update if necessary.

## Running the Application

1. Start the backend server:
   ```
   python app.py
   ```
   The API will be available at `http://localhost:5000`

2. In a separate terminal, start the frontend development server:
   ```
   cd multi-cloud-dashboard
   npm start
   ```
   The frontend will be available at `http://localhost:3000`

## API Endpoints

- `GET /multi-cloud-resources`: Fetches and returns resources from both AWS and Azure

## Testing

### Backend Tests
Run the backend test suite using:
```
python -m unittest discover tests
```
Or with pytest:
```
pytest tests
```

### Frontend Tests
Run the frontend tests using:
```
cd multi-cloud-dashboard
npm test
```

## Error Handling and Logging

- Backend implements try-except blocks in cloud resource fetching functions
- Errors are logged for debugging purposes
- API responses include appropriate error messages and status codes
- Frontend displays user-friendly error messages when API calls fail

## Containerization

A Dockerfile is provided for containerizing the application. Build and run the Docker container with:

```
docker build -t multi-cloud-app .
docker run -p 5000:5000 multi-cloud-app
```

## Security

- Sensitive credentials are stored in Azure Key Vault
- Backend retrieves secrets at runtime, avoiding storage of sensitive information in code or environment variables
- CORS settings in the backend restrict access to the frontend origin

## Future Improvements

- Implement user authentication and authorization
- Add functionality to manage (create, update, delete) cloud resources
- Expand coverage of cloud resources (e.g., include more AWS and Azure services)
- Implement real-time updates of cloud resource status
- Enhance frontend with more interactive features and detailed resource views
- Implement secret rotation strategies for long-term security

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
