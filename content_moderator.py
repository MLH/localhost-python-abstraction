import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import config
import re

# Request headers
headers = {
    "Content-Type": "text/plain",
    "Ocp-Apim-Subscription-Key": config.OCP_APIM_SUBSCRIPTION_KEY,
}

# Request params
params = {}

COGNITIVE_SERVICES_URL = "eastus.api.cognitive.microsoft.com"


def moderate(message):
    data = make_request_to_api(message.encode("utf8"))
    decoded_data = data.decode("utf-8")
    json_data = json.loads(decoded_data)
    terms = json_data["Terms"]

    if not terms or terms == None:
        return message
    else:
        for term in terms:
            pattern = re.compile(term["Term"], re.IGNORECASE)
            message = pattern.sub("[CENSORED]", message)
    return message


def make_request_to_api(message):
    content_moderator_connection = http.client.HTTPSConnection(COGNITIVE_SERVICES_URL)
    content_moderator_connection.request(
        "POST",
        "/contentmoderator/moderate/v1.0/ProcessText/Screen?%s" % params,
        message,
        headers,
    )

    response = content_moderator_connection.getresponse()
    data = response.read()
    content_moderator_connection.close()

    return data
