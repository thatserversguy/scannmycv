#ScannMyCV — AI-powered Resume Analyzer
🎯 An AI-driven web application that analyzes resumes for ATS (Applicant Tracking System) friendliness and provides actionable improvement suggestions.

This project demonstrates how to build, deploy, and run a Next.js + FastAPI application on Azure cloud, with full CI/CD automation using Azure DevOps — even on a free-tier Azure subscription with quotas and limitations.

🚀 Features
✅ Upload your resume (PDF)
✅ Get ATS-friendly score (0–100%)
✅ AI-generated suggestions to improve your resume
✅ Fully automated CI/CD pipeline
✅ Deployed using cost-efficient Azure services

🧰 Tech Stack
Frontend: Next.js + TailwindCSS

Backend: Python FastAPI + OpenAI GPT API

CI/CD: Azure DevOps Pipelines (YAML)

Cloud Infrastructure:

Azure Static Web Apps (frontend)

Azure Container Instances (backend — due to free-tier quota on Web Apps)

Azure DevOps (repo, pipeline, self-hosted agent)

☁️ Cloud Architecture
Here’s how the app is architected:

less
Copy
Edit
[ GitHub / Azure Repos ]
        |
        v
   [ Azure DevOps ]
        |
        | YAML pipeline
        v
[ Self-hosted Linux agent ]
        |
        v
-------------------------------
|         Azure Cloud         |
|                             |
|  Static Web App (frontend)  |
|         +                   |
|  Container Instance (API)   |
-------------------------------
Frontend: hosted on Azure Static Web App

Backend: containerized FastAPI app hosted on Azure Container Instance

CI/CD: Azure DevOps triggers on main branch push, builds and deploys both components

🧑‍💻 Deployment Steps
Prerequisites
✅ Azure account (free tier is fine)
✅ Azure DevOps organization + project
✅ GitHub or Azure Repos for code
✅ OpenAI API key

1️⃣ Fork and clone this repo
bash
Copy
Edit
git clone https://github.com/<your-username>/scannmycv.git
cd scannmycv
2️⃣ Frontend: Static Web App
Go to Azure Portal → Create Resource → Static Web App

Choose:

Source: Azure DevOps

Organization & Project: your Azure DevOps project

Repository & branch: main

Framework: Next.js

App location: frontend

Output location: .next

Complete creation

3️⃣ Backend: Azure Container Instance
Build and push FastAPI Docker image (backend/Dockerfile) to your container registry (ACR or Docker Hub)

Deploy ACI:

Choose your image from registry

Expose port 8000

Configure environment variable OPENAI_API_KEY

4️⃣ Azure DevOps Pipelines
Create a YAML pipeline (azure-pipelines.yml) in the repo

Make sure your agent pool points to either:

Azure Hosted Agents (if parallelism granted)

Or self-hosted Linux agent (instructions in agent-setup.md)

Run pipeline — it will build frontend and deploy to Static Web App, and deploy backend image to ACI.

🔑 OpenAI API Key
⚠️ Note: The OpenAI API key used for testing may become invalid or rate-limited. To use the app yourself, get your own OpenAI key and set it as an environment variable OPENAI_API_KEY in ACI.

📄 Files & Folders
/frontend → Next.js client app

/backend → FastAPI server

azure-pipelines.yml → Azure DevOps pipeline config
