import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("SMS handler triggered.")
    try:
        data = req.get_json()
        message = data.get("text")
        sender = data.get("from", {}).get("phone_number")
        to_number = data.get("to", [{}])[0].get("phone_number")

        logging.info(f"Message from {sender} to {to_number}: {message}")
        return func.HttpResponse("Message processed successfully.", status_code=200)

    except Exception as e:
        logging.error(f"Error processing SMS: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
