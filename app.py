import streamlit as st
from PIL import Image
import os
from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, concatenate_videoclips
from rembg import remove

st.set_page_config(page_title="Political Media Studio", layout="wide")
st.title("Daily Political Poster & Video Reel Studio")

mode = st.sidebar.radio("Select Tool", ["Poster Studio", "Video Reel Mixer"])

# ----------------- 1. POSTER STUDIO -----------------
if mode == "Poster Studio":
    st.header("Daily Political Poster Creation")

    col1, col2 = st.columns(2)
    with col1:
        subject_file = st.file_uploader("Upload Leader/Subject Photo", type=["png", "jpg", "jpeg"])
        auto_remove_bg = st.checkbox("Auto-remove background from leader photo", value=True)
        bg_file = st.file_uploader("Upload Background / Banner Base", type=["png", "jpg", "jpeg"])
        top_overlay = st.file_uploader("Upload Party Header / Logo Overlay (PNG)", type=["png"])

    with col2:
        if st.button("Generate Poster"):
            if not subject_file or not bg_file:
                st.warning("Please upload both a leader photo and a background image.")
            else:
                with st.spinner("Processing poster..."):
                    bg_img = Image.open(bg_file).convert("RGBA").resize((1080, 1350))
                    subj_img = Image.open(subject_file).convert("RGBA")

                    if auto_remove_bg:
                        subj_img = remove(subj_img)

                    subj_img.thumbnail((800, 800))
                    bg_img.paste(subj_img, (140, 550), subj_img)

                    if top_overlay:
                        overlay = Image.open(top_overlay).convert("RGBA").resize((1080, 250))
                        bg_img.paste(overlay, (0, 0), overlay)

                    st.image(bg_img, caption="Generated Poster", use_container_width=True)
                    output_poster = "final_poster.png"
                    bg_img.save(output_poster)

                    with open(output_poster, "rb") as file:
                        st.download_button("Download Poster", file, "poster.png", "image/png")

# ----------------- 2. VIDEO MIXER -----------------
elif mode == "Video Reel Mixer":
    st.header("10-Slot Video & Photo Reel Creator")

    tab_videos, tab_photos, tab_audio = st.tabs(["10 Video Slots", "10 Photo Slots", "Audio Track"])

    video_files = []
    with tab_videos:
        st.write("Upload up to 10 video clips:")
        v_cols = st.columns(5)
        for i in range(10):
            with v_cols[i % 5]:
                vf = st.file_uploader(f"Video {i+1}", type=["mp4", "mov"], key=f"vid_{i}")
                if vf:
                    video_files.append(vf)

    photo_files = []
    with tab_photos:
        st.write("Upload up to 10 photos to include in the video:")
        p_cols = st.columns(5)
        for i in range(10):
            with p_cols[i % 5]:
                pf = st.file_uploader(f"Photo {i+1}", type=["png", "jpg"], key=f"pho_{i}")
                if pf:
                    photo_files.append(pf)

    with tab_audio:
        audio_file = st.file_uploader("Upload Background Song/Music", type=["mp3", "wav"])
        photo_duration = st.slider("Photo Display Duration (seconds)", 1, 6, 3)

    if st.button("Mix and Render Video"):
        if not video_files and not photo_files:
            st.error("Please upload at least one video or photo.")
        else:
            with st.spinner("Processing clips and rendering reel..."):
                clips = []

                for idx, vf in enumerate(video_files):
                    temp_vpath = f"temp_v_{idx}.mp4"
                    with open(temp_vpath, "wb") as f:
                        f.write(vf.read())
                    clip = VideoFileClip(temp_vpath).resize(height=1920)
                    clips.append(clip)

                for idx, pf in enumerate(photo_files):
                    temp_ppath = f"temp_p_{idx}.png"
                    with open(temp_ppath, "wb") as f:
                        f.write(pf.read())
                    p_clip = ImageClip(temp_ppath).set_duration(photo_duration).resize(height=1920)
                    clips.append(p_clip)

                final_video = concatenate_videoclips(clips, method="compose")

                if audio_file:
                    temp_apath = "temp_audio.mp3"
                    with open(temp_apath, "wb") as f:
                        f.write(audio_file.read())
                    audio = AudioFileClip(temp_apath)
                    if audio.duration > final_video.duration:
                        audio = audio.subclip(0, final_video.duration)
                    final_video = final_video.set_audio(audio)

                output_path = "final_output.mp4"
                final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

                st.video(output_path)
                with open(output_path, "rb") as f:
                    st.download_button("Download Mixed Video", f, "mixed_video.mp4", "video/mp4")
