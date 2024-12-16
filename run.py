import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Use host="0.0.0.0" to make the app accessible externally
    app.run(host="0.0.0.0", port=8080, debug=False)  # Debug mode off in production
    
    # app.run(debug=True) # for development 