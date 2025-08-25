import streamlit as st
from streamlit_redirect import redirect

st.title("Example Redirect App")

st.write("")

st.divider()

st.write("Redirect to Google")
st.button("Redirect Me", on_click=redirect, args=("https://www.google.com",), icon="🚀")


st.divider()

st.write("Enter a URL in the textfield and press ENTER to redirect. URL must contain http:// or https://")

redirect_url = st.text_input("URL")

if redirect_url:
    redirect(redirect_url)
