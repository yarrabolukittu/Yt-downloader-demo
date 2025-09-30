import streamlit as st
from yt_dlp import YoutubeDL

st.set_page_config(page_title="YouTube Video Downloader", page_icon="🎬")
st.title("YouTube Video Downloader")

# --- PASSWORD PROTECTION ---
PASSWORD = "peddi"  # change this to whatever you want
password_input = st.text_input("Enter password to access the app:", type="password")

if password_input != PASSWORD:
    st.warning("❌ Incorrect password. Please enter the correct password to continue.")
else:
    # Input YouTube URL
    url = st.text_input("Enter YouTube URL:")

    if url:
        st.write("Fetching available formats...")

        # Step 1: Extract video info
        ydl_opts = {
            'quiet': True,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])

            # Step 2: Prepare dropdown list
            format_list = []
            for f in formats:
                if f.get('format_id'):
                    size = f.get('filesize') or f.get('filesize_approx')
                    if size:
                        size_mb = size / (1024 * 1024)
                        size_text = f"{size_mb:.1f} MB"
                    else:
                        size_text = "Unknown size"
                    format_list.append(f"{f['format_id']} - {f.get('format')} - {size_text}")

            # Step 3: Let user select quality
            choice = st.selectbox("Select Quality/Format", format_list)

            if st.button("Download"):
                selected_id = choice.split(" - ")[0]  # get format_id
                ydl_opts = {
                    'format': selected_id,
                    'outtmpl': '%(title)s.%(ext)s',
                    'quiet': False,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                }
                st.write("Downloading...")
                with YoutubeDL(ydl_opts) as ydl_download:
                    ydl_download.download([url])
                st.success("✅ Download Completed!")

        except Exception as e:
            st.error(f"Error: {e}")
