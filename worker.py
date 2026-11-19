import os
import json
import time
import boto3
import redis
import app as app_module
from my_project.auth.service.appointment_service import AppointmentService

SQS_QUEUE_URL = os.environ["SQS_QUEUE_URL"]
AWS_REGION = os.environ.get("AWS_REGION", "eu-north-1")
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

flask_app = getattr(app_module, "app", None) or app_module.create_app()
sqs = boto3.client("sqs", region_name=AWS_REGION)

try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=1)
except Exception:
    redis_client = None


def process_messages():
    service = AppointmentService()
    print(f"Worker started. Listening to {SQS_QUEUE_URL}...", flush=True)

    while True:
        try:
            resp = sqs.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=5,
                WaitTimeSeconds=20,
            )
            messages = resp.get("Messages", [])
            if not messages:
                continue

            with flask_app.app_context():
                for msg in messages:
                    receipt_handle = msg["ReceiptHandle"]
                    message_id = msg["MessageId"]
                    body = json.loads(msg["Body"])
                    idem_key = body.get("idempotency_key") or message_id
                    dedup_key = f"worker:processed:{idem_key}"

                    # Дедуплікація на рівні обробника (захист від at-least-once доставки SQS)
                    if redis_client is not None:
                        already_done = not redis_client.set(dedup_key, "1", nx=True, ex=86400)
                        if already_done:
                            print(f"Duplicate message skipped: {idem_key}", flush=True)
                            sqs.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt_handle)
                            continue

                    service.create(body["data"])
                    print(f"Processed appointment request_id={body.get('request_id')}", flush=True)

                    sqs.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt_handle)

        except Exception as e:
            print(f"Worker error: {e}", flush=True)
            time.sleep(2)


if __name__ == "__main__":
    process_messages()
