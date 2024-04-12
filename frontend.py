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

    # Streamlit logo with padding
    col1, col2, col3 = st.columns([1, 20, 1])
    with col2:
        st.image("https://images.g2crowd.com/uploads/product/image/social_landscape/social_landscape_1233ef954d868794f19ce75837789fe8/g2.png", width=150)  # Replace with your logo URL

    # Team name with padding
    st.markdown("<h1 style='text-align: left; padding-left:500px;'>Team Name: Req&Resp</h1>", unsafe_allow_html=True)


    st.markdown("<h1 style='text-align: left; padding-left:430px;'>Product Description Generator</h2>", unsafe_allow_html=True)
    # st.title('Product Description Generator')

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
