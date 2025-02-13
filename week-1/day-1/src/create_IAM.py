import boto3
import json

class AWSIAMManager:
    def __init__(self, region="us-east-1"):
        self.iam_client = boto3.client("iam", region_name=region)

    def create_iam_user(self, user_name):
        """Creates an IAM user."""
        try:
            response = self.iam_client.create_user(UserName=user_name)
            print(f"User '{user_name}' created successfully.")
            return response
        except self.iam_client.exceptions.EntityAlreadyExistsException:
            print(f"User '{user_name}' already exists.")
            return None

    def attach_inline_policy(self, user_name, policy_name, policy_document):
        """Attaches an inline policy to the IAM user."""
        try:
            self.iam_client.put_user_policy(
                UserName=user_name,
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_document)
            )
            print(f"Inline policy '{policy_name}' attached to user '{user_name}' successfully.")
        except Exception as e:
            print(f"Error attaching inline policy: {e}")

    def attach_managed_policy(self, user_name, policy_arn):
        """Attaches a managed policy to the IAM user."""
        try:
            self.iam_client.attach_user_policy(
                UserName=user_name,
                PolicyArn=policy_arn
            )
            print(f"Managed policy '{policy_arn}' attached to user '{user_name}' successfully.")
        except Exception as e:
            print(f"Error attaching managed policy: {e}")

# AWS Configuration
AWS_REGION = "us-east-1"
USER_NAME = "test_user2"  # Creating only test_user2
INLINE_POLICY_NAME = "S3WriteOnlyPolicy"
MANAGED_POLICY_ARN = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"

# Inline policy document
INLINE_POLICY_DOCUMENT = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": "*"
        }
    ]
}

def main():
    iam_manager = AWSIAMManager(region=AWS_REGION)

    # Create IAM user
    iam_manager.create_iam_user(USER_NAME)

    # Attach inline policy
    iam_manager.attach_inline_policy(USER_NAME, INLINE_POLICY_NAME, INLINE_POLICY_DOCUMENT)

    # Attach managed policy
    iam_manager.attach_managed_policy(USER_NAME, MANAGED_POLICY_ARN)

if __name__ == "__main__":
    main()
