import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import requests
from io import BytesIO
from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, concatenate_videoclips
from rembg import remove

st.set_page_config(page_title="BRS Media Studio - Tata Madhusudhan MLC", layout="wide", page_icon="🌸")

# Fetch official Unicode Telugu Font for error-free script shaping
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/suranna/Suranna-Regular.ttf"
FONT_PATH = "Suranna-Telugu.ttf"
if not os.path.exists(FONT_PATH):
    try:
        resp = requests.get(FONT_URL, timeout=10)
        with open(FONT_PATH, "wb") as f:
            f.write(resp.content)
    except Exception:
        pass

# Official BRS Branding Colors
BRS_PINK = (229, 0, 125)
BRS_DARK_PINK = (180, 0, 95)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
BLACK = (20, 20, 20)

def make_circular_image(img, size=(160, 160), border_color=(255, 255, 255), border_width=4):
    img = img.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
    mask = Image.new("L", size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, size[0], size[1]), fill=255)
    
    circular_img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    circular_img.putalpha(mask)
    
    bordered = Image.new("RGBA", size, (0, 0, 0, 0))
    bordered.paste(circular_img, (0, 0), circular_img)
    draw_border = ImageDraw.Draw(bordered)
    draw_border.ellipse(
        (border_width // 2, border_width // 2, size[0] - border_width // 2, size[1] - border_width // 2),
        outline=border_color,
        width=border_width
    )
    return bordered

LEADER_FALLBACKS = {
    "kcr": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/K._Chandrashekar_Rao_in_2023.jpg/360px-K._Chandrashekar_Rao_in_2023.jpg",
    "ktr": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/K._T._Rama_Rao_in_2023.jpg/360px-K._T._Rama_Rao_in_2023.jpg",
    "harish": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/T._Harish_Rao_in_2023.jpg/360px-T._Harish_Rao_in_2023.jpg"
}

def load_or_fetch(uploaded_file, fallback_key):
    if uploaded_file is not None:
        return Image.open(uploaded_file)
    try:
        res = requests.get(LEADER_FALLBACKS[fallback_key], timeout=5)
        return Image.open(BytesIO(res.content))
    except Exception:
        fallback_img = Image.new("RGBA", (200, 200), BRS_PINK)
        d = ImageDraw.Draw(fallback_img)
        d.text((100, 100), fallback_key.upper(), fill=WHITE, anchor="mm")
        return fallback_img

st.sidebar.title("BRS Media Studio")
st.sidebar.markdown("**Sri Tata Madhusudhan Garu (MLC)**")
st.sidebar.caption("Khammam District BRS Media Generator")

mode = st.sidebar.radio("Select Creation Mode:", ["Poster Studio", "Video Reel Mixer"])

# ========================================================
# 1. POSTER STUDIO
# ========================================================
if mode == "Poster Studio":
    st.header("Daily Political Poster Studio")
    st.caption("Generate official BRS posters with verified Telugu script formatting.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Leader Photographs")
        tata_file = st.file_uploader("Upload Sri Tata Madhusudhan Photo (Main Subject)", type=["png", "jpg", "jpeg"])
        cutout_tata = st.checkbox("Auto-remove background from Tata Madhusudhan photo", value=True)
        
        with st.expander("Top Leaders Custom Overlays (Optional - Defaults auto-loaded)"):
            kcr_file = st.file_uploader("Custom KCR Photo (Top-Left)", type=["png", "jpg"])
            ktr_file = st.file_uploader("Custom KTR Photo (Top-Right)", type=["png", "jpg"])
            harish_file = st.file_uploader("Custom Harish Rao Photo (Top-Right)", type=["png", "jpg"])
            bg_file = st.file_uploader("Custom Poster Background (Optional)", type=["png", "jpg"])

        st.subheader("2. Telugu Poster Text (Editable)")
        telugu_heading = st.text_input("Main Telugu Heading:", value="హృదయపూర్వక శుభాకాంక్షలు")
        telugu_body = st.text_area("Telugu Description / Message:", value="తెలంగాణ ఉద్యమ నాయకుడు, ఖమ్మం జిల్లా బీఆర్ఎస్ పార్టీ అధ్యక్షులు, గౌరవ శాసనమండలి సభ్యులు (MLC)")
        telugu_leader_name = st.text_input("Main Designation Strip:", value="శ్రీ తాతా మధుసూదన్ గారు, MLC")
        telugu_greetings = st.text_input("Greetings Strip (Footer):", value="భారత రాష్ట్ర సమితి (BRS) శ్రేణులు, ఖమ్మం జిల్లా")

    with col2:
        st.subheader("3. Live Poster Preview & Export")
        if st.button("Generate Telugu Poster", type="primary"):
            with st.spinner("Rendering poster with high-resolution typography..."):
                W, H = 1080, 1440
                
                if bg_file:
                    poster = Image.open(bg_file).convert("RGBA").resize((W, H))
                else:
                    poster = Image.new("RGBA", (W, H), (255, 243, 247, 255))
                    draw_grad = ImageDraw.Draw(poster)
                    for y in range(H):
                        blend = y / H
                        r = int(255 - (blend * 20))
                        g = int(240 - (blend * 150))
                        b = int(245 - (blend * 90))
                        draw_grad.line([(0, y), (W, y)], fill=(r, g, b, 255))

                draw = ImageDraw.Draw(poster)

                # Top Header Ribbon
                draw.rectangle([0, 0, W, 210], fill=BRS_PINK)
                draw.rectangle([0, 205, W, 212], fill=GOLD)
                
                font_top = ImageFont.truetype(FONT_PATH, 52)
                draw.text((W // 2, 105), "భారత రాష్ట్ర సమితి (BRS)", fill=WHITE, font=font_top, anchor="mm")

                # Top Leaders Badges
                img_kcr = load_or_fetch(kcr_file, "kcr")
                kcr_badge = make_circular_image(img_kcr, size=(170, 170), border_color=GOLD, border_width=5)
                poster.paste(kcr_badge, (35, 20), kcr_badge)

                img_ktr = load_or_fetch(ktr_file, "ktr")
                ktr_badge = make_circular_image(img_ktr, size=(150, 150), border_color=WHITE, border_width=4)
                poster.paste(ktr_badge, (W - 325, 30), ktr_badge)

                img_harish = load_or_fetch(harish_file, "harish")
                harish_badge = make_circular_image(img_harish, size=(150, 150), border_color=WHITE, border_width=4)
                poster.paste(harish_badge, (W - 165, 30), harish_badge)

                # Tata Madhusudhan Main Portrait
                if tata_file is not None:
                    tata_img = Image.open(tata_file).convert("RGBA")
                    if cutout_tata:
                        tata_img = remove(tata_img)
                    
                    tata_img.thumbnail((720, 950), Image.Resampling.LANCZOS)
                    tw, th = tata_img.size
                    poster.paste(tata_img, (W - tw - 30, H - th - 210), tata_img)

                # Telugu Content Typography
                font_heading = ImageFont.truetype(FONT_PATH, 50)
                font_sub = ImageFont.truetype(FONT_PATH, 32)
                font_name = ImageFont.truetype(FONT_PATH, 48)
                font_footer = ImageFont.truetype(FONT_PATH, 34)

                draw.text((60, 260), telugu_heading, fill=BRS_DARK_PINK, font=font_heading)

                words = telugu_body.split()
                line = ""
                curr_y = 340
                for w in words:
                    test_str = f"{line} {w}".strip()
                    if draw.textlength(test_str, font=font_sub) < 520:
                        line = test_str
                    else:
                        draw.text((60, curr_y), line, fill=BLACK, font=font_sub)
                        curr_y += 45
                        line = w
                if line:
                    draw.text((60, curr_y), line, fill=BLACK, font=font_sub)

                # Bottom Designation Ribbon
                draw.rectangle([0, H - 210, W, H], fill=BRS_PINK)
                draw.rectangle([0, H - 215, W, H - 210], fill=GOLD)
                
                draw.text((W // 2, H - 140), telugu_leader_name, fill=GOLD, font=font_name, anchor="mm")
                draw.text((W // 2, H - 65), telugu_greetings, fill=WHITE, font=font_footer, anchor="mm")

                st.image(poster, caption="Generated Telugu Poster Preview", use_container_width=True)
                output_file = "tata_madhusudhan_poster.png"
                poster.convert("RGB").save(output_file, quality=95)

                with open(output_file, "rb") as f:
                    st.download_button(
                        label="Download Telugu HD Poster",
                        data=f,
                        file_name="tata_madhusudhan_poster.png",
                        mime="image/png"
                    )

# ========================================================
# 2. VIDEO REELS MIXER (10 Video + 10 Photo Slots)
# ========================================================
elif mode == "Video Reel Mixer":
    st.header("10-Slot Video & Photo Reel Mixer")
    st.caption("Upload up to 10 campaign videos, 10 campaign photos, and background Telugu party songs.")

    tab_v, tab_p, tab_a = st.tabs(["10 Video Slots", "10 Photo Slots", "Audio & Render Settings"])

    video_uploads = []
    with tab_v:
        st.write("Upload up to 10 Campaign / Speech Video Clips:")
        v_cols = st.columns(5)
        for i in range(10):
            with v_cols[i % 5]:
                v = st.file_uploader(f"Video Clip {i+1}", type=["mp4", "mov"], key=f"reel_v_{i}")
                if v:
                    video_uploads.append(v)

    photo_uploads = []
    with tab_p:
        st.write("Upload up to 10 Event / Campaign Photos:")
        p_cols = st.columns(5)
        for i in range(10):
            with p_cols[i % 5]:
                p = st.file_uploader(f"Photo {i+1}", type=["png", "jpg"], key=f"reel_p_{i}")
                if p:
                    photo_uploads.append(p)

    with tab_a:
        audio_file = st.file_uploader("Upload BRS Campaign Song / BGM (MP3 or WAV)", type=["mp3", "wav"])
        photo_display_time = st.slider("Photo Display Duration (seconds per image):", 1, 6, 3)

    if st.button("Mix and Render Reel", type="primary"):
        if not video_uploads and not photo_uploads:
            st.error("Please upload at least one video or photo to mix.")
        else:
            with st.spinner("Processing media tracks and stitching reel..."):
                clips = []

                for idx, v_item in enumerate(video_uploads):
                    v_tmp = f"temp_v_{idx}.mp4"
                    with open(v_tmp, "wb") as f:
                        f.write(v_item.read())
                    c = VideoFileClip(v_tmp).resize(width=1080)
                    clips.append(c)

                for idx, p_item in enumerate(photo_uploads):
                    p_tmp = f"temp_p_{idx}.png"
                    with open(p_tmp, "wb") as f:
                        f.write(p_item.read())
                    c = ImageClip(p_tmp).set_duration(photo_display_time).resize(width=1080)
                    clips.append(c)

                final_reel = concatenate_videoclips(clips, method="compose")

                if audio_file:
                    a_tmp = "temp_audio.mp3"
                    with open(a_tmp, "wb") as f:
                        f.write(audio_file.read())
                    bgm = AudioFileClip(a_tmp)
                    if bgm.duration > final_reel.duration:
                        bgm = bgm.subclip(0, final_reel.duration)
                    final_reel = final_reel.set_audio(bgm)

                output_reel_name = "tata_madhusudhan_mixed_reel.mp4"
                final_reel.write_videofile(output_reel_name, fps=24, codec="libx264", audio_codec="aac")

                st.video(output_reel_name)
                with open(output_reel_name, "rb") as f:
                    st.download_button(
                        label="Download Mixed Video Reel",
                        data=f,
                        file_name="tata_madhusudhan_mixed_reel.mp4",
                        mime="video/mp4"
                    )
