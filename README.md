
# Current Weather Application (CloudCast-Python-App)

This is a simple Python web application that fetches and displays the current weather in any location worldwide in real-time. The application is containerized using Docker and deployed on a Kubernetes cluster using Minikube. The entire process is automated end to end using a GitHub Actions pipeline that runs whenever there's a push to the main branch.


## Features

- **Real-time Exchange Rates**: Fetches current NGN to USD exchange rates from a free API
- **Web Interface**: Clean, responsive web interface accessible via browser
- **Command Line Support**: Can also be run from command line for quick rate checks
- **Error Handling**: Robust error handling for API failures and network issues
- **Docker Support**: Containerized application for easy deployment
- **CI/CD Ready**: Configured for automated deployment pipelines

## Technologies Used

- **Python 3.9+**: Core application language
- **Flask**: Lightweight web framework for serving the web interface
- **Requests**: HTTP library for API calls
- **Docker**: Containerization for consistent deployment
- **OpenWeatherMap API**: The external API used to fetch real-time weather data.
- **Docker**: To containerize the application
- **python-dotenv**: For securely loading environment variables during local development.
- **Minikube**: A lightweight kubernetes dpeloyment environment that uses one node to run both the control plan and worker nodes
- **GitHub Actions**: For automating the creation of docker containers and running the containers in the kubernetes cluster



## Project Structure

```
cicd-python-application/
├── app.py                    # Main application file
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── deployment.yml           # Kubernetes deployment manifest
├── service.yml              # Kubernetes service manifest
├── .github/workflows/       # CI/CD pipeline
│   └── deploy.yml          # GitHub Actions workflow
├── README.md               # Project documentation
└── LICENSE                 # License file
```

## Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cicd-python-application
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`
   - Or use command line by importing and calling `main()` function

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t username/cloudcast-python-app .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 username/cloudcast-python-app
   ```

3. **Access the application**
   - Navigate to: `http://localhost:5000`

## API Usage

The application uses the [OpenWeatherMap API](https://openweathermap.org/) free tier which provides:
- Real-time current weather data for any location worldwide.
- Requires an API key (obtained after free registration)
- 1,500 requests per month (free tier)
- Updates every 24 hours

## Application Features

### Web Interface
- Allows users to input a city name to get weather data
- Displays current temperature (in Celsius), weather description, humidity, and wind speed
- Shows the last fetched timestamp for the displayed weather data
- Provides a clean, responsive design with clear error messages for invalid city inputs or API issues

### Command Line Interface
- The core weather fetching logic can be used programmatically by importing the get_weather_data() function
- Returns structured data containing location, temperature, description, humidity, wind speed, and current fetch  timestamp
- Includes comprehensive error handling for API and network issues when used directly


## Configuration

The application runs on:
- **Host**: `0.0.0.0` (accessible from all network interfaces)
- **Port**: `5000`
- **Debug Mode**: Enabled for development
- **API Key**: The OpenWeatherMap API key is loaded securely from the OPENWEATHER_API_KEY environment variable, ensuring it's not hardcoded in the codebase

## Dependencies

- `requests==2.31.0` - HTTP library for API calls
- `flask==2.3.3` - Web framework
- `python-dotenv==1.0.0` - Variable loading

## Error Handling

The application handles various error scenarios:
- Network connectivity issues
- API service unavailability
- Invalid API responses
- Unexpected Data Formats
- General exceptions


## Deployment

### Docker Deployment
The application is containerized using Docker for consistent deployment across environments.

### Kubernetes Deployment with Minikube

The application can be deployed to Kubernetes using minikube running on an AWS EC2 instance.

#### Prerequisites:
- AWS EC2 instance with Docker, kubectl, and minikube installed
- Minikube cluster running on the EC2 instance

#### Deployment Files:
- `deployment.yml` - Kubernetes deployment with 2 replicas
- `service.yml` - NodePort service exposing the app on port 30080

#### Manual Deployment:
```bash
# Build and load Docker image
docker build -t cloudcatch-python-app:latest .
minikube image load cloudcatch-python-app:latest

# Deploy to Kubernetes
kubectl apply -f deployment.yml
kubectl apply -f service.yml

# Get service URL
minikube service cloudcatch-service --url
```

#### CI/CD Pipeline
Automated deployment pipeline using GitHub Actions that:
- Connects to AWS EC2 instance via SSH
- Builds Docker image and loads it into minikube
- Deploys application to Kubernetes cluster
- Monitors deployment rollout status

#### Required GitHub Secrets:
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `EC2_SSH_KEY` - Private SSH key for EC2 instance
- `EC2_HOST` - Public IP/hostname of EC2 instance

#### Pipeline Workflow:
1. **Build Stage**: Creates Docker image from source code
2. **Deploy Stage**: SSH into EC2, builds image, loads into minikube
3. **Kubernetes Deploy**: Applies manifests and monitors rollout

The service is exposed using ClusterIP.

To access the App on your browser, open a new ssh terminal and run this command to automatically port-forward your node port to your local host port

```bash
ssh -L 5000:localhost:5000 -i path/to/your/keypair ubuntu@ec2-ip-address

```
Inside your terminal run this command to port-ward your service from your cluster to your node port


```bash
kubectl port-forward service/cloudcast-service 5000:80 
```


The application can be assessed on localhost:5000 after successful deployment to Kubernetes.

![app running successfully on loacalhost:5000](<Screenshot (651).png>)




## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the terms specified in the MIT LICENSE file.

## Support

For issues, questions, or contributions, please open an issue in the repository.

---

**Note**: This application is designed for educational and demonstration purposes. For production use, consider implementing additional features like caching, rate limiting, and enhanced security measures.

## Created by Olajide