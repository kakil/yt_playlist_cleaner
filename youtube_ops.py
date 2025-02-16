# youtube_ops.py
import streamlit as st
from googleapiclient.discovery import build


def get_youtube_client(credentials):
    """
    Returns a YouTube API client built using the provided credentials.
    """
    return build('youtube', 'v3', credentials=credentials)


def remove_all_videos_from_playlist(youtube, playlist_id):
    """
    Removes all videos from the specified playlist.
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
            return False

        # Collect (playlist item id, video id) for each item
        items += [
            (item['id'], item['snippet']['resourceId']['videoId'])
            for item in response.get('items', [])
        ]
        request = youtube.playlistItems().list_next(request, response)

    st.write(f"Total videos in playlist: {len(items)}")

    if items:
        for item_id, video_id in items:
            try:
                youtube.playlistItems().delete(id=item_id).execute()
                st.write(f"Removed video {video_id}")
            except Exception as e:
                st.error(f"Failed to remove video {video_id}: {e}")
        return True
    else:
        st.info("No videos found in the playlist.")
        return False


def remove_video_from_playlist(youtube, playlist_id, video_id):
    """
    Removes a single video from the specified playlist.
    """
    # Retrieve the playlist item for the given video
    request = youtube.playlistItems().list(
        part="id",
        playlistId=playlist_id,
        videoId=video_id
    )
    response = request.execute()

    if response.get('items'):
        playlist_item_id = response['items'][0]['id']
        try:
            youtube.playlistItems().delete(id=playlist_item_id).execute()
            st.write(f"Removed video {video_id} from playlist.")
        except Exception as e:
            st.error(f"Error removing video {video_id}: {e}")
    else:
        st.info("Video not found in the playlist.")
