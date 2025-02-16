# google_auth.py
import os
import pickle
import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the scopes needed for the YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def get_credentials():
    """
    Returns valid Google API credentials for the current session.
    Uses Streamlit session state to store the credentials so that each user is authenticated separately.
    """
    # Check if credentials are already stored in session state
    credentials = st.session_state.get("credentials", None)

    # If credentials exist and are valid, return them
    if credentials and credentials.valid:
        return credentials

    # Create the flow from the client secret file
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json',
                                                     scopes=SCOPES)

    # If we have credentials but they are expired and a refresh token is available, try to refresh them.
    if credentials and credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
        except Exception as e:
            st.error(f"Failed to refresh the access token: {e}")
            # Remove credentials from session state to force a new login.
            credentials = None

    # If no valid credentials are available, run the OAuth flow.
    if not credentials:
        credentials = flow.run_local_server(port=8080)

    # Save the credentials in session state
    st.session_state["credentials"] = credentials
    return credentials
