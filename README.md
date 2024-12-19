# Tirthankara

## Project Overview
Tirthankara is a web application that creates retrofuturistic artwork using AI. Built with Flask and deployed on a home Kubernetes cluster, it provides a web interface for users to generate images by entering text prompts. The project demonstrates modern deployment practices using container orchestration on affordable hardware.

## How It Works
Users can interact with Tirthankara in two ways:
1. Through the web interface, where they can enter prompts and see generated images displayed with a carefully crafted gold-and-dark theme
2. Through direct API calls, allowing programmatic access for automation or integration into other applications

The application handles all communication with Stable Diffusion using a single API key, so users don't need their own credentials.

## Technical Details
The application is built using:
- Flask for the web server
- A custom-designed HTML/CSS interface
- Kubernetes (K3s) for deployment
- Two Orange Pi 3B boards for the computing cluster


### File Structure

```
Tirthankara/
├── src/                    
│   └── webapp.py
├── kubernetes/            
│   ├── deployment.yaml
│   └── service.yaml
├── Dockerfile
├── requirements.txt
└── README.md
```

## For Users
To use Tirthankara, simply:
1. Visit the web interface at 'http://<cluster-ip>' (exact address will be updated after deployment)
2. Enter your prompt in the text field
3. Click "Generate" to create your artwork

For programmatic access:
```python
import requests

response = requests.post(
    "http://<cluster-ip>/generate",
    json={"prompt": "your artistic vision here"}
)
```

## For Developers
If you want to run your own instance of Tirthankara:

1. Clone the repository
2. Set up a Kubernetes cluster (the project uses K3s on Orange Pi 3B boards)
3. Create a secret with your Stable Diffusion API key:
```bash
kubectl create secret generic stability-api-secret \
  --from-literal=api-key='your-api-key'
```
4. Deploy the application:
```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

## Deployment Environment
For local development:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a .env file with your API key and run:
```bash
STABILITY_API_KEY=your-api-key
python src/webapp.py
```
## Project Goals
This project demonstrates:

- Containerized application deployment
- Kubernetes orchestration on affordable hardware
- Secure API key management
- Modern web interface design
- Dual-mode access (web and API)
