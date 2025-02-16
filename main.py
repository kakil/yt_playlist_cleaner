# main.py
import streamlit as st
from google_auth import get_credentials
from youtube_ops import get_youtube_client, remove_all_videos_from_playlist

st.title("YouTube Playlist Video Remover")

# Input field for the user to enter the playlist ID
playlist_id = st.text_input("Enter playlist id:")

if st.button("Remove Videos"):
    # Get user credentials via our auth module
    credentials = get_credentials()

    # Build the YouTube client using the credentials
    youtube = get_youtube_client(credentials)

    # Remove all videos from the provided playlist id
    with st.spinner('Deleting videos from the playlist... Please wait.'):
        result = remove_all_videos_from_playlist(youtube, playlist_id)

    if result:
        st.success(
            "All videos have been successfully removed from the playlist.")
    else:
        st.error("Failed to remove videos from the playlist.")
