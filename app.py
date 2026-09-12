import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import requests
from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, concatenate_videoclips
from rembg import remove

st.set_page_config(page_title="BRS Media Studio - Tata Madhusudhan", layout="wide", page_icon="🌸")

# Download authentic Telugu Unicode Font (Suranna)
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/suranna/Suranna-Regular.ttf"
FONT_PATH = "Suranna-Telugu.ttf"
if not os.path.exists(FONT_PATH):
    resp = requests.get(FONT_URL)
    with open(FONT_PATH, "wb") as f:
        f.write(resp.content)

# BRS Color Branding
BRS_PINK = (229, 0, 125)        # #E5007D
BRS_DARK_PINK = (180, 0, 95)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
BLACK = (20, 20, 20)

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Bharat_Rashtra_Samithi_flag.svg/320px-Bharat_Rashtra_Samithi_flag.svg.png", width=120)
st.sidebar.title("BRS డిజిటల్ స్టూడియో")
st.sidebar.markdown("**తాతా మధుసూదన్ MLC** గారి ప్రచార మాధ్యమ వేదిక")
mode = st.sidebar.radio("ఎంపిక చేసుకోండి (Select Feature):", ["పోస్టర్ మేకర్ (Poster Studio)", "వీడియో రీల్స్ మిక్సర్ (Video Reels Mixer)"])

# ==========================================
# 1. TELUGU POLITICAL POSTER STUDIO
# ==========================================
if mode == "పోస్టర్ మేకర్ (Poster Studio)":
    st.markdown("<h2 style='color:#E5007D;'>🌸 భారత రాష్ట్ర సమితి (BRS) - డైలీ పొలిటికల్ పోస్టర్ స్టూడియో</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. ఫొటోలు & వివరాలు (Inputs)")
        leader_img_file = st.file_uploader("తాతా మధుసూదన్ గారి ఫొటో / నాయకుడి ఫొటో", type=["png", "jpg", "jpeg"])
        cutout_bg = st.checkbox("ఫొటో బ్యాక్‌గ్రౌండ్ ఆటోమేటిక్‌గా తొలగించు (Auto Remove Background)", value=True)
        
        party_header_file = st.file_uploader("BRS టాప్ లీడర్స్ బ్యానర్ / KCR-KTR Frame (ఐచ్ఛికం)", type=["png", "jpg"])
        custom_bg_file = st.file_uploader("కస్టమ్ బ్యాక్‌గ్రౌండ్ వాల్‌పేపర్ (ఐచ్ఛికం)", type=["png", "jpg"])
        
        st.subheader("2. తెలుగు టెక్స్ట్ వివరాలు (Poster Text)")
        title_text = st.text_input("ముఖ్య శీర్షిక (Main Heading):", value="హృదయపూర్వక జన్మదిన శుభాకాంక్షలు")
        sub_text = st.text_area("సందేశం / ఉప శీర్షిక (Message/Details):", value="తెలంగాణ ఉద్యమ నాయకుడు, ఖమ్మం జిల్లా బీఆర్ఎస్ పార్టీ అధ్యక్షులు, గౌరవ శాసనమండలి సభ్యులు (MLC)")
        leader_name = st.text_input("నాయకుడి పేరు (Designation):", value="శ్రీ తాతా మధుసూదన్ గారు, MLC")
        greetings_from = st.text_input("శుభాకాంక్షలతో (Greeting By):", value="బీఆర్ఎస్ పార్టీ శ్రేణులు, ఖమ్మం జిల్లా")

    with col2:
        st.subheader("3. లైవ్ ప్రివ్యూ & డౌన్‌లోడ్")
        if st.button("🌸 HD పోస్టర్ సృష్టించండి (Generate Poster)"):
            with st.spinner("పోస్టర్ తయారవుతోంది..."):
                W, H = 1080, 1440
                
                # Canvas background
                if custom_bg_file:
                    poster = Image.open(custom_bg_file).convert("RGBA").resize((W, H))
                else:
                    # Default royal gradient/pink BRS background
                    poster = Image.new("RGBA", (W, H), (255, 240, 245, 255))
                    draw_grad = ImageDraw.Draw(poster)
                    for y in range(H):
                        blend = y / H
                        r = int(255 - (blend * 30))
                        g = int(240 - (blend * 180))
                        b = int(245 - (blend * 120))
                        draw_grad.line([(0, y), (W, y)], fill=(r, g, b, 255))
                
                # Layer top header frame
                if party_header_file:
                    top_banner = Image.open(party_header_file).convert("RGBA").resize((W, 260))
                    poster.paste(top_banner, (0, 0), top_banner)
                else:
                    # Built-in BRS Ribbon Header
                    draw = ImageDraw.Draw(poster)
                    draw.rectangle([0, 0, W, 180], fill=BRS_PINK)
                    font_hdr = ImageFont.truetype(FONT_PATH, 56)
                    draw.text((W//2, 90), "భారత రాష్ట్ర సమితి (BRS)", fill=WHITE, font=font_hdr, anchor="mm")
                
                # Subject image processing
                if leader_img_file:
                    subj = Image.open(leader_img_file).convert("RGBA")
                    if cutout_bg:
                        subj = remove(subj)
                    
                    # Position subject properly on bottom-right/center
                    subj.thumbnail((720, 950), Image.Resampling.LANCZOS)
                    subj_w, subj_h = subj.size
                    poster.paste(subj, (W - subj_w - 40, H - subj_h - 220), subj)
                
                # Bottom ribbon for Name & Designation
                draw = ImageDraw.Draw(poster)
                draw.rectangle([0, H - 220, W, H], fill=BRS_PINK)
                draw.rectangle([0, H - 230, W, H - 220], fill=GOLD)
                
                # Authentic Telugu text rendering with Raqm/Harfbuzz
                font_title = ImageFont.truetype(FONT_PATH, 54)
                font_name = ImageFont.truetype(FONT_PATH, 50)
                font_sub = ImageFont.truetype(FONT_PATH, 32)
                font_greet = ImageFont.truetype(FONT_PATH, 34)
                
                # Main Heading on Top-Left
                draw.text((60, 240), title_text, fill=BRS_DARK_PINK, font=font_title)
                
                # Subtext wrap
                words = sub_text.split()
                line = ""
                y_offset = 320
                for w in words:
                    test_line = f"{line} {w}".strip()
                    if draw.textlength(test_line, font=font_sub) < 550:
                        line = test_line
                    else:
                        draw.text((60, y_offset), line, fill=BLACK, font=font_sub)
                        y_offset += 45
                        line = w
                if line:
                    draw.text((60, y_offset), line, fill=BLACK, font=font_sub)
                
                # Leader name & Greeting in bottom strip
                draw.text((W//2, H - 150), leader_name, fill=GOLD, font=font_name, anchor="mm")
                draw.text((W//2, H - 70), greetings_from, fill=WHITE, font=font_greet, anchor="mm")
                
                # Display output
                st.image(poster, caption="తయారైన BRS పోస్టర్ (Ready)", use_container_width=True)
                out_path = "brs_tata_poster.png"
                poster.convert("RGB").save(out_path, quality=95)
                
                with open(out_path, "rb") as f:
                    st.download_button("📥 HD పోస్టర్ డౌన్‌లోడ్ చేసుకోండి", f, "tata_madhusudhan_brs_poster.png", "image/png")

# ==========================================
# 2. 10-SLOT BRS VIDEO REELS MIXER
# ==========================================
elif mode == "వీడియో రీల్స్ మిక్సర్ (Video Reels Mixer)":
    st.markdown("<h2 style='color:#E5007D;'>🎬 10-స్లాట్స్ BRS రీల్స్ & వీడియో మిక్సర్</h2>", unsafe_allow_html=True)
    
    tab_v, tab_p, tab_a = st.tabs(["10 వీడియో స్లాట్లు", "10 ఫొటో స్లాట్లు", "BRS బ్యాక్‌గ్రౌండ్ సాంగ్"])
    
    videos = []
    with tab_v:
        st.write("ప్రచార / కార్యక్రమ వీడియో క్లిప్‌లు (10 Slots):")
        cols1 = st.columns(5)
        for i in range(10):
            with cols1[i % 5]:
                vf = st.file_uploader(f"వీడియో {i+1}", type=["mp4", "mov"], key=f"brs_v_{i}")
                if vf:
                    videos.append(vf)
                    
    photos = []
    with tab_p:
        st.write("కార్యక్రమ ఫొటోలు (10 Slots):")
        cols2 = st.columns(5)
        for i in range(10):
            with cols2[i % 5]:
                pf = st.file_uploader(f"ఫొటో {i+1}", type=["png", "jpg"], key=f"brs_p_{i}")
                if pf:
                    photos.append(pf)
                    
    with tab_a:
        audio = st.file_uploader("తెలంగాణ / BRS ప్రచార పాట లేదా ఆడియో (MP3)", type=["mp3", "wav"])
        photo_dur = st.slider("ఒక్కో ఫొటో స్క్రీన్ సమయం (సెకన్లలో):", 1, 5, 3)

    if st.button("🚀 వీడియో రీల్ మిక్స్ చేయండి (Render Reel)"):
        if not videos and not photos:
            st.warning("దయచేసి కనీసం ఒక వీడియో లేదా ఫొటోను అప్‌లోడ్ చేయండి.")
        else:
            with st.spinner("రీల్ రెండర్ అవుతోంది... దయచేసి వేచి ఉండండి"):
                clips = []
                
                # Load video clips
                for idx, v in enumerate(videos):
                    t_name = f"v_temp_{idx}.mp4"
                    with open(t_name, "wb") as f:
                        f.write(v.read())
                    c = VideoFileClip(t_name).resize(width=1080)
                    clips.append(c)
                
                # Load photo clips
                for idx, p in enumerate(photos):
                    t_name = f"p_temp_{idx}.png"
                    with open(t_name, "wb") as f:
                        f.write(p.read())
                    c = ImageClip(t_name).set_duration(photo_dur).resize(width=1080)
                    clips.append(c)
                
                final_reel = concatenate_videoclips(clips, method="compose")
                
                if audio:
                    a_name = "temp_bgm.mp3"
                    with open(a_name, "wb") as f:
                        f.write(audio.read())
                    bgm = AudioFileClip(a_name)
                    if bgm.duration > final_reel.duration:
                        bgm = bgm.subclip(0, final_reel.duration)
                    final_reel = final_reel.set_audio(bgm)
                    
                v_out = "brs_tata_reel.mp4"
                final_reel.write_videofile(v_out, fps=24, codec="libx264", audio_codec="aac")
                
                st.video(v_out)
                with open(v_out, "rb") as f:
                    st.download_button("📥 వీడియో రీల్ డౌన్‌లోడ్ చేసుకోండి", f, "tata_madhusudhan_reel.mp4", "video/mp4")
