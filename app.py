from flask import Flask, request, render_template, session, flash, redirect, url_for, jsonify

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

from celery import Celery

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

@celery.task()
def add_together(a, b):
    return a + b

@app.route('/')
def root():
    result = add_together.delay(23, 42)
    result.wait()  # 65
    return jsonify({'result': result.get()})

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)