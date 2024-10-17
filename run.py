# run.py
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.debug = True  # Désactivez en production
    port = int(os.environ.get("PORT", 4000))
    app.run(host='0.0.0.0', port=port)
