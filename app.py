import streamlit as st
from PIL import Image, ImageDraw, ImageOps, ImageFilter
import os
import requests
from io import BytesIO

st.set_page_config(page_title="BRS Media Studio - Tata Madhusudhan MLC", layout="wide", page_icon="🌸")

# --- DOWNLOAD GOOGLE ANEK TELUGU FONT ---
ANEK_BOLD_URL = "https://github.com/google/fonts/raw/main/ofl/anektelugu/AnekTelugu-Bold.ttf"
ANEK_REG_URL = "https://github.com/google/fonts/raw/main/ofl/anektelugu/AnekTelugu-Regular.ttf"
FONT_BOLD_PATH = "AnekTelugu-Bold.ttf"
FONT_REG_PATH = "AnekTelugu-Regular.ttf"

for url, path in [(ANEK_BOLD_URL, FONT_BOLD_PATH), (ANEK_REG_URL, FONT_REG_PATH)]:
    if not os.path.exists(path):
        try:
            r = requests.get(url, timeout=10)
            with open(path, "wb") as f:
                f.write(r.content)
        except Exception:
            pass

# --- BRS BRAND PALETTE ---
PINK_PRIMARY = "#E5007D"
PINK_DARK = "#99004F"
GOLD_COLOR = "#FFD700"

def make_circular_image(img, size=(160, 160), border_color="#FFD700", border_width=5):
    img = img.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
    mask = Image.new("L", size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, size[0], size[1]), fill=255)
    
    circular = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    circular.putalpha(mask)
    
    output = Image.new("RGBA", size, (0, 0, 0, 0))
    output.paste(circular, (0, 0), circular)
    
    draw_b = ImageDraw.Draw(output)
    draw_b.ellipse(
        (border_width // 2, border_width // 2, size[0] - border_width // 2, size[1] - border_width // 2),
        outline=border_color,
        width=border_width
    )
    return output

LEADER_FALLBACKS = {
    "kcr": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/K._Chandrashekar_Rao_in_2023.jpg/360px-K._Chandrashekar_Rao_in_2023.jpg",
    "ktr": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/K._T._Rama_Rao_in_2023.jpg/360px-K._T._Rama_Rao_in_2023.jpg",
    "harish": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/T._Harish_Rao_in_2023.jpg/360px-T._Harish_Rao_in_2023.jpg"
}

def load_image(file, fallback_key=None):
    if file is not None:
        return Image.open(file)
    if fallback_key:
        try:
            res = requests.get(LEADER_FALLBACKS[fallback_key], timeout=5)
            return Image.open(BytesIO(res.content))
        except Exception:
            pass
    return None

# --- SIDEBAR UI ---
st.sidebar.title("BRS Media Studio")
st.sidebar.markdown("**Sri Tata Madhusudhan Garu (MLC)**")
st.sidebar.caption("Khammam District BRS Graphic & Reel Creator")

mode = st.sidebar.radio("Select Creation Mode:", ["Poster Studio", "Video Reel Mixer"])

# ========================================================
# 1. POSTER STUDIO
# ========================================================
if mode == "Poster Studio":
    st.header("Daily Political Poster Studio")
    st.caption("Generate high-impact, AI-aesthetic BRS political posters with Anek Telugu typography.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Leader Photographs")
        tata_file = st.file_uploader("Upload Sri Tata Madhusudhan Photo", type=["png", "jpg", "jpeg"])
        erase_bg = st.checkbox("Auto-erase background (Cutout subject cleanly)", value=True)
        
        with st.expander("Top Leaders Custom Photos (Optional - Defaults auto-loaded)"):
            kcr_file = st.file_uploader("KCR Photo (Top-Left)", type=["png", "jpg"])
            ktr_file = st.file_uploader("KTR Photo (Top-Right)", type=["png", "jpg"])
            harish_file = st.file_uploader("Harish Rao Photo (Top-Right)", type=["png", "jpg"])
            custom_bg = st.file_uploader("Custom Poster Background Texture (Optional)", type=["png", "jpg"])

        st.subheader("2. Telugu Poster Typography")
        heading_text = st.text_input("Main Heading (శీర్షిక):", value="హృదయపూర్వక జన్మదిన శుభాకాంక్షలు")
        sub_text = st.text_area("Event/Quote Description (వివరణ):", value="తెలంగాణ ఉద్యమ సింహం, నిరంతరం ప్రజాసేవలో ముందంజ వేస్తూ, ఉమ్మడి ఖమ్మం జిల్లా ప్రజల ఆశాజ్యోతి గౌరవ శాసనమండలి సభ్యులు.")
        leader_title = st.text_input("Designation Ribbon:", value="శ్రీ తాతా మధుసూదన్ గారు, MLC")
        district_text = st.text_input("Sub-Designation:", value="బీఆర్ఎస్ పార్టీ జిల్లా అధ్యక్షులు, ఖమ్మం")
        greeting_text = st.text_input("Footer Greeting (శుభాకాంక్షలతో):", value="శుభాకాంక్షలతో: బీఆర్ఎస్ పార్టీ శ్రేణులు, ఉమ్మడి ఖమ్మం జిల్లా")

    with col2:
        st.subheader("3. Live Poster Preview & Export")
        if st.button("Generate High-End Poster", type="primary"):
            if not tata_file:
                st.warning("Please upload Sri Tata Madhusudhan Garu's photo.")
            else:
                with st.spinner("Removing background and compositing AI-grade graphic layout..."):
                    W, H = 1080, 1440
                    
                    # 1. Background Generation
                    if custom_bg:
                        canvas = Image.open(custom_bg).convert("RGBA").resize((W, H))
                    else:
                        # Studio-grade deep magenta/pink gradient
                        canvas = Image.new("RGBA", (W, H), (25, 0, 12, 255))
                        draw_grad = ImageDraw.Draw(canvas)
                        for y in range(H):
                            ratio = y / H
                            r = int(180 - (ratio * 150))
                            g = int(0 + (ratio * 10))
                            b = int(90 - (ratio * 60))
                            draw_grad.line([(0, y), (W, y)], fill=(r, g, b, 255))
                        
                        # Add warm golden flare glow at the center
                        flare = Image.new("RGBA", (600, 600), (255, 215, 0, 35))
                        flare_mask = Image.new("L", (600, 600), 0)
                        ImageDraw.Draw(flare_mask).ellipse((50, 50, 550, 550), fill=255)
                        flare_mask = flare_mask.filter(ImageFilter.GaussianBlur(80))
                        flare.putalpha(flare_mask)
                        canvas.paste(flare, (W//2 - 300, H//2 - 200), flare)

                    # 2. Top Banner Header
                    header = Image.new("RGBA", (W, 230), (0, 0, 0, 0))
                    draw_hdr = ImageDraw.Draw(header)
                    draw_hdr.rectangle([0, 0, W, 215], fill=(229, 0, 125, 240))
                    draw_hdr.rectangle([0, 215, W, 222], fill=(255, 215, 0, 255))
                    canvas.paste(header, (0, 0), header)

                    # 3. Top Badges (KCR, KTR, Harish Rao)
                    kcr_img = load_image(kcr_file, "kcr")
                    if kcr_img:
                        kcr_badge = make_circular_image(kcr_img, size=(175, 175), border_color="#FFD700", border_width=5)
                        canvas.paste(kcr_badge, (35, 20), kcr_badge)

                    ktr_img = load_image(ktr_file, "ktr")
                    if ktr_img:
                        ktr_badge = make_circular_image(ktr_img, size=(150, 150), border_color="#FFFFFF", border_width=4)
                        canvas.paste(ktr_badge, (W - 330, 30), ktr_badge)

                    harish_img = load_image(harish_file, "harish")
                    if harish_img:
                        harish_badge = make_circular_image(harish_img, size=(150, 150), border_color="#FFFFFF", border_width=4)
                        canvas.paste(harish_badge, (W - 165, 30), harish_badge)

                    # 4. Clean Background Removal & Madhusudhan Garu Placement
                    raw_subj = Image.open(tata_file).convert("RGBA")
                    if erase_bg:
                        try:
                            from rembg import remove
                            subj = remove(raw_subj)
                        except Exception:
                            subj = raw_subj
                    else:
                        subj = raw_subj

                    subj.thumbnail((780, 1050), Image.Resampling.LANCZOS)
                    sw, sh = subj.size

                    # Soft drop-shadow behind subject
                    shadow = Image.new("RGBA", (sw + 40, sh + 40), (0, 0, 0, 0))
                    shadow_mask = subj.split()[3].filter(ImageFilter.GaussianBlur(25))
                    shadow_layer = Image.new("RGBA", (sw, sh), (0, 0, 0, 180))
                    shadow_layer.putalpha(shadow_mask)
                    canvas.paste(shadow_layer, (W - sw - 10, H - sh - 220), shadow_layer)

                    # Paste leader cut-out
                    canvas.paste(subj, (W - sw - 20, H - sh - 230), subj)

                    # Save base image to render HTML/SVG layout with verified Anek Telugu shaping
                    temp_bg_path = "temp_poster_base.png"
                    canvas.save(temp_bg_path)

                    # 5. Composite Verified Telugu Typography (Anek Telugu Engine)
                    poster_html = f"""
                    <style>
                        @font-face {{
                            font-family: 'AnekTelugu';
                            src: url('https://fonts.gstatic.com/s/anektelugu/v8/jVjc7PH_28z4m0N1Q46mX2V91yQ.woff2') format('woff2');
                            font-weight: 700;
                        }}
                        @font-face {{
                            font-family: 'AnekTeluguLight';
                            src: url('https://fonts.gstatic.com/s/anektelugu/v8/jVjc7PH_28z4m0N1Q46mX2V91yQ.woff2') format('woff2');
                            font-weight: 500;
                        }}
                        .poster-card {{
                            position: relative;
                            width: 100%;
                            max-width: 620px;
                            margin: 0 auto;
                            box-shadow: 0 16px 40px rgba(0,0,0,0.5);
                            border-radius: 12px;
                            overflow: hidden;
                            background: #000;
                            line-height: 1.35;
                        }}
                        .base-img {{
                            width: 100%;
                            display: block;
                        }}
                        .top-title {{
                            position: absolute;
                            top: 6.5%;
                            left: 50%;
                            transform: translate(-50%, -50%);
                            font-family: 'AnekTelugu', sans-serif;
                            font-size: 24px;
                            color: #FFFFFF;
                            font-weight: 700;
                            letter-spacing: 0.5px;
                            text-shadow: 0 2px 4px rgba(0,0,0,0.4);
                            white-space: nowrap;
                        }}
                        .content-box {{
                            position: absolute;
                            top: 20%;
                            left: 5%;
                            width: 50%;
                            text-shadow: 0 3px 8px rgba(0,0,0,0.8);
                        }}
                        .main-heading {{
                            font-family: 'AnekTelugu', sans-serif;
                            font-size: 26px;
                            font-weight: 800;
                            color: #FFD700;
                            margin-bottom: 8px;
                        }}
                        .body-text {{
                            font-family: 'AnekTeluguLight', sans-serif;
                            font-size: 15px;
                            color: #FFFFFF;
                            font-weight: 500;
                        }}
                        .ribbon {{
                            position: absolute;
                            bottom: 0;
                            left: 0;
                            width: 100%;
                            background: linear-gradient(180deg, #E5007D 0%, #99004F 100%);
                            border-top: 4px solid #FFD700;
                            padding: 12px 10px 10px 10px;
                            text-align: center;
                            box-sizing: border-box;
                        }}
                        .leader-name {{
                            font-family: 'AnekTelugu', sans-serif;
                            font-size: 25px;
                            color: #FFD700;
                            font-weight: 800;
                            margin: 0;
                        }}
                        .district-name {{
                            font-family: 'AnekTelugu', sans-serif;
                            font-size: 15px;
                            color: #FFFFFF;
                            font-weight: 600;
                            margin-top: 2px;
                        }}
                        .footer-greeting {{
                            font-family: 'AnekTelugu', sans-serif;
                            font-size: 13px;
                            color: #FFE6F2;
                            font-weight: 500;
                            margin-top: 6px;
                            border-top: 1px solid rgba(255,255,255,0.25);
                            padding-top: 4px;
                        }}
                    </style>
                    <div class="poster-card">
                        <img src="data:image/png;base64,{}" class="base-img" />
                        <div class="top-title">భారత రాష్ట్ర సమితి (BRS)</div>
                        <div class="content-box">
                            <div class="main-heading">{heading_text}</div>
                            <div class="body-text">{sub_text}</div>
                        </div>
                        <div class="ribbon">
                            <div class="leader-name">{leader_title}</div>
                            <div class="district-name">{district_text}</div>
                            <div class="footer-greeting">{greeting_text}</div>
                        </div>
                    </div>
                    """
                    
                    import base64
                    with open(temp_bg_path, "rb") as f:
                        b64_bg = base64.b64encode(f.read()).decode("utf-8")

                    st.markdown(poster_html.format(b64_bg), unsafe_allow_html=True)
                    
                    # Direct download
                    with open(temp_bg_path, "rb") as f:
                        st.download_button("Download High-Resolution Base", f, "tata_madhusudhan_poster.png", "image/png")

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
                from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, concatenate_videoclips

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
