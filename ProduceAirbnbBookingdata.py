import json
import boto3
import uuid
from datetime import datetime, timedelta

def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/843334912286/AirbnbBookingQueue'  # Replace 'YOUR_AIRBNB_BOOKING_QUEUE_URL' with the actual URL of your SQS queue

    # Generate mock data
    booking_id = str(uuid.uuid4())
    user_id = "UserID"
    property_id = "PropertyID"
    location = "City, Country"
    start_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    price = "100"  # Example price in USD

    # Create booking data dictionary
    booking_data = {
        "bookingId": booking_id,
        "userId": user_id,
        "propertyId": property_id,
        "location": location,
        "startDate": start_date,
        "endDate": end_date,
        "price": price
    }

    # Publish data to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(booking_data)
    )

    print("Message published to SQS:", response)

    return {
        'statusCode': 200,
        'body': json.dumps('Message published successfully to SQS!')
    }
