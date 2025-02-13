import os
from rq import Worker, Queue
from redis_config import conn
from app import create_app
from models import db

listen = ['default']

# ✅ Create Flask app instance properly
app = create_app()

if __name__ == '__main__':
    print("Starting worker...")

    # ✅ Ensures the worker has Flask context
    with app.app_context():
        worker = Worker([Queue(name, connection=conn) for name in listen], connection=conn)
        worker.work()


