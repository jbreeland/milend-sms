import logging
import azure.functions as func
import requests
import json
import os

def get_graph_token():
    tenant_id = "78e83a99-eab7-4401-9c77-c4f806f03f8f"
    client_id = "d0623837-4e45-4bd2-a9df-e17df6fcbad2"
    client_secret = "46a64807-52a9-4561-88ed-33914fa6fc07"

    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": client_id,
        "scope": "https://graph.microsoft.com/.default",
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def get_user_id(token, email):
    url = f"https://graph.microsoft.com/v1.0/users/{email}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["id"]

def create_chat(token, user_id):
    url = "https://graph.microsoft.com/v1.0/chats"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {
        "chatType": "oneOnOne",
        "members": [
            {
                "@odata.type": "#microsoft.graph.aadUserConversationMember",
                "roles": ["owner"],
                "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{user_id}')"
            }
        ]
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["id"]

def send_chat_message(token, chat_id, message_text):
    url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {
        "body": {
            "content": message_text
        }
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("SMS handler triggered.")

    try:
        raw_body = req.get_body().decode("utf-8")
        logging.info(f"Raw body: {raw_body}")
        data = req.get_json()

        text = data.get("text", "")
        from_number = data.get("from", {}).get("phone_number", "")
        to_number = data.get("to", [{}])[0].get("phone_number", "")

        full_message = f"Incoming SMS from {from_number} to {to_number}: {text}"

        token = get_graph_token()
        user_id = get_user_id(token, "jbreeland@milend.com")
        chat_id = create_chat(token, user_id)
        send_chat_message(token, chat_id, full_message)

        return func.HttpResponse("SMS forwarded to Teams", status_code=200)

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse("Failed", status_code=500)
