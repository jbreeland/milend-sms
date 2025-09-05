import logging
import azure.functions as func
import requests
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('SMS handler triggered.')

    try:
        req_body = req.get_json()
        logging.info(f"Raw body: {req_body}")
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON body",
            status_code=400
        )

    # Extract fields safely
    from_number = req_body.get("from")
    to_number = req_body.get("to")
    message_body = req_body.get("body")

    if not all([from_number, to_number, message_body]):
        return func.HttpResponse(
            "Missing required fields",
            status_code=400
        )

    logging.info(f"From: {from_number}, To: {to_number}, Body: {message_body}")

    # Example response or logic here
    return func.HttpResponse(
        "Message received successfully",
        status_code=200
    )
