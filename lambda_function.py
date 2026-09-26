import json
import boto3
import urllib.parse

# Initialize the SNS client
sns_client = boto3.client('sns')

# PASTE YOUR SNS TOPIC ARN HERE
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    # Extract the bucket name and file name from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        # Format the email message
        message_text = f"Success! A new file named '{key}' was just uploaded to your S3 bucket '{bucket}'."
        
        # Send the email via SNS
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message_text,
            Subject='New Cloud Upload Alert!'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Notification sent successfully!')
        }
        
    except Exception as e:
        print(f"Error processing upload: {e}")
        raise e
