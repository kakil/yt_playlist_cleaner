import streamlit as st
from google_auth import get_credentials
from youtube_ops import get_youtube_client, remove_all_videos_from_playlist
import requests


# ✅ Set Streamlit Page Title
st.set_page_config(page_title="YouTube Playlist Cleaner", page_icon="🎬")

# ✅ App Header
st.title("🎬 YouTube Playlist Cleaner")

# ✅ Instructions Section
st.markdown("""
## 📝 How to Use This App

1. **Sign in with Google** – Click the **"Sign in with Google"** button below to authenticate.
2. **Enter the Playlist ID** – Copy and paste the ID of the YouTube playlist you want to clean.
   - The **playlist ID** is the part after `list=` in a YouTube playlist URL.
   - Example: If your playlist URL is:
     ```
     https://www.youtube.com/playlist?list=PLabcd1234xyz
     ```
     Then the **Playlist ID** is `PLabcd1234xyz`.
3. **Click "Remove Videos"** – The app will remove all videos from the playlist and display the deleted videos.
4. **Wait for Confirmation** – The app will list all deleted videos after processing.

⚠️ **Note:** This action is **permanent** and cannot be undone.
""")

# ✅ Add a "Sign in with Google" Button
st.subheader("🔐 Sign in to Continue")

# Initialize user_authenticated before any condition
user_authenticated = False

# Check if user is already authenticated
credentials = st.session_state.get("credentials", None)

# Check if credentials exist and refresh if expired
if credentials and credentials.expired and credentials.refresh_token:
    try:
        credentials.refresh(Request())
    except Exception as e:
        st.error(f"Failed to refresh credentials: {e}")
        user_authenticated = False


if credentials and credentials.valid:
    user_authenticated = True
    try:
        # ✅ Fetch user info from Google's OAuth2 API
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {credentials.token}"}
        response = requests.get(user_info_url, headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            user_email = user_data.get("email", "Unknown User")
            st.success(f"✅ Signed in as: **{user_email}**")
        else:
            st.error("⚠️ Failed to retrieve user info. Please reauthenticate.")
            user_authenticated = False
    except Exception as e:
        st.error(f"⚠️ Error retrieving user info: {e}")
        user_authenticated = False


# Show login button if not authenticated
if not user_authenticated:
    if st.button("🔑 Sign in with Google"):
        credentials = get_credentials()
        st.session_state["credentials"] = credentials
        st.rerun()  # Refresh the page after login

# ✅ Only show the input field if the user is authenticated
if user_authenticated:
    st.subheader("🎥 Enter Your Playlist ID")

    playlist_id = st.text_input(
        "Enter your YouTube Playlist ID:",
        placeholder="e.g., PLabcd1234xyz"
    )

    if st.button("🗑️ Remove Videos"):
        # Build the YouTube client using the credentials
        youtube = get_youtube_client(credentials)

        # Remove all videos from the provided playlist ID
        with st.spinner("Deleting videos from the playlist... Please wait."):
            remove_all_videos_from_playlist(youtube, playlist_id)
