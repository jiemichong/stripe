# stripe


## How to run
1. Create and activate a new virtual environment

**MacOS / Unix**

```
python3 -m venv env
source env/bin/activate
```

**Windows (PowerShell)**

```
python3 -m venv env
.\env\Scripts\activate.bat
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Export and run the application

Change to the src directory

```
cd src
```

**MacOS / Unix**

```
export FLASK_APP=server.py
python3 -m flask run --port=4242
```

**Windows (PowerShell)**

```
$env:FLASK_APP=“server.py"
python3 -m flask run --port=4242
```

4. Go to `localhost:4242` to see the demo.

5. To use waitress as a WSGI server:
```
pip install waitress
waitress-serve --port 4242 server:app
```

