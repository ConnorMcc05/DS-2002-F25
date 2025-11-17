#!/usr/bin/env python3

import sys
import os
import urllib.request
import boto3

def main():
    if len(sys.argv) != 4:
        print("Usage: python s3_fetch_upload_presign.py <FILE_URL> <BUCKET_NAME> <EXPIRES_IN_SECONDS>")
        sys.exit(1)

    file_url = sys.argv[1]
    bucket_name = sys.argv[2]
    expires_in = int(sys.argv[3])

    # 1. Download file from the internet
    local_filename = os.path.basename(file_url.split("?")[0])  # strip query params if any
    print(f"Downloading {file_url} -> {local_filename}")
    urllib.request.urlretrieve(file_url, local_filename)

    # 2. Upload file to S3
    s3 = boto3.client("s3", region_name="us-east-1")
    object_name = local_filename  # key in S3

    print(f"Uploading {local_filename} to s3://{bucket_name}/{object_name}")
    s3.upload_file(
        Filename=local_filename,
        Bucket=bucket_name,
        Key=object_name
    )

    # 3. Generate presigned URL
    print(f"Generating presigned URL (expires in {expires_in} seconds)")
    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_name},
        ExpiresIn=expires_in
    )

    # 4. Output URL
    print("Presigned URL:")
    print(presigned_url)


if __name__ == "__main__":
    main()
