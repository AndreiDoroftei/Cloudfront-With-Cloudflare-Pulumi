from imports import json, aws, FileAsset, mimetypes, os

PulumiBucket = aws.s3.Bucket("PulumiBucket", acl="public-read")
content_dir = "assets"
for file in os.listdir(content_dir):
    filepath = os.path.join(content_dir, file)
    mime_type, _ = mimetypes.guess_type(filepath)
    obj = aws.s3.BucketObject(
        file, bucket=PulumiBucket.id, source=FileAsset(filepath), content_type=mime_type
    )


def public_read_policy_for_bucket(bucket_name):
    return json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [
                        f"arn:aws:s3:::{bucket_name}/*",
                    ],
                }
            ],
        }
    )


bucket_name = PulumiBucket.id
bucket_policy = aws.s3.BucketPolicy(
    "bucket-policy",
    bucket=bucket_name,
    policy=bucket_name.apply(public_read_policy_for_bucket),
)
