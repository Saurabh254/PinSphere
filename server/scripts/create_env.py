from pathlib import Path

# Define your environment variables with placeholders
env_variables = """
# Redis
REDIS_DSN=<your_redis_dsn_here>

# Authentication
ALGORITHM=<your_algorithm_here>
AUTH_SECRET=<your_auth_secret_here>

# AWS
AWS_STORAGE_BUCKET_NAME=<your_bucket_name_here>
AWS_REGION=<your_aws_region_here>
AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key_here>
AWS_ACCESS_KEY_ID=<your_aws_access_key_id_here>
AWS_SESSION_TOKEN=<your_aws_session_token_here>
AWS_SIGNATURE_VERSION=<your_aws_signature_version_here>

# Token Expiration
REFRESH_TOKEN_EXPIRATION_SECONDS=<your_refresh_token_expiration_here>

# AWS Endpoint
AWS_ENDPOINT_URL=<your_aws_endpoint_url_here>

# Celery
CELERY_QUEUE_URL=<your_celery_queue_url_here>

# Environment
ENVIRONMENT=<your_environment_here>

# Google OAuth2
GOOGLE_OAUTH2_CLIENT_ID=<your_google_oauth2_client_id_here>
GOOGLE_OAUTH2_CLIENT_SECRET=<your_google_oauth2_client_secret_here>
GOOGLE_OAUTH2_REDIRECT_URI=<your_google_oauth2_redirect_uri_here>

# SBERT Model
SBERT_MODEL_NAME=<your_sbert_model_name_here>
"""

def create_env_file():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        print(".env file already exists!")
    else:
        with open(env_path, "w") as f:
            f.write(env_variables.strip())
        print(".env file created successfully!")

if __name__ == "__main__":
    create_env_file()
