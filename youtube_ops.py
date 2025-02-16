import streamlit as st
from googleapiclient.discovery import build

def get_youtube_client(credentials):
    """
    Returns a YouTube API client built using the provided credentials.
    """
    return build('youtube', 'v3', credentials=credentials)

def remove_all_videos_from_playlist(youtube, playlist_id):
    """
    Removes all videos from the specified playlist and displays the success message above the video list.
    """
    items = []

    # Get the playlist items (maximum of 50 per request)
    request = youtube.playlistItems().list(
        part="id,snippet",
        playlistId=playlist_id,
        maxResults=50
    )

    while request:
        try:
            response = request.execute()
        except Exception as e:
            st.error(f"Error retrieving playlist items: {e}")
            return

        # Collect (playlist item id, video id) for each item
        items += [
            (item['id'], item['snippet']['resourceId']['videoId'])
            for item in response.get('items', [])
        ]
        request = youtube.playlistItems().list_next(request, response)

    if not items:
        st.info("No videos found in the playlist.")
        return

    # ✅ Display the success message first
    st.success(
        f"✅ Successfully removed {len(items)} videos from the playlist."
    )

    # ✅ Then display the list of removed videos
    st.write("### Deleted Videos:")

    for item_id, video_id in items:
        try:
            youtube.playlistItems().delete(id=item_id).execute()
            st.write(f"✅ Removed video: `{video_id}`")
        except Exception as e:
            st.error(f"Failed to remove video {video_id}: {e}")
