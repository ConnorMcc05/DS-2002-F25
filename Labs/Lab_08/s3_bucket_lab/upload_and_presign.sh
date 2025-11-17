#!/usr/bin/env bash

# Usage:
# ./upload_and_presign.sh LOCAL_FILE BUCKET_NAME EXPIRES_IN_SECONDS
# Example:
# ./upload_and_presign.sh mypic.png ds2002-f25-abc123 604800

set -euo pipefail

LOCAL_FILE="$1"
BUCKET="$2"
EXPIRES_IN="$3"

# Just the file name (strip any local path)
OBJECT_NAME="$(basename "$LOCAL_FILE")"

echo "Uploading $LOCAL_FILE to s3://$BUCKET/$OBJECT_NAME ..."
aws s3 cp "$LOCAL_FILE" "s3://$BUCKET/$OBJECT_NAME"

echo "Generating presigned URL (expires in $EXPIRES_IN seconds) ..."
aws s3 presign "s3://$BUCKET/$OBJECT_NAME" --expires-in "$EXPIRES_IN"
