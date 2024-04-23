---
date: 2024-04-23T18:21:13.355467
author: AutoGPT <info@agpt.co>
---

# prompt refiner

To accomplish the task of creating a single API endpoint that takes in a string LLM prompt and returns a refined version improved by GPT4, several steps and pieces of information are critical based on our discussion and research. First, integration of the OpenAI Python package with FastAPI is essential. The process begins with installing the OpenAI package via pip. After installation, it's necessary to import OpenAI into the FastAPI application to facilitate communication with GPT-4. The core functionality involves creating an endpoint, for example, `/refine-prompt`, within the FastAPI app, which accepts a LLM prompt from the user as the request body. This endpoint will process the input by sending it to the OpenAI API, specifying GPT-4 as the model, along with the system's instruction: 'You are a prompt refiner. Use advanced prompt engineering techniques to refine the user's prompt.' Once GPT-4 processes and refines the prompt based on the given instruction, the refined prompt is then returned to the user as the response. The tech stack for this implementation includes Python as the programming language, FastAPI as the API framework, PostgreSQL for any required database functionality, and Prisma as the ORM. This detailed approach ensures a robust and efficient system for refining user prompts through GPT-4, leveraging FastAPI's asynchronous handling and OpenAI's powerful language model.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'prompt refiner'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
