import streamlit as st
import requests

def send_file(uploaded_file, api_key):
    """Send a file to the API."""
    url = 'https://api.chatpdf.com/v1/sources/add-file'
    headers = {'x-api-key': api_key}
    files = [
        ('file', (uploaded_file.name, uploaded_file, 'application/octet-stream'))
    ]
    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        return f"Source ID: {response.json()['sourceId']}"
    else:
        return f"Status {response.status_code}: {response.text}"

def chat_with_endpoint(message, api_key, source_id):
    """Send a chat message to the API and receive a response."""
    headers = {
        'x-api-key': api_key,
        "Content-Type": "application/json",
    }
    data = {
        'sourceId': source_id,
        "referenceSources": True ,
        'messages': [
        
            {
                'role': "user",
                'content': message + " " + "answer as verbosely as possible",
            }
        ]
    }
    response = requests.post('https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error {response.status_code}: {response.text}"

def delete_file(source_id, api_key):
    """Delete a file from the API."""
    url = 'https://api.chatpdf.com/v1/sources/delete'
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json',
    }
    data = {
        'sources': [source_id],
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return "Success"
    except requests.exceptions.RequestException as error:
        return f"Error: {str(error)}\nResponse: {error.response.text}"

def main():
    st.sidebar.title("API Configuration")
    api_key = st.sidebar.text_input("Enter your API Key", value="sec_xxxxxx")
    source_id = st.sidebar.text_input("Enter Source ID", value="src_xxxxxx")

    st.title("Ellevate Alpha Chat Interface")

    # File upload section
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None and st.button("Upload File"):
        file_send_result = send_file(uploaded_file, api_key)
        st.write("File Send Result:", file_send_result)

    # Chat interface
    user_input = st.text_input("Enter your message:")
    if st.button("Send Message"):
        chat_response = chat_with_endpoint(user_input, api_key, source_id)
        st.write("Chat Response:", chat_response)

    # Delete file
    if st.button("Delete File"):
        delete_result = delete_file(source_id, api_key)
        st.write("Delete Result:", delete_result)

if __name__ == "__main__":
    main()
