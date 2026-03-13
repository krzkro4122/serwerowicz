import os
import django
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# 1. Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'serwerowicz.settings')
django.setup()

def test_s3_integration():
    file_name = "s3_test_file.txt"
    content = b"Hello S3! This is a test from Django settings."

    print(f"--- Starting S3 Test for Bucket: {getattr(django.conf.settings, 'AWS_STORAGE_BUCKET_NAME', 'Not Found')} ---")

    try:
        # 2. Test Upload
        print(f"Attempting to upload '{file_name}'...")
        path = default_storage.save(file_name, ContentFile(content))
        print(f"Successfully uploaded to: {path}")

        # 3. Test Read/Exists
        if default_storage.exists(path):
            print("Verified: File exists on S3.")
            with default_storage.open(path, 'rb') as f:
                data = f.read()
                if data == content:
                    print("Verified: File content matches.")
                else:
                    print("Error: File content mismatch!")

        # 4. Test Delete (Cleanup)
        print(f"Deleting test file '{path}'...")
        default_storage.delete(path)

        if not default_storage.exists(path):
            print("Successfully cleaned up test file.")
            print("\nResult: S3 Settings are working perfectly!")
        else:
            print("Warning: Cleanup failed, file still exists.")

    except Exception as e:
        print(f"\n[!] ERROR: {str(e)}")
        print("Check your AWS credentials, bucket name, and region in settings.py.")

if __name__ == "__main__":
    test_s3_integration()
