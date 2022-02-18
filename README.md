# flask-game-suggestion-app
Flask API endpoints to identify a combination of games that has the highest total value of all possible game combinations that fits given pen-drive space

# Getting Started

## Step 1. Install virtualenv on Linux

**- For Debian/Ubuntu:**
1. Start by opening the Linux terminal.

2. Use apt to install virtualenv on Debian, Ubuntu and other related distributions:

`sudo apt install python-virtualenv`

## Step 2: Clone this repo

## Step 3. Create an Environment

1. Move into the cloned project directory:

`cd flask-game-suggestion-app`

To create a virtual environment for Python 3, use the venv module and give it a name:

`python3 -m venv <name of environment>`

## Step 4: Activate the Environment

`. <name of environment>/bin/activate`

## Step 5: Run docker compose build command

`docker build -t <image-name> .`

## Step 6: Start and run your entire app using docker compose 

`docker compose up -d`


# API Endpoints

Once app  is up, visit *http://localhost:5000/docs* for openapi documentation.