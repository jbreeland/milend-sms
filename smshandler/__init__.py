import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("SMS handler triggered.")

    try:
        # Log raw body
        raw_body = req.get_body().decode("utf-8")
        logging.info(f"Raw body: {raw_body}")

        data = req.get_json()

        text = data.get("text", "")
        from_number = data.get("from", {}).get("phone_number", "")
        to_number = data.get("to", [{}])[0].get("phone_number", "")

        logging.info(f"Message from {from_number} to {to_number}: {text}")

        return func.HttpResponse("SMS processed", status_code=200)

    except Exception as e:
        logging.error(f"Error processing SMS: {str(e)}")
        return func.HttpResponse("Error processing SMS", status_code=400)
