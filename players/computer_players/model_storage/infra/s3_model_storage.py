import os

import boto3
import json

from botocore.exceptions import ClientError

from players.computer_players.model_storage.infra.base_model_storage import BaseModelStorage

class S3ModelStorage(BaseModelStorage):

    def __init__(self):
        s3_bucket = os.getenv("S3_BUCKET")
        s3_endpoint = os.getenv("S3_ENDPOINT")
        s3_access_key = os.getenv("S3_ACCESS_KEY")
        s3_secret_key = os.getenv("S3_SECRET_KEY")
        s3_region = os.getenv("S3_REGION")


        self.bucket = s3_bucket

        self.client = boto3.client(
            "s3",
            endpoint_url = s3_endpoint,
            aws_access_key_id = s3_access_key,
            aws_secret_access_key = s3_secret_key,
            region_name = s3_region,
        )

        self.ensure_bucket()

    def ensure_bucket(self):
        existing = [b["Name"] for b in self.client.list_buckets()["Buckets"]]
        if self.bucket not in existing:
            self.client.create_bucket(Bucket=self.bucket)        

    def save_model(self, path: str, data: bytes) -> None:
        self.client.put_object(
            Bucket=self.bucket,
            Key=path,
            Body=data
        )

    def load_model(self, path: str) -> bytes:
        try:
            obj = self.client.get_object(Bucket=self.bucket, Key=path)
            return obj["Body"].read()
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            else:
                raise e

    def save_metadata(self, path: str, metadata: dict) -> None:
        self.client.put_object(
            Bucket=self.bucket,
            Key=path,
            Body=json.dumps(metadata).encode("utf-8")
        )

    def load_metadata(self, path: str) -> dict:
        try:
            obj = self.client.get_object(Bucket=self.bucket, Key=path)
            return json.loads(obj["Body"].read().decode("utf-8"))
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            else:
                raise e