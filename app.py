import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import os
import requests
from io import BytesIO

st.set_page_config(page_title="BRS Media Studio - Tata Madhusudhan MLC", layout="wide", page_icon="🌸")

# Brand Palette
BRS_PINK = (229, 0, 125)
BRS_DARK = (140, 0, 75)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)

# Fetch authentic Telugu font with unicode support
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/suranna/Suranna-Regular.ttf"
FONT_PATH = "TeluguFont.ttf"
if not os.path.exists(FONT_PATH):
    try:
        r = requests.get(FONT_URL, timeout=10)
        with open(FONT_PATH, "wb") as f:
            f.write(r.content)
    except Exception:
        pass

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def make_circular_badge(img, size=(160, 160), border_color=(255, 215, 0), border_width=6):
    img = img.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
    mask = Image.new("L", size, 0)
    draw_m = ImageDraw.Draw(mask)
    draw_m.ellipse((0, 0, size[0], size[1]), fill=255)
    
    circular = ImageOps.fit(img, size, centering=(0.5, 0.5))
    circular.putalpha(mask)
    
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.paste(circular, (0, 0), circular)
    
    draw_b = ImageDraw.Draw(canvas)
    draw_b.ellipse(
        (border_width // 2, border_width // 2, size[0] - border_width // 2, size[1] - border_width // 2),
        outline=border_color,
        width=border_width
    )
    return canvas

def soft_blend_portrait(img, target_size=(750, 980)):
    """Removes harsh rectangular borders by applying an elliptical soft-gradient alpha mask."""
    img = img.convert("RGBA").resize(target_size, Image.Resampling.LANCZOS)
    w, h = img.size
    
    # Create vignette/feather mask
    mask = Image.new("L", (w, h), 255)
    draw_m = ImageDraw.Draw(mask)
    
    # Feather top and sides
    for i in range(40):
        alpha = int(255 * (i / 40.0))
        draw_m.rectangle([0, i, w, i+1], fill=alpha)
        draw_m.rectangle([i, 0, i+1, h], fill=alpha)
        draw_m.rectangle([w - i - 1, 0, w - i, h], fill=alpha)
        
    mask = mask.filter(ImageFilter.GaussianBlur(15))
    img.putalpha(mask)
    return img

LEADERS = {
    "kcr": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/K._Chandrashekar_Rao_in_2023.jpg/360px-K._Chandrashekar_Rao_in_2023.jpg",
    "ktr": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/K._T._Rama_Rao_in_2023.jpg/360px-K._T._Rama_Rao_in_2023.jpg",
    "harish": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/T._Harish_Rao_in_2023.jpg/360px-T._Harish_Rao_in_2023.jpg"
}

def load_img(uploaded, key):
    if uploaded is not None:
        return Image.open(uploaded)
    try:
        res = requests.get(LEADERS[key], timeout=5)
        return Image.open(BytesIO(res.content))
    except Exception:
        return Image.new("RGBA", (160, 160), BRS_PINK)

st.sidebar.title("BRS Media Studio")
st.sidebar.markdown("**శ్రీ తాతా మధుసూదన్ గారు (MLC)**")
mode = st.sidebar.radio("Select Tool:", ["Poster Studio", "Video Reel Mixer"])

if mode == "Poster Studio":
    st.header("Daily Political Poster Studio")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        tata_file = st.file_uploader("Upload Sri Tata Madhusudhan Garu Photo", type=["png", "jpg", "jpeg"])
        custom_bg = st.file_uploader("Custom Background Graphic (Optional)", type=["png", "jpg"])
        
        with st.expander("Top Leadership Badges (Defaults auto-loaded)"):
            kcr_f = st.file_uploader("Custom KCR Photo", type=["png", "jpg"])
            ktr_f = st.file_uploader("Custom KTR Photo", type=["png", "jpg"])
            harish_f = st.file_uploader("Custom Harish Rao Photo", type=["png", "jpg"])
            
        st.subheader("Poster Text (Telugu)")
        h1 = st.text_input("Main Heading:", value="న్యాయం గెలుస్తుంది")
        msg = st.text_area("Message:", value="ఎన్ని అడ్డంకులు, అవరోధాలు ఎదురైనా బీఆర్ఎస్ పార్టీ జైత్రయాత్ర ఆగదు. ప్రజాసేవలో సదా ముందంజ.")
        l_name = st.text_input("Leader Name Strip:", value="తాతా మధుసూదన్, MLC")
        footer = st.text_input("Footer Greetings:", value="జై తెలంగాణ.. జై కేసీఆర్.. జై భారత్ రాష్ట్ర సమితి!")

    with col2:
        if st.button("Generate Professional Poster", type="primary"):
            if not tata_file:
                st.warning("Please upload Sri Tata Madhusudhan Garu's photo.")
            else:
                with st.spinner("Compositing graphic layout..."):
                    W, H = 1080, 1440
                    
                    # 1. Base Gradient Canvas
                    if custom_bg:
                        poster = Image.open(custom_bg).convert("RGBA").resize((W, H))
                    else:
                        poster = Image.new("RGBA", (W, H), (20, 0, 10, 255))
                        d_bg = ImageDraw.Draw(poster)
                        for y in range(H):
                            t = y / H
                            r = int(220 - (t * 180))
                            g = int(0 + (t * 15))
                            b = int(120 - (t * 90))
                            d_bg.line([(0, y), (W, y)], fill=(r, g, b, 255))
                    
                    # 2. Add Soft Portrait with Blended Edges (Eliminates Studio Box)
                    raw_subj = Image.open(tata_file)
                    blended_subj = soft_blend_portrait(raw_subj, target_size=(740, 960))
                    poster.paste(blended_subj, (W - 750, H - 1180), blended_subj)
                    
                    # 3. Top Banner
                    draw = ImageDraw.Draw(poster)
                    draw.rectangle([0, 0, W, 220], fill=BRS_PINK)
                    draw.rectangle([0, 215, W, 222], fill=GOLD)
                    
                    # Top Leadership Badges
                    kcr_badge = make_circular_badge(load_img(kcr_f, "kcr"), size=(175, 175), border_color=GOLD, border_width=6)
                    poster.paste(kcr_badge, (35, 22), kcr_badge)
                    
                    ktr_badge = make_circular_badge(load_img(ktr_f, "ktr"), size=(150, 150), border_color=WHITE, border_width=5)
                    poster.paste(ktr_badge, (W - 325, 35), ktr_badge)
                    
                    harish_badge = make_circular_badge(load_img(harish_f, "harish"), size=(150, 150), border_color=WHITE, border_width=5)
                    poster.paste(harish_badge, (W - 165, 35), harish_badge)
                    
                    # Party Name (Centered between badges)
                    font_hdr = get_font(52)
                    draw.text((W // 2 + 10, 110), "భారత రాష్ట్ర సమితి (BRS)", fill=WHITE, font=font_hdr, anchor="mm")
                    
                    # 4. Text Content (Left Side)
                    font_main = get_font(60)
                    font_sub = get_font(34)
                    
                    # Heading with Glow Shadow
                    draw.text((62, 342), h1, fill=BLACK, font=font_main)
                    draw.text((60, 340), h1, fill=GOLD, font=font_main)
                    
                    # Message Wrapping
                    words = msg.split()
                    line = ""
                    y_pos = 440
                    for w in words:
                        test = f"{line} {w}".strip()
                        if draw.textlength(test, font=font_sub) < 460:
                            line = test
                        else:
                            draw.text((60, y_pos), line, fill=WHITE, font=font_sub)
                            y_pos += 48
                            line = w
                    if line:
                        draw.text((60, y_pos), line, fill=WHITE, font=font_sub)
                        
                    # 5. Bottom Designations Ribbon
                    draw.rectangle([0, H - 240, W, H], fill=BRS_PINK)
                    draw.rectangle([0, H - 245, W, H - 240], fill=GOLD)
                    
                    font_lead = get_font(54)
                    font_foot = get_font(32)
                    
                    draw.text((W // 2, H - 155), l_name, fill=GOLD, font=font_lead, anchor="mm")
                    draw.text((W // 2, H - 70), footer, fill=WHITE, font=font_foot, anchor="mm")
                    
                    # 6. Save & Provide Direct Download (Baking typography in)
                    out_path = "final_brs_poster.png"
                    poster.convert("RGB").save(out_path, quality=95)
                    
                    st.image(poster, caption="Baked High-Resolution Poster", use_container_width=True)
                    with open(out_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Full HD Baked Poster",
                            data=f,
                            file_name="tata_madhusudhan_brs_poster.png",
                            mime="image/png"
                        )
