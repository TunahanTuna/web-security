# run.py
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Docker'da 0.0.0.0'da dinle
    app.run(host='0.0.0.0', port=5000, debug=True) 