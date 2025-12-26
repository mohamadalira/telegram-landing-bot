# app.py
import streamlit as st
import os
import base64
from datetime import datetime
import shutil
from PIL import Image
import io

st.set_page_config(
    page_title="🎨 سازنده لندینگ پیج آنلاین",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# استایل‌های CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #4A90E2, #50E3C2);
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 10px;
        font-weight: bold;
    }
    .color-box {
        width: 50px;
        height: 50px;
        border-radius: 10px;
        display: inline-block;
        margin: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .template-card {
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s;
    }
    .template-card:hover {
        border-color: #4A90E2;
        transform: translateY(-5px);
    }
    .template-card.selected {
        border-color: #4A90E2;
        background: #f0f8ff;
    }
    .preview-container {
        border: 2px dashed #ddd;
        border-radius: 15px;
        padding: 20px;
        min-height: 400px;
        background: #fafafa;
    }
</style>
""", unsafe_allow_html=True)

# هدر اصلی
st.markdown('<h1 class="main-header">🎨 سازنده لندینگ پیج آنلاین</h1>', unsafe_allow_html=True)

# دو ستون
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 اطلاعات صفحه")
    
    # نام
    name = st.text_input("نام / عنوان صفحه:", value="شرکت نمونه")
    
    # متن اصلی
    text = st.text_area(
        "متن اصلی صفحه:", 
        value="""این یک متن نمونه برای صفحه لندینگ شماست. شما می‌توانید این متن را با محتوای خودتان جایگزین کنید.

لندینگ پیج شما به صورت کاملاً واکنش‌گرا طراحی شده و در همه دستگاه‌ها به زیبایی نمایش داده خواهد شد.""",
        height=150
    )
    
    # آپلود عکس
    st.markdown("### 📷 عکس پروفایل")
    uploaded_file = st.file_uploader("یک عکس آپلود کنید", type=['png', 'jpg', 'jpeg', 'gif'])
    
    if uploaded_file:
        # نمایش عکس آپلود شده
        image = Image.open(uploaded_file)
        st.image(image, caption="عکس انتخابی", width=200)
        
        # ذخیره موقت
        if not os.path.exists("temp"):
            os.makedirs("temp")
        
        with open(f"temp/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
    
    # انتخاب رنگ‌ها
    st.markdown("### 🎨 انتخاب رنگ‌ها")
    
    col1a, col2a, col3a = st.columns(3)
    
    with col1a:
        color1 = st.color_picker("رنگ اول", "#4A90E2")
        st.markdown(f'<div class="color-box" style="background-color: {color1};"></div>', unsafe_allow_html=True)
    
    with col2a:
        color2 = st.color_picker("رنگ دوم", "#50E3C2")
        st.markdown(f'<div class="color-box" style="background-color: {color2};"></div>', unsafe_allow_html=True)
    
    with col3a:
        color3 = st.color_picker("رنگ سوم", "#F5A623")
        st.markdown(f'<div class="color-box" style="background-color: {color3};"></div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 🎯 انتخاب قالب")
    
    # انتخاب تمپلیت
    template_options = {
        "مدرن": "طراحی مینیمال و مدرن",
        "خلاقانه": "طرح هنری و خلاقانه", 
        "حرفه‌ای": "قالب شرکتی و رسمی"
    }
    
    selected_template = st.radio(
        "یک قالب انتخاب کنید:",
        list(template_options.keys()),
        format_func=lambda x: f"**{x}** - {template_options[x]}"
    )
    
    # نمایش نمونه
    st.markdown("### 👁️ پیش‌نمایش")
    
    # ساخت پیش‌نمایش ساده
    preview_html = f"""
    <div class="preview-container">
        <div style="background: linear-gradient(45deg, {color1}, {color2}); 
                    padding: 30px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="color: white; margin: 0;">{name}</h3>
        </div>
        
        <div style="display: flex; gap: 10px; margin: 20px 0;">
            <div style="flex: 1; height: 40px; background: {color1}; border-radius: 5px;"></div>
            <div style="flex: 1; height: 40px; background: {color2}; border-radius: 5px;"></div>
            <div style="flex: 1; height: 40px; background: {color3}; border-radius: 5px;"></div>
        </div>
        
        <p style="color: #666;">{text[:100]}...</p>
        
        <div style="margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 10px;">
            <small>قالب: <strong>{selected_template}</strong></small>
        </div>
    </div>
    """
    
    st.markdown(preview_html, unsafe_allow_html=True)
    
    # نام فایل خروجی
    st.markdown("### 💾 ذخیره سازی")
    filename = st.text_input("نام فایل خروجی:", value="landing_page")
    
    if not filename.endswith('.html'):
        filename += '.html'

# تمپلیت‌ها
TEMPLATES = {
    "مدرن": """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{نام}} | لندینگ پیج</title>
    <style>
        :root {
            --primary: {{رنگ1}};
            --secondary: {{رنگ2}};
            --accent: {{رنگ3}};
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Vazir', sans-serif; }
        body { background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); min-height: 100vh; }
        .hero { 
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            color: white; 
            padding: 100px 20px; 
            text-align: center;
            clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
            margin-bottom: 60px;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        .profile-img { 
            width: 200px; 
            height: 200px; 
            border-radius: 50%; 
            object-fit: cover;
            border: 8px solid rgba(255,255,255,0.3);
            margin: 30px auto;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .content-card {
            background: white;
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            margin: 40px 0;
        }
        .color-palette {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 40px 0;
        }
        .color-box {
            width: 60px;
            height: 60px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .footer {
            background: var(--secondary);
            color: white;
            padding: 40px;
            text-align: center;
            margin-top: 80px;
        }
        @media (max-width: 768px) {
            .hero { padding: 60px 20px; }
            .profile-img { width: 150px; height: 150px; }
            .content-card { padding: 30px; }
        }
    </style>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/vazir-font@30.1.0/dist/font-face.css">
</head>
<body>
    <header class="hero">
        <div class="container">
            <h1 style="font-size: 3rem; margin-bottom: 20px;">{{نام}}</h1>
            {{عکس}}
            <p style="font-size: 1.2rem; opacity: 0.9; max-width: 600px; margin: 0 auto;">
                به صفحه اختصاصی ما خوش آمدید
            </p>
        </div>
    </header>
    
    <main class="container">
        <div class="content-card">
            <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
                {{متن}}
            </p>
            
            <div class="color-palette">
                <div class="color-box" style="background-color: var(--primary);"></div>
                <div class="color-box" style="background-color: var(--secondary);"></div>
                <div class="color-box" style="background-color: var(--accent);"></div>
            </div>
        </div>
    </main>
    
    <footer class="footer">
        <p>© {{سال}} - {{نام}}. تمامی حقوق محفوظ است.</p>
        <p style="margin-top: 10px; opacity: 0.8;">
            ساخته شده با ❤️ توسط سازنده لندینگ پیج آنلاین
        </p>
    </footer>
</body>
</html>""",
    
    "خلاقانه": """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{نام}} | صفحه خلاقانه</title>
    <style>
        :root {
            --color1: {{رنگ1}};
            --color2: {{رنگ2}};
            --color3: {{رنگ3}};
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Vazir', sans-serif;
            background: linear-gradient(45deg, 
                color-mix(in srgb, var(--color1) 15%, transparent 85%),
                color-mix(in srgb, var(--color2) 15%, transparent 85%),
                color-mix(in srgb, var(--color3) 15%, transparent 85%)
            );
            min-height: 100vh;
        }
        .creative-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            min-height: 100vh;
            gap: 40px;
            padding: 40px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .profile-side {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .profile-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 50px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        }
        .creative-img {
            width: 220px;
            height: 220px;
            border-radius: 50%;
            object-fit: cover;
            border: 10px solid;
            border-image: linear-gradient(45deg, var(--color1), var(--color2), var(--color3)) 1;
            margin: 30px auto;
            transition: transform 0.5s ease;
        }
        .creative-img:hover {
            transform: scale(1.05) rotate(5deg);
        }
        .creative-name {
            font-size: 2.8rem;
            background: linear-gradient(45deg, var(--color1), var(--color2));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin: 20px 0;
            font-weight: 800;
        }
        .content-side {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .creative-content {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 60px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        }
        .creative-text {
            font-size: 1.2rem;
            line-height: 1.8;
            color: #444;
            position: relative;
            padding-right: 30px;
        }
        .creative-text::before {
            content: '"';
            font-size: 8rem;
            position: absolute;
            top: -50px;
            right: 0;
            color: var(--color1);
            opacity: 0.2;
            font-family: Georgia, serif;
        }
        .color-strip {
            display: flex;
            gap: 20px;
            margin-top: 50px;
        }
        .color-item {
            flex: 1;
            height: 80px;
            border-radius: 15px;
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease;
        }
        .color-item:hover {
            transform: translateY(-10px);
        }
        .color-label {
            position: absolute;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            font-size: 0.9rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        @media (max-width: 1024px) {
            .creative-grid { grid-template-columns: 1fr; gap: 20px; }
            .creative-name { font-size: 2.2rem; }
        }
    </style>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/vazir-font@30.1.0/dist/font-face.css">
</head>
<body>
    <div class="creative-grid">
        <div class="profile-side">
            <div class="profile-card">
                {{عکس}}
                <h1 class="creative-name">{{نام}}</h1>
                <p style="color: #666; font-size: 1.1rem;">طراحی منحصر به فرد و خلاقانه</p>
            </div>
        </div>
        
        <div class="content-side">
            <div class="creative-content">
                <div class="creative-text">
                    {{متن}}
                </div>
                
                <div class="color-strip">
                    <div class="color-item" style="background-color: var(--color1);">
                        <span class="color-label">رنگ اصلی</span>
                    </div>
                    <div class="color-item" style="background-color: var(--color2);">
                        <span class="color-label">رنگ دوم</span>
                    </div>
                    <div class="color-item" style="background-color: var(--color3);">
                        <span class="color-label">رنگ سوم</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>""",
    
    "حرفه‌ای": """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{نام}} | صفحه رسمی</title>
    <style>
        :root {
            --primary: {{رنگ1}};
            --secondary: {{رنگ2}};
            --accent: {{رنگ3}};
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Vazir', sans-serif;
            color: #1a1a1a;
            background: #f5f5f7;
            line-height: 1.6;
        }
        .navbar {
            background: white;
            box-shadow: 0 2px 20px rgba(0,0,0,0.05);
            padding: 0 40px;
            height: 80px;
            display: flex;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .brand {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
            text-decoration: none;
        }
        .hero-section {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 120px 40px;
            text-align: center;
        }
        .professional-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 80px 20px;
        }
        .professional-card {
            background: white;
            border-radius: 20px;
            padding: 60px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            border-right: 6px solid var(--accent);
        }
        .professional-img {
            width: 280px;
            height: 280px;
            object-fit: cover;
            border-radius: 20px;
            margin: 40px auto;
            display: block;
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
            border: 10px solid white;
        }
        .professional-title {
            font-size: 3.5rem;
            margin-bottom: 30px;
            color: white;
        }
        .professional-text {
            font-size: 1.15rem;
            color: #444;
            line-height: 1.8;
            margin-bottom: 50px;
        }
        .color-showcase {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            margin-top: 60px;
        }
        .color-card {
            padding: 40px 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            min-height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            transition: transform 0.3s ease;
        }
        .color-card:hover {
            transform: translateY(-10px);
        }
        .professional-footer {
            background: #1a1a1a;
            color: white;
            padding: 60px 40px;
            text-align: center;
            margin-top: 100px;
        }
        @media (max-width: 768px) {
            .professional-title { font-size: 2.2rem; }
            .color-showcase { grid-template-columns: 1fr; }
            .professional-card { padding: 30px; }
            .professional-img { width: 200px; height: 200px; }
        }
    </style>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/vazir-font@30.1.0/dist/font-face.css">
</head>
<body>
    <nav class="navbar">
        <a href="#" class="brand">{{نام}}</a>
    </nav>
    
    <header class="hero-section">
        <h1 class="professional-title">{{نام}}</h1>
        <p style="font-size: 1.3rem; opacity: 0.9; max-width: 700px; margin: 0 auto;">
            ارائه خدمات حرفه‌ای و با کیفیت
        </p>
    </header>
    
    <main class="professional-container">
        <div class="professional-card">
            {{عکس}}
            
            <div class="professional-text">
                {{متن}}
            </div>
            
            <div class="color-showcase">
                <div class="color-card" style="background-color: var(--primary);">
                    <h3 style="font-size: 1.5rem; margin-bottom: 10px;">رنگ اصلی</h3>
                    <p>برای هویت برند و لوگو</p>
                </div>
                <div class="color-card" style="background-color: var(--secondary);">
                    <h3 style="font-size: 1.5rem; margin-bottom: 10px;">رنگ ثانویه</h3>
                    <p>برای بخش‌های فرعی</p>
                </div>
                <div class="color-card" style="background-color: var(--accent);">
                    <h3 style="font-size: 1.5rem; margin-bottom: 10px;">رنگ تأکیدی</h3>
                    <p>برای دکمه‌های اقدام</p>
                </div>
            </div>
        </div>
    </main>
    
    <footer class="professional-footer">
        <p style="font-size: 1.1rem;">© {{سال}} {{نام}}. تمامی حقوق محفوظ است.</p>
        <p style="margin-top: 20px; opacity: 0.8; font-size: 0.95rem;">
            این صفحه به صورت حرفه‌ای توسط سیستم تولید لندینگ پیج طراحی شده است
        </p>
    </footer>
</body>
</html>"""
}

def create_image_html(uploaded_file, template_type):
    """ایجاد HTML برای عکس"""
    if not uploaded_file:
        if template_type == "مدرن":
            return '<div class="profile-img" style="background: linear-gradient(45deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem;">LOGO</div>'
        elif template_type == "خلاقانه":
            return '<div class="creative-img" style="background: linear-gradient(45deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem;">LOGO</div>'
        else:
            return '<img src="https://via.placeholder.com/280x280/4A90E2/ffffff?text=LOGO" class="professional-img" alt="تصویر">'
    
    try:
        # تبدیل به base64 برای نمایش مستقیم در HTML
        img_bytes = uploaded_file.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode()
        
        if template_type == "مدرن":
            return f'<img src="data:image/png;base64,{img_base64}" class="profile-img" alt="{name}">'
        elif template_type == "خلاقانه":
            return f'<img src="data:image/png;base64,{img_base64}" class="creative-img" alt="{name}">'
        else:
            return f'<img src="data:image/png;base64,{img_base64}" class="professional-img" alt="{name}">'
    except:
        return '<div class="profile-img" style="background: linear-gradient(45deg, #667eea, #764ba2);"></div>'

# دکمه ساخت در پایین صفحه
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    if st.button("🚀 ساخت لندینگ پیج", key="generate_btn"):
        if not name:
            st.error("⚠️ لطفاً نام صفحه را وارد کنید!")
        elif not text:
            st.error("⚠️ لطفاً متن اصلی را وارد کنید!")
        else:
            with st.spinner("در حال ساخت صفحه..."):
                # انتخاب تمپلیت
                template = TEMPLATES[selected_template]
                
                # ساخت HTML عکس
                img_html = create_image_html(uploaded_file, selected_template)
                
                # جایگزینی متغیرها
                html_content = template
                html_content = html_content.replace("{{نام}}", name)
                html_content = html_content.replace("{{متن}}", text)
                html_content = html_content.replace("{{رنگ1}}", color1)
                html_content = html_content.replace("{{رنگ2}}", color2)
                html_content = html_content.replace("{{رنگ3}}", color3)
                html_content = html_content.replace("{{سال}}", str(datetime.now().year))
                html_content = html_content.replace("{{عکس}}", img_html)
                
                # ذخیره فایل
                output_dir = "generated_pages"
                os.makedirs(output_dir, exist_ok=True)
                
                output_path = os.path.join(output_dir, filename)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # نمایش موفقیت
                st.success(f"✅ لندینگ پیج با موفقیت ساخته شد!")
                
                # دانلود فایل
                with open(output_path, "rb") as file:
                    btn = st.download_button(
                        label="📥 دانلود فایل HTML",
                        data=file,
                        file_name=filename,
                        mime="text/html"
                    )
                
                # نمایش پیش‌نمایش
                st.markdown("### 👁️ پیش‌نمایش صفحه ساخته شده")
                st.components.v1.html(html_content, height=600, scrolling=True)
                
                # پاک کردن فایل موقت
                if uploaded_file and os.path.exists(f"temp/{uploaded_file.name}"):
                    os.remove(f"temp/{uploaded_file.name}")

# سایدبار برای اطلاعات
with st.sidebar:
    st.markdown("### 📌 راهنما")
    st.markdown("""
    1. **نام صفحه** را وارد کنید
    2. **متن اصلی** را بنویسید
    3. **عکس** آپلود کنید (اختیاری)
    4. **سه رنگ** انتخاب کنید
    5. **قالب** دلخواه را انتخاب کنید
    6. دکمه **ساخت** را بزنید
    7. فایل را **دانلود** کنید
    
    ⚡ تمام صفحات ساخته شده:
    - کاملاً **واکنش‌گرا** هستند
    - از **فارسی** پشتیبانی می‌کنند
    - **بهینه** برای SEO
    - **سریع** لود می‌شوند
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 قالب‌های موجود")
    
    for template_name, desc in template_options.items():
        st.info(f"**{template_name}**: {desc}")
    
    st.markdown("---")
    st.markdown("### 📊 آمار")
    
    if os.path.exists("generated_pages"):
        count = len([f for f in os.listdir("generated_pages") if f.endswith('.html')])
        st.metric("صفحات ساخته شده", count)
    else:
        st.metric("صفحات ساخته شده", 0)