from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your service account key file
SERVICE_ACCOUNT_FILE = r'C:\Users\Peter\Blueprint\text\care-for-test\meta-strata-442816-s2-4f7cf8330314.json'

# Authenticate and construct service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

service = build('sqladmin', 'v1beta4', credentials=credentials)

# Define the instance details
instance_body = {
    "name": "care-for-test",
    "settings": {
        "tier": "db-f1-micro",
        "dataDiskSizeGb": 10,
        "dataDiskType": "PD_SSD",
        "activationPolicy": "ALWAYS",
        "ipConfiguration": {
            "ipv4Enabled": True
        }
    },
    "databaseVersion": "POSTGRES_13",
    "region": "europe-west2"
}

# Create the instance
project_id = 'meta-strata-442816-s2'
request = service.instances().insert(project=project_id, body=instance_body)
response = request.execute()

print(response)