# Spotify SongAdder

A simple web app for managing and adding songs to your Spotify playlists.

## Table of Contents
- [Introduction](#introduction)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#1-clone-the-repository)
  - [Create and Activate a Virtual Environment](#2-create-and-activate-a-virtual-environment)
  - [Install Dependencies](#3-install-dependencies)
  - [Set Up Spotify API Credentials](#4-set-up-spotify-api-credentials)
  - [Configure Environment Variables](#5-configure-environment-variables)
  - [Run the Application](#6-run-the-application)
- [Usage](#usage)

## Introduction

Spotify SongAdder allows users to authenticate with Spotify and add songs to their playlists with ease. The app allows you to process playlists by entering the playlist link, adding tracks, and viewing feedback on added, skipped, or missing tracks.

## Setup Instructions

Follow these steps to set up the project on your local machine:

### Prerequisites

Make sure you have the following installed:
- Python 3.x (preferably Python 3.7+)
- Git (to clone the repository)
- Spotify Developer Account (for creating a Spotify API application and obtaining credentials)

### 1. Clone the Repository

Open your terminal and clone the project repository:

```bash
git clone https://github.com/Chetoh16/SongAdder
```

### 2. Create and Activate a Virtual Environment

Navigate to the project directory and create a virtual environment:

```bash
cd spotify-songadder
python -m venv venv
```

#### Activate the virtual environment:

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```
### 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

### 4. Set Up Spotify API Credentials

To use the Spotify API, you need to create an app on the Spotify Developer Dashboard.

1. Go to the Spotify Developer Dashboard and log in with your Spotify account.
2. Create a new app.
3. Note down the Client ID, Client Secret, and Redirect URI (you will need to set this URI in your app as well).

### 5. Configure Environment Variables

Create a .env file in the root directory of the project. This file will store sensitive information such as your Spotify API credentials. Add the following contents to the .env file:

```bash
client_id=your_client_id
client_secret=your_client_secret
```
Replace your_client_id and your_client_secret with your actual credentials.

### 6. Run the Application

After setting up everything, run the Flask application:

```bash
python song_adder.py
```
This should start the server locally at http://localhost:5000. Open this URL in your browser to use the app.

### Usage
1. Log In: When you visit the homepage, you'll be prompted to log in to your Spotify account.
2. Add Songs: After logging in, you can paste your Spotify playlist URL to add songs to the playlist.
3. Error Handling: If the playlist link is invalid, an error message will appear.
4. Song Processing Feedback: Once songs are processed, you'll see feedback showing which songs were added, skipped, or couldn't be found.
