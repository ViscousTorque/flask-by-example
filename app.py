import os
import requests
import operator
import re
import nltk
import json
from flask import jsonify, redirect, url_for, render_template, request, Flask
from flask_sqlalchemy import SQLAlchemy
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from redis_config import q, conn
from rq.job import Job

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_SETTINGS'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

load_dotenv()
db = SQLAlchemy()
app = create_app()

# Import models AFTER initializing db
from models import Result, db

def count_and_save_words(url):
    errors = []
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        errors.append(f"Request failed: {str(e)}")
        print({"error": errors})
        return None  

    raw = BeautifulSoup(r.text, features="html.parser").get_text()
    nltk.data.path.append('./venv/nltk_data/')  
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)

    nonPunct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if nonPunct.match(w)]
    raw_word_count = Counter(raw_words)

    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    no_stop_words_count = Counter(no_stop_words)

    with app.app_context():
        try:
            result = Result(
                url=url,
                result_all=raw_word_count,
                result_no_stop_words=no_stop_words_count
            )
            db.session.add(result)
            db.session.commit()
            return result.id  
        except Exception as e:
            db.session.rollback()
            errors.append(f"Database error: {str(e)}")
            print({"error": errors})
            return None

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        result = Result.query.filter_by(id=job.result).first()
        results = sorted(
            result.result_no_stop_words.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:10]
        return jsonify(results)
    else:
        return "Nay!", 202
    
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def get_counts():
    data = json.loads(request.data.decode())
    url = data["url"]
    if not url[:8].startswith(('https://', 'http://')):
        url = 'http://' + url
    job = q.enqueue_call(
        func=count_and_save_words, args=(url,), result_ttl=5000
    )
    return job.get_id()


if __name__ == '__main__':
    app.run()
