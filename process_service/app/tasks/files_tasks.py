from app.celery_app import celery_app
from app.services.storage_service import storage_service


@celery_app.task(
    name='process_service.process_file',
    queue='files_processing'
)
def process_file(file_name: str) -> None:
    file = storage_service.download_file(
        file_name=file_name
    )

    print(f'file size: {len(file)}')
