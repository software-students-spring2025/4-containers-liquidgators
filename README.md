![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![Python Test Workflow- Machine Learning Client](https://github.com/software-students-spring2025/4-containers-liquidgators/actions/workflows/machine-learning.yml/badge.svg?event=pull_request)
![Python Test Workflow- Web App](https://github.com/software-students-spring2025/4-containers-liquidgators/actions/workflows/web-app.yml/badge.svg?event=pull_request)

# Britishify

A containerized app that takes in non-British English speech and returns Britishified English text.

The app is composed of three parts:
- *Machine learning client*: 
    - A Python program that uses Google Cloud Speech to Text to convert the user's speech into text.
- *Web app*: 
    - An interface that allows users to speak any phrase or sentence, and view a Britishified version of the input in text form.
- *MongoDB database*: 
    - A database that stores the user's audio, user's transcribed text, and the Britishified version of user text. 

## Teammates
- [Samantha Lin](https://github.com/sal2948)
- [Jasmine Fan](https://github.com/jasmine7310)
- [Tadelin De Leon](https://github.com/TadelinD)
- [Ray Ochotta](https://github.com/SnowyOchole)

## Instructions for setup

### Installation 

1. Install Docker Desktop [here](https://www.docker.com/products/docker-desktop/)
2. Clone and access our repository:
```
git clone https://github.com/software-students-spring2025/4-containers-liquidgators.git
cd 4-containers-liquidgators
```
3. Create an `.env` file in the root directory with these parameters:
```
GOOGLE_APPLICATION_CREDENTIALS = "provided_google_application_credentials.json"
MONGO_URI=mongodb://mongodb:your_local_host/your_repo_name
MONGO_DB=your_database
```
3. Access the `web-app` folder:
```
cd web-app
```
4. With Docker Desktop open, type "docker build -t localName ." localName can be anything you wish. We recommend something like "Britishify" or "necessary_corrector".
```
docker build -t localName .
```
5. Inside Docker Desktop, click on the `Images` tab to view your new container. Click on the name you gave your Dockerfile to open it, and click `Run`. Set the port number to anything you'd like, and it will run.


