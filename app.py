from flask import Flask, request, make_response, session, flash, redirect, url_for, jsonify, Response
from celery import Celery
from factories import TransactionFactory
from json import dumps
import csv
from helpers import export_json_to_csv

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

def make_celery(app):
    celery = Celery(
        app.name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

# Celery Tasks
@celery.task()
def add_together(a, b):
    return a + b

# Task to queue  generation export
@celery.task()
def store_report_pdf(a, b):
    return a + b

# API Routes
@app.route('/')
def root():
    result = add_together.delay(23, 42)
    result.wait()  # 65
    return jsonify({'result': result.get()})

@app.route('/mock-transactions')
def mock_transactions():
    factory = TransactionFactory()
    factory.get_mock_transactions()
    return "<h1> Transactions have been mocked </h1>"

@app.route('/transactions')
def transactions():
    file = open('storage/transactions.json', 'r') 
    transactions_json = file.read().replace('\"', '')
    return jsonify(transactions_json)

@app.route('/transactions/csv')
def transactions_csv():
    csv_path = 'storage/reports/export.csv'    
    with open(csv_path, 'rb') as csv_file:
        transactions_csv = csv_file.read()
        return Response(transactions_csv, mimetype='text/csv')
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)