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

def chat_with_endpoint(questions, api_key, source_id):
    """Send chat messages sequentially to the API and format responses."""
    headers = {
        'x-api-key': api_key,
        "Content-Type": "application/json",
    }
    responses = []
    question_list = [question.strip() + " answer as verbosely as possible" for question in questions.split(',')]
    for i, question in enumerate(question_list, 1):
        data = {
            'sourceId': source_id,
            'messages': [{'role': "user", 'content': question}]
        }
        response = requests.post('https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)
        if response.status_code == 200:
            answer = response.json()['content']
            responses.append(f"Question #{i}: {question}\nAnswer #{i}: {answer}\n")
        else:
            responses.append(f"Error {response.status_code}: {response.text}\n")
    return "\n\n".join(responses)


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

    st.title("API Integration Example")

    # File upload section
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None and st.button("Upload File"):
        file_send_result = send_file(uploaded_file, api_key)
        st.write("File Send Result:", file_send_result)

    # Chat interface for multiple questions
    questions = st.text_area("Enter your questions, separated by commas:")
    if st.button("Send Messages"):
        chat_responses = chat_with_endpoint(questions, api_key, source_id)
        st.write("Chat Responses:", chat_responses)

    # Delete file
    if st.button("Delete File"):
        delete_result = delete_file(source_id, api_key)
        st.write("Delete Result:", delete_result)

if __name__ == "__main__":
    main()
