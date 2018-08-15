from flask import Flask, request, render_template, session, flash, redirect, url_for, jsonify
from celery import Celery
from factories import TransactionFactory

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
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)