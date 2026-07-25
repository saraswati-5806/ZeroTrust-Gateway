import os
import datetime
import ibm_boto3
from ibm_botocore.client import Config

class IBMCOSLogger:
    def __init__(self):
        self.api_key = os.getenv("COS_API_KEY")
        self.service_instance_id = os.getenv("COS_SERVICE_INSTANCE_ID")
        self.bucket_name = os.getenv("COS_BUCKET_NAME", "zerotrust-access-logs")
        self.endpoint_url = os.getenv("COS_ENDPOINT", "https://s3.private.us.cloud-object-storage.appdomain.cloud")
        
        # Initialize COS client if credentials exist
        if self.api_key and self.service_instance_id:
            self.cos_client = ibm_boto3.client(
                "s3",
                ibm_api_key_id=self.api_key,
                ibm_service_instance_id=self.service_instance_id,
                config=Config(signature_version="oauth"),
                endpoint_url=self.endpoint_url
            )
        else:
            self.cos_client = None

    def log_event(self, event_name, user, details=""):
        timestamp = datetime.datetime.utcnow().isoformat()
        log_content = f"[{timestamp}] EVENT: {event_name} | USER: {user} | DETAILS: {details}\n"
        object_name = f"audit_logs/{datetime.datetime.utcnow().strftime('%Y-%m-%d')}/{timestamp}.log"

        if self.cos_client:
            try:
                self.cos_client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=log_content
                )
                return True
            except Exception as e:
                print(f"Failed to write audit log to IBM COS: {e}")
                return False
        else:
            print(f"[LOCAL DEV FALLBACK] {log_content}")
            return False

# Global instance for easy importing
cos_logger = IBMCOSLogger()