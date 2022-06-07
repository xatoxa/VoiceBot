import requests
import json


def create_token(oauth_token):
	params = {'yandexPassportOauthToken': oauth_token}
	response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', params=params)
	decode_response = response.content.decode('UTF-8')
	text = json.loads(decode_response)
	iam_token = text.get('iamToken')
	expires_iam_token = text.get('expiresAt')

	return iam_token, expires_iam_token
