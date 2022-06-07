import uvicorn
import os
from app.backend.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # os.system("streamlit run frontend/write_page_in_progress.py --server.port 30001")