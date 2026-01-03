run:
	uv run uvicorn main:app --host 0.0.0.0 --port 8000

run-celery: 
	uv run celery -A celery_app.app worker --loglevel=DEBUG

