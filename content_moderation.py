import requests

def moderate_content(text):
    # Example using a hypothetical API for content moderation
    api_url = "https://api.contentmoderation.com/analyze"
    api_key = "YOUR_API_KEY"  # Replace with your API key

    response = requests.post(api_url, headers={"Authorization": f"Bearer {api_key}"}, json={"text": text})

    if response.status_code == 200:
        result = response.json()
        return result['is_appropriate']  # Assuming the API returns a field 'is_appropriate'
    else:
        raise Exception("Content moderation API error")

# Example usage
# try:
#     if moderate_content("some user-generated content"):
#         print("Content is appropriate")
#     else:
#         print("Content is inappropriate")
# except Exception as e:
#     print(f"Error: {e}")
