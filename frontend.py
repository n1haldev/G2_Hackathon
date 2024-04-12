import streamlit as st
import requests

# Function to interact with the Flask server
def get_summary_from_server(url):
    server_url = "http://localhost:5000/"  # Change this to your server URL
    payload = {'url': url}
    response = requests.post(server_url, data=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get('Summarized Text', 'Error: No summarized text found.')
    else:
        return f"Error: {response.status_code}"

# Streamlit UI
def main():
    st.set_page_config(page_title='Req&Res', page_icon=None, layout='wide', initial_sidebar_state='auto')

    # Background image CSS
    background_image = '''
    <style>
    body {
        background-image: url("https://example.com/path/to/your/image.jpg");
        background-size: cover;
        background-repeat: no-repeat;
    }
    </style>
    '''
    st.markdown(background_image, unsafe_allow_html=True)

    st.title('Product Description Generator')

    # Input URL from user
    url = st.text_input('Enter URL:', 'https://aim-agency.com/')  # Default URL

    # Button to trigger summarization
    if st.button('Generate Description'):
        with st.spinner('Generating...'):
            summarized_text = get_summary_from_server(url)
            st.write('Generated Description:')
            st.write(summarized_text)

if __name__ == "__main__":
    main()
