import os
import pickle
import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.auth.exceptions

# Define the scopes needed for the YouTube API
SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
]


def get_credentials():
    """
    Returns valid Google API credentials for the current session.
    Uses Streamlit session state to store the credentials so that each user is authenticated separately.
    """
    credentials = st.session_state.get("credentials", None)

    # If credentials exist and are valid, return them
    if credentials and credentials.valid:
        return credentials

    # Detect environment: Running locally vs. running on the VPS
    running_on_vps = os.getenv("RUNNING_ON_VPS", "false").lower() == "true"

    # Create the OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=SCOPES)

    if credentials and credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
        except Exception as e:
            st.error(f"Failed to refresh the access token: {e}")
            credentials = None  # Force re-login if refresh fails

    # If no valid credentials exist, start authentication
    if not credentials:
        if running_on_vps:
            # VPS Mode: Use console-based authentication (no browser popup)
            credentials = flow.run_console()
        else:
            # Local Mode: Open browser for OAuth
            credentials = flow.run_local_server(port=8080)

    # Store credentials in Streamlit session state
    st.session_state["credentials"] = credentials
    return credentials
