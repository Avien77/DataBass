# DataBASS

Nate Oberdier [AI Major], Pablo Avila [CS Major], Kaeden Bryer [CS Major], Nicholas Sakowski [CS Major]

## Setup Instructions

Create a virtual environment with:
- `python -m venv .venv` 
-  `source .venv/bin/activate` (on mac, look up windows alternative)

Then, install the requirements with `pip3 install -r requirements.txt`. Make sure you're in the root directory

Next, create a .env file. Clone .env.example with `cp .env.example .env`, then replace DB_USER and DB_PASS

After all of this is done, you can run setup.py with
`python3 app/database/setup.py`. Look for a print statement indicating success.

Run the web server using uvicorn. *Make sure you're in the root directory when you do this*.

`uvicorn app.main:app --reload`

## Description

DataBass is a uniform and instrument rental system for our local high school marching band.

