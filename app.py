import streamlit as st
from PIL import Image, ImageDraw, ImageOps, ImageFilter
import os
import requests
from io import BytesIO
import base64

st.set_page_config(page_title="BRS Media Studio - Tata Madhusudhan MLC", layout="wide", page_icon="🌸")

# Brand colors
BRS_PINK = "#E5007D"
BRS_DARK = "#99004F"
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

def auto_clean_portrait_bg(img, tolerance=35):
    """Erases smooth studio backdrop cleanly without downloading heavy 1GB models"""
    img = img.convert("RGBA")
    datas = img.getdata()
    # Sample corner backdrop color
    corner_pixel = datas[0]
    
    newData = []
    for item in datas:
        # Check difference from backdrop color
        diff = abs(item[0] - corner_pixel[0]) + abs(item[1] - corner_pixel[1]) + abs(item[2] - corner_pixel[2])
        if diff < tolerance:
            newData.append((255, 255, 255, 0))
        elif diff < tolerance + 25:
            # Soft edge blending
            alpha = int(255 * ((diff - tolerance) / 25))
            newData.append((item[0], item[1], item[2], alpha))
        else:
            newData.append(item)
            
    img.putdata(newData)
    return img

LEADER_FALLBACKS = {
    "kcr": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/K._Chandrashekar_Rao_in_2023.jpg/360px-K._Chandrashekar_Rao_in_2023.jpg",
    "ktr": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/K._T._Rama_Rao_in_2023.jpg/360px-K._T._Rama_Rao_in_2023.jpg",
    "harish": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/T._Harish_Rao_in_2023.jpg/360px-T._Harish_Rao_in_2023.jpg"
}

def load_leader_image(uploaded_file, fallback_key):
    if uploaded_file is not None:
        return Image.open(uploaded_file)
    try:
        res = requests.get(LEADER_FALLBACKS[fallback_key], timeout=5)
        return Image.open(BytesIO(res.content))
    except Exception:
        return Image.new("RGBA", (180, 180), (229, 0, 125, 255))

st.sidebar.title("BRS Media Studio")
st.sidebar.markdown("**Sri Tata Madhusudhan Garu (MLC)**")
st.sidebar.caption("Khammam District BRS Graphic & Reel Creator")

mode = st.sidebar.radio("Select Creation Mode:", ["Poster Studio", "Video Reel Mixer"])

# ========================================================
# 1. POSTER STUDIO
# ========================================================
if mode == "Poster Studio":
    st.header("Daily Political Poster Studio")
    st.caption("Generate official BRS posters with verified Anek Telugu typography.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Leader Photographs")
        tata_file = st.file_uploader("Upload Sri Tata Madhusudhan Photo", type=["png", "jpg", "jpeg"])
        erase_bg = st.checkbox("Auto-clean studio background (Cutout subject cleanly)", value=True)
        
        with st.expander("Top Leadership Custom Overlays (Optional)"):
            kcr_file = st.file_uploader("Custom KCR Photo (Top-Left)", type=["png", "jpg"])
            ktr_file = st.file_uploader("Custom KTR Photo (Top-Right)", type=["png", "jpg"])
            harish_file = st.file_uploader("Custom Harish Rao Photo (Top-Right)", type=["png", "jpg"])
            custom_bg = st.file_uploader("Custom Poster Background (Optional)", type=["png", "jpg"])

        st.subheader("2. Telugu Poster Typography (Editable)")
        heading_text = st.text_input("Main Telugu Heading:", value="హృదయపూర్వక జన్మదిన శుభాకాంక్షలు")
        sub_text = st.text_area("Telugu Description / Slogan:", value="తెలంగాణ ఉద్యమ నాయకుడు, నిరంతరం ప్రజాసేవలో ముందంజ వేస్తూ, ఉమ్మడి ఖమ్మం జిల్లా ప్రజల ఆశాజ్యోతి గౌరవ శాసనమండలి సభ్యులు.")
        leader_name = st.text_input("Designation Ribbon:", value="శ్రీ తాతా మధుసూదన్ గారు, MLC")
        district_name = st.text_input("Sub-Designation:", value="బీఆర్ఎస్ పార్టీ జిల్లా అధ్యక్షులు, ఖమ్మం")
        greeting_text = st.text_input("Footer Greeting:", value="శుభాకాంక్షలతో: బీఆర్ఎస్ పార్టీ శ్రేణులు, ఉమ్మడి ఖమ్మం జిల్లా")

    with col2:
        st.subheader("3. Live Poster Preview & Export")
        if st.button("Generate High-End Poster", type="primary"):
            if not tata_file:
                st.warning("Please upload Sri Tata Madhusudhan Garu's photo.")
            else:
                with st.spinner("Compositing poster layout..."):
                    W, H = 1080, 1440
                    
                    # Canvas background
                    if custom_bg:
                        canvas = Image.open(custom_bg).convert("RGBA").resize((W, H))
                    else:
                        canvas = Image.new("RGBA", (W, H), (25, 2, 14, 255))
                        draw_bg = ImageDraw.Draw(canvas)
                        for y in range(H):
                            ratio = y / H
                            r = int(195 - (ratio * 165))
                            g = int(0 + (ratio * 10))
                            b = int(105 - (ratio * 80))
                            draw_bg.line([(0, y), (W, y)], fill=(r, g, b, 255))
                            
                        # Ambient Golden Flare Glow
                        flare = Image.new("RGBA", (650, 650), (255, 215, 0, 35))
                        f_mask = Image.new("L", (650, 650), 0)
                        ImageDraw.Draw(f_mask).ellipse((50, 50, 600, 600), fill=255)
                        f_mask = f_mask.filter(ImageFilter.GaussianBlur(90))
                        flare.putalpha(f_mask)
                        canvas.paste(flare, (W//2 - 325, H//2 - 250), flare)

                    # Top Header Ribbon
                    header = Image.new("RGBA", (W, 230), (0, 0, 0, 0))
                    d_hdr = ImageDraw.Draw(header)
                    d_hdr.rectangle([0, 0, W, 215], fill=(229, 0, 125, 240))
                    d_hdr.rectangle([0, 215, W, 222], fill=(255, 215, 0, 255))
                    canvas.paste(header, (0, 0), header)

                    # Top Leadership Badges
                    img_kcr = load_leader_image(kcr_file, "kcr")
                    kcr_badge = make_circular_image(img_kcr, size=(175, 175), border_color="#FFD700", border_width=5)
                    canvas.paste(kcr_badge, (35, 20), kcr_badge)

                    img_ktr = load_leader_image(ktr_file, "ktr")
                    ktr_badge = make_circular_image(img_ktr, size=(150, 150), border_color="#FFFFFF", border_width=4)
                    canvas.paste(ktr_badge, (W - 330, 30), ktr_badge)

                    img_harish = load_leader_image(harish_file, "harish")
                    harish_badge = make_circular_image(img_harish, size=(150, 150), border_color="#FFFFFF", border_width=4)
                    canvas.paste(harish_badge, (W - 165, 30), harish_badge)

                    # Main Portrait: Sri Tata Madhusudhan Garu
                    raw_subj = Image.open(tata_file).convert("RGBA")
                    if erase_bg:
                        subj = auto_clean_portrait_bg(raw_subj)
                    else:
                        subj = raw_subj

                    subj.thumbnail((780, 1050), Image.Resampling.LANCZOS)
                    sw, sh = subj.size

                    # Soft drop shadow
                    if "A" in subj.getbands():
                        shadow_mask = subj.split()[3].filter(ImageFilter.GaussianBlur(25))
                        shadow_layer = Image.new("RGBA", (sw, sh), (0, 0, 0, 190))
                        shadow_layer.putalpha(shadow_mask)
                        canvas.paste(shadow_layer, (W - sw - 10, H - sh - 220), shadow_layer)

                    canvas.paste(subj, (W - sw - 20, H - sh - 230), subj)

                    temp_base = "temp_poster_base.png"
                    canvas.save(temp_base)

                    with open(temp_base, "rb") as img_f:
                        b64_base = base64.b64encode(img_f.read()).decode("utf-8")

                    css_block = (
                        "<style>"
                        "@import url('https://fonts.googleapis.com/css2?family=Anek+Telugu:wght@400;600;700;800&display=swap');"
                        ".poster-wrap { position: relative; width: 100%; max-width: 600px; margin: 0 auto; box-shadow: 0 20px 45px rgba(0,0,0,0.6); border-radius: 14px; overflow: hidden; background: #000; font-family: 'Anek Telugu', sans-serif; }"
                        ".poster-bg { width: 100%; display: block; }"
                        ".top-party-title { position: absolute; top: 6.8%; left: 50%; transform: translate(-50%, -50%); font-size: 24px; color: #FFFFFF; font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.6); white-space: nowrap; }"
                        ".text-content-zone { position: absolute; top: 22%; left: 6%; width: 50%; text-shadow: 0 3px 6px rgba(0,0,0,0.9); }"
                        ".main-title-text { font-size: 26px; font-weight: 800; color: #FFD700; line-height: 1.3; margin-bottom: 10px; }"
                        ".body-desc-text { font-size: 15px; font-weight: 600; color: #FFFFFF; line-height: 1.4; }"
                        ".bottom-ribbon { position: absolute; bottom: 0; left: 0; width: 100%; background: linear-gradient(180deg, #E5007D 0%, #8C0048 100%); border-top: 4px solid #FFD700; padding: 12px 10px 10px 10px; text-align: center; box-sizing: border-box; }"
                        ".ribbon-name { font-size: 24px; font-weight: 800; color: #FFD700; margin: 0; }"
                        ".ribbon-district { font-size: 14px; font-weight: 600; color: #FFFFFF; margin-top: 2px; }"
                        ".ribbon-greeting { font-size: 13px; font-weight: 500; color: #FFE6F2; margin-top: 6px; border-top: 1px solid rgba(255,255,255,0.25); padding-top: 4px; }"
                        "</style>"
                    )

                    body_html = (
                        f"{css_block}"
                        f"<div class='poster-wrap'>"
                        f"<img src='data:image/png;base64,{b64_base}' class='poster-bg' />"
                        f"<div class='top-party-title'>భారత రాష్ట్ర సమితి (BRS)</div>"
                        f"<div class='text-content-zone'>"
                        f"<div class='main-title-text'>{heading_text}</div>"
                        f"<div class='body-desc-text'>{sub_text}</div>"
                        f"</div>"
                        f"<div class='bottom-ribbon'>"
                        f"<div class='ribbon-name'>{leader_name}</div>"
                        f"<div class='ribbon-district'>{district_name}</div>"
                        f"<div class='ribbon-greeting'>{greeting_text}</div>"
                        f"</div></div>"
                    )

                    st.markdown(body_html, unsafe_allow_html=True)
                    
                    with open(temp_base, "rb") as f:
                        st.download_button("Download High-Resolution Base Poster", f, "tata_madhusudhan_poster.png", "image/png")

# ========================================================
# 2. VIDEO REELS MIXER (10 Video + 10 Photo Slots)
# ========================================================
elif mode == "Video Reel Mixer":
    st.header("10-Slot Video & Photo Reel Mixer")
    st.caption("Upload up to 10 campaign videos, 10 campaign photos, and background Telugu party songs.")

    tab_v, tab_p, tab_a = st.tabs(["10 Video Slots", "10 Photo Slots", "Audio & Render Settings"])

    video_uploads = []
    with tab_v:
        st.write("Upload up to 10 Campaign Video Clips:")
        v_cols = st.columns(5)
        for i in range(10):
            with v_cols[i % 5]:
                v = st.file_uploader(f"Video {i+1}", type=["mp4", "mov"], key=f"reel_v_{i}")
                if v:
                    video_uploads.append(v)

    photo_uploads = []
    with tab_p:
        st.write("Upload up to 10 Campaign Photos:")
        p_cols = st.columns(5)
        for i in range(10):
            with p_cols[i % 5]:
                p = st.file_uploader(f"Photo {i+1}", type=["png", "jpg"], key=f"reel_p_{i}")
                if p:
                    photo_uploads.append(p)

    with tab_a:
        audio_file = st.file_uploader("Upload BRS Campaign Song / BGM (MP3)", type=["mp3", "wav"])
        photo_display_time = st.slider("Photo Display Duration (seconds):", 1, 6, 3)

    if st.button("Mix and Render Reel", type="primary"):
        if not video_uploads and not photo_uploads:
            st.error("Please upload at least one video or photo.")
        else:
            with st.spinner("Processing media tracks and rendering reel..."):
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
