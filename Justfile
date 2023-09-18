# Justfile
default:
    @just --list

flask-run:
    #!/usr/bin/env bash
    source .venv/bin/activate &&
    export FLASK_APP=app.py &&
    export FLASK_ENV=development &&
    export FLASK_DEBUG=1 &&
    flask run

tailwindcss-watch:
    #!/usr/bin/env bash
    source .venv/bin/activate &&
    tailwindcss -i ./static/src/main.css -o ./static/dist/main.css --minify --watch

test:
    #!/usr/bin/env bash
    source .venv/bin/activate &&
    pytest tests/