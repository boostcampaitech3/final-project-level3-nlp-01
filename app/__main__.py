import uvicorn
import argparse

from app.backend.main import app

parser = argparse.ArgumentParser(description='클라우드에 있는 DB 관련 정보를 받습니다.')
parser.add_argument('--url', required=True, help="DB의 url")
parser.add_argument('--port', required=True, help="DB의 port")
parser.add_argument('--db_name', required=True, help="DB의 테이블 이름")
args = parser.parse_args()
URL = args.url
PORT = int(args.port)
DB_NAME = args.db_name

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)