from celery import Celery


celery_app = Celery(
    'process_service',
    broker='amqp://admin:secret_pass@localhost:5672/',
    include=[
        'app.tasks.files_tasks',
    ]
)
