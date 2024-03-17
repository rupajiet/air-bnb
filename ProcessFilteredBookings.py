import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event))
    
    try:
        # Check if the event contains the payload in the expected location
        event_payload = extract_payload(event)
        if event_payload is None:
            logger.error("Payload not found in the event.")
            return {
                'statusCode': 400,
                'body': json.dumps('Payload not found')
            }

        # Extract relevant information from the event payload
        booking_info = {
            "bookingId": event_payload.get('bookingId', ''),
            "userId": event_payload.get('userId', ''),
            "propertyId": event_payload.get('propertyId', ''),
            "location": event_payload.get('location', ''),
            "startDate": event_payload.get('startDate', ''),
            "endDate": event_payload.get('endDate', ''),
            "price": event_payload.get('price', '')
        }

        # Construct S3 object key
        object_key = f"booking/{booking_info['bookingId']}.json"

        # Write booking information to S3 bucket
        s3.put_object(
            Bucket='rup-airbnb-booking-records',
            Key=object_key,
            Body=json.dumps(booking_info)
        )

        logger.info("Booking information successfully written to S3 bucket")
        return {
            'statusCode': 200,
            'body': json.dumps('Booking information successfully written to S3 bucket')
        }
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing event')
        }

def extract_payload(event):
    # Check if the event is a standard dict
    if isinstance(event, dict):
        return event.get('detail')  # Assuming the payload is under the 'detail' key
    elif isinstance(event, str):
        return json.loads(event)  # Assuming the event is a JSON string
    else:
        return None
