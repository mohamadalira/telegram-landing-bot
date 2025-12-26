import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
import os
from datetime import datetime
import shutil
from PIL import Image, ImageTk
import base64

class LandingPageCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 سازنده لندینگ پیج هوشمند")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f2f5')
        
        # ذخیره داده‌ها
        self.image_path = None
        self.colors = ['#4A90E2', '#50E3C2', '#F5A623']  # رنگ‌های پیش‌فرض
        self.templates = self.load_templates()
        
        # تم رنگی
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # ساخت UI
        self.setup_ui()
        
    def setup_ui(self):
        """ایجاد رابط کاربری"""
        
        # فریم اصلی
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # عنوان
        title_label = tk.Label(
            main_frame,
            text="🚀 سازنده لندینگ پیج اختصاصی",
            font=('Vazir', 24, 'bold'),
            bg='#f0f2f5',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 30))
        
        # فریم برای دو ستون
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # ستون چپ: فرم ورود
        left_frame = ttk.LabelFrame(content_frame, text="📝 اطلاعات صفحه", padding="20")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # ستون راست: پیش‌نمایش
        right_frame = ttk.LabelFrame(content_frame, text="👁️ پیش‌نمایش رنگ‌ها", padding="20")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # === بخش فرم ورود ===
        
        # نام
        tk.Label(left_frame, text="نام / عنوان:", font=('Vazir', 11)).pack(anchor='w', pady=(0, 5))
        self.name_entry = tk.Entry(left_frame, font=('Vazir', 11), width=40)
        self.name_entry.pack(fill=tk.X, pady=(0, 15))
        self.name_entry.insert(0, "شرکت نمونه")
        
        # متن اصلی
        tk.Label(left_frame, text="متن اصلی صفحه:", font=('Vazir', 11)).pack(anchor='w', pady=(0, 5))
        self.text_text = tk.Text(left_frame, height=6, font=('Vazir', 11), width=40)
        self.text_text.pack(fill=tk.X, pady=(0, 15))
        self.text_text.insert('1.0', """این یک متن نمونه برای صفحه لندینگ شماست. شما می‌توانید این متن را با محتوای خودتان جایگزین کنید.
        
لندینگ پیج شما به صورت کاملاً واکنش‌گرا طراحی شده و در همه دستگاه‌ها به زیبایی نمایش داده خواهد شد.""")
        
        # آپلود عکس
        photo_frame = ttk.Frame(left_frame)
        photo_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(photo_frame, text="عکس پروفایل:", font=('Vazir', 11)).pack(anchor='w', pady=(0, 5))
        
        self.photo_btn = tk.Button(
            photo_frame,
            text="📁 انتخاب عکس",
            command=self.upload_image,
            bg='#3498db',
            fg='white',
            font=('Vazir', 10),
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        self.photo_btn.pack(side=tk.LEFT)
        
        self.photo_label = tk.Label(photo_frame, text="هیچ عکسی انتخاب نشده", fg='#7f8c8d', font=('Vazir', 10))
        self.photo_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # انتخاب رنگ‌ها
        tk.Label(left_frame, text="انتخاب سه رنگ:", font=('Vazir', 11)).pack(anchor='w', pady=(0, 5))
        
        colors_frame = ttk.Frame(left_frame)
        colors_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.color_btns = []
        for i in range(3):
            btn = tk.Button(
                colors_frame,
                text=f"رنگ {i+1}",
                command=lambda idx=i: self.choose_color(idx),
                bg=self.colors[i],
                fg='white' if i != 2 else 'black',
                font=('Vazir', 10),
                relief=tk.FLAT,
                width=10,
                padx=10,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=(0, 10))
            self.color_btns.append(btn)
        
        # انتخاب تمپلیت
        tk.Label(left_frame, text="طرح قالب:", font=('Vazir', 11)).pack(anchor='w', pady=(0, 5))
        self.template_var = tk.StringVar(value="مدرن")
        template_combo = ttk.Combobox(
            left_frame,
            textvariable=self.template_var,
            values=["مدرن", "خلاقانه", "حرفه‌ای"],
            font=('Vazir', 10),
            state='readonly',
            width=37
        )
        template_combo.pack(fill=tk.X, pady=(0, 15))
        
        # نام فایل خروجی
        tk.Label(left_frame, text="نام فایل خروجی:", font=('Vazir', 11)).pack(anchor='w', pady=(0, 5))
        self.filename_entry = tk.Entry(left_frame, font=('Vazir', 11), width=40)
        self.filename_entry.pack(fill=tk.X, pady=(0, 20))
        self.filename_entry.insert(0, "landing_page")
        
        # دکمه ساخت
        self.generate_btn = tk.Button(
            left_frame,
            text="🚀 ساخت لندینگ پیج",
            command=self.generate_page,
            bg='#2ecc71',
            fg='white',
            font=('Vazir', 12, 'bold'),
            relief=tk.FLAT,
            padx=30,
            pady=15
        )
        self.generate_btn.pack()
        
        # === بخش پیش‌نمایش ===
        
        # نمایش رنگ‌ها
        self.color_preview_frame = tk.Frame(right_frame, bg='white', height=200)
        self.color_preview_frame.pack(fill=tk.X, pady=(0, 20))
        self.color_preview_frame.pack_propagate(False)
        
        # نمونه لندینگ پیج
        preview_label = tk.Label(right_frame, text="نمونه طرح:", font=('Vazir', 11))
        preview_label.pack(anchor='w', pady=(0, 5))
        
        self.preview_canvas = tk.Canvas(right_frame, bg='white', height=300)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # به‌روزرسانی اولیه پیش‌نمایش
        self.update_preview()
        
    def choose_color(self, index):
        """انتخاب رنگ"""
        color = colorchooser.askcolor(title=f"انتخاب رنگ {index+1}", initialcolor=self.colors[index])[1]
        if color:
            self.colors[index] = color
            self.color_btns[index].config(bg=color)
            # تغییر رنگ متن برای خوانایی
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            text_color = 'white' if brightness < 128 else 'black'
            self.color_btns[index].config(fg=text_color)
            self.update_preview()
    
    def upload_image(self):
        """آپلود عکس"""
        filetypes = [
            ('تصاویر', '*.png *.jpg *.jpeg *.gif *.bmp'),
            ('همه فایل‌ها', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title="انتخاب عکس",
            filetypes=filetypes
        )
        
        if filename:
            self.image_path = filename
            self.photo_label.config(
                text=os.path.basename(filename)[:20] + "...",
                fg='#27ae60'
            )
    
    def update_preview(self):
        """به‌روزرسانی پیش‌نمایش"""
        self.preview_canvas.delete("all")
        
        # رسم نمونه طرح
        width = self.preview_canvas.winfo_width() or 400
        height = self.preview_canvas.winfo_height() or 300
        
        # هدر
        self.preview_canvas.create_rectangle(
            10, 10, width - 10, 80,
            fill=self.colors[0],
            outline=''
        )
        
        # عنوان
        self.preview_canvas.create_text(
            width/2, 45,
            text="لندینگ پیج شما",
            fill='white',
            font=('Vazir', 12, 'bold')
        )
        
        # محتوا
        self.preview_canvas.create_rectangle(
            10, 100, width/2 - 5, height - 10,
            fill='#f8f9fa',
            outline='#dee2e6'
        )
        
        self.preview_canvas.create_rectangle(
            width/2 + 5, 100, width - 10, height - 10,
            fill='#ffffff',
            outline='#dee2e6'
        )
        
        # رنگ‌های انتخابی
        color_width = (width - 40) / 3
        for i in range(3):
            x1 = 20 + (i * (color_width + 10))
            x2 = x1 + color_width
            self.preview_canvas.create_rectangle(
                x1, 120, x2, 160,
                fill=self.colors[i],
                outline=''
            )
    
    def load_templates(self):
        """لود تمپلیت‌ها"""
        templates = {
            "مدرن": """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{نام}} | لندینگ پیج</title>
    <style>
        :root {
            --primary-color: {{رنگ1}};
            --secondary-color: {{رنگ2}};
            --accent-color: {{رنگ3}};
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; }
        body { background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); min-height: 100vh; }
        .hero { background: linear-gradient(45deg, var(--primary-color), var(--secondary-color)); 
                color: white; padding: 80px 20px; text-align: center; }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
        .content-card { background: white; border-radius: 20px; padding: 40px; 
                       box-shadow: 0 10px 30px rgba(0,0,0,0.08); }
        .profile-img { width: 200px; height: 200px; border-radius: 50%; object-fit: cover; 
                      border: 8px solid rgba(255,255,255,0.3); margin: 20px auto; }
        .color-palette { display: flex; justify-content: center; gap: 20px; margin: 30px 0; }
        .color-box { width: 60px; height: 60px; border-radius: 10px; }
        .footer { background: var(--secondary-color); color: white; padding: 30px; text-align: center; }
        @media (max-width: 768px) { .profile-img { width: 150px; height: 150px; } }
    </style>
</head>
<body>
    <header class="hero">
        <h1 style="font-size: 2.5rem; margin-bottom: 20px;">{{نام}}</h1>
        {{عکس_هدر}}
        <p style="font-size: 1.2rem; opacity: 0.9; max-width: 600px; margin: 0 auto;">
            خوش آمدید به صفحه اختصاصی
        </p>
    </header>
    
    <main class="container">
        <div class="content-card">
            <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify; margin-bottom: 30px;">
                {{متن}}
            </p>
            
            <div class="color-palette">
                <div class="color-box" style="background-color: {{رنگ1}}"></div>
                <div class="color-box" style="background-color: {{رنگ2}}"></div>
                <div class="color-box" style="background-color: {{رنگ3}}"></div>
            </div>
        </div>
    </main>
    
    <footer class="footer">
        <p>© {{سال}} - {{نام}}. تمامی حقوق محفوظ است.</p>
        <p style="margin-top: 10px; opacity: 0.8;">ساخته شده با ❤️ توسط سازنده لندینگ پیج</p>
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
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(45deg, 
                color-mix(in srgb, var(--color1) 10%, transparent 90%),
                color-mix(in srgb, var(--color2) 10%, transparent 90%),
                color-mix(in srgb, var(--color3) 10%, transparent 90%)
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
            align-items: center;
        }
        .profile-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            max-width: 400px;
        }
        .creative-img {
            width: 180px;
            height: 180px;
            border-radius: 50%;
            object-fit: cover;
            border: 8px solid;
            border-image: linear-gradient(45deg, var(--color1), var(--color2), var(--color3)) 1;
            margin: 20px auto;
        }
        .creative-name {
            font-size: 2.5rem;
            background: linear-gradient(45deg, var(--color1), var(--color2));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin: 20px 0;
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
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        }
        .creative-text {
            font-size: 1.2rem;
            line-height: 1.8;
            color: #444;
            position: relative;
            padding: 20px;
        }
        .creative-text::before {
            content: '"';
            font-size: 6rem;
            position: absolute;
            top: -40px;
            right: 0;
            color: var(--color1);
            opacity: 0.3;
            font-family: Georgia, serif;
        }
        .color-strip {
            display: flex;
            gap: 15px;
            margin-top: 40px;
        }
        .color-item {
            flex: 1;
            height: 60px;
            border-radius: 12px;
            position: relative;
            overflow: hidden;
        }
        @media (max-width: 1024px) {
            .creative-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="creative-grid">
        <div class="profile-side">
            <div class="profile-card">
                {{عکس_محتوا}}
                <h1 class="creative-name">{{نام}}</h1>
                <p style="color: #666; margin-bottom: 20px;">طراحی خلاقانه و منحصر به فرد</p>
            </div>
        </div>
        
        <div class="content-side">
            <div class="creative-content">
                <div class="creative-text">
                    {{متن}}
                </div>
                
                <div class="color-strip">
                    <div class="color-item" style="background-color: var(--color1);"></div>
                    <div class="color-item" style="background-color: var(--color2);"></div>
                    <div class="color-item" style="background-color: var(--color3);"></div>
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
            font-family: 'Segoe UI', Tahoma, sans-serif;
            color: #1a1a1a;
            background: #f5f5f7;
            line-height: 1.6;
        }
        .professional-header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 120px 40px;
            text-align: center;
        }
        .professional-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 60px 20px;
        }
        .professional-card {
            background: white;
            border-radius: 20px;
            padding: 60px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            border-right: 6px solid var(--accent);
        }
        .professional-img {
            width: 250px;
            height: 250px;
            object-fit: cover;
            border-radius: 20px;
            margin: 30px auto;
            display: block;
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
            border: 8px solid white;
        }
        .professional-title {
            font-size: 3rem;
            margin-bottom: 20px;
            color: white;
        }
        .professional-text {
            font-size: 1.1rem;
            color: #444;
            line-height: 1.8;
            margin-bottom: 40px;
        }
        .color-showcase {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            margin-top: 60px;
        }
        .color-card {
            padding: 30px;
            border-radius: 15px;
            color: white;
            text-align: center;
            min-height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .professional-footer {
            background: #1a1a1a;
            color: white;
            padding: 40px;
            text-align: center;
            margin-top: 80px;
        }
        @media (max-width: 768px) {
            .professional-title { font-size: 2rem; }
            .color-showcase { grid-template-columns: 1fr; }
            .professional-card { padding: 30px; }
        }
    </style>
</head>
<body>
    <header class="professional-header">
        <h1 class="professional-title">{{نام}}</h1>
        <p style="font-size: 1.2rem; opacity: 0.9; max-width: 600px; margin: 0 auto;">
            ارائه خدمات حرفه‌ای و با کیفیت
        </p>
    </header>
    
    <main class="professional-container">
        <div class="professional-card">
            {{عکس_محتوا}}
            
            <div class="professional-text">
                {{متن}}
            </div>
            
            <div class="color-showcase">
                <div class="color-card" style="background-color: var(--primary);">
                    <h3>رنگ اصلی</h3>
                    <p>برای برند و هویت بصری</p>
                </div>
                <div class="color-card" style="background-color: var(--secondary);">
                    <h3>رنگ ثانویه</h3>
                    <p>برای المان‌های تکمیلی</p>
                </div>
                <div class="color-card" style="background-color: var(--accent);">
                    <h3>رنگ تأکیدی</h3>
                    <p>برای دکمه‌ها و CTA</p>
                </div>
            </div>
        </div>
    </main>
    
    <footer class="professional-footer">
        <p>© {{سال}} {{نام}}. تمامی حقوق محفوظ است.</p>
        <p style="margin-top: 10px; opacity: 0.8; font-size: 0.9rem;">
            این صفحه به صورت حرفه‌ای طراحی و تولید شده است
        </p>
    </footer>
</body>
</html>"""
        }
        return templates
    
    def process_image(self, image_path, template_type):
        """پردازش عکس برای استفاده در HTML"""
        if not image_path or not os.path.exists(image_path):
            if template_type == "مدرن":
                return '<div class="profile-img" style="background: linear-gradient(45deg, #667eea, #764ba2);"></div>'
            elif template_type == "خلاقانه":
                return '<div class="creative-img" style="background: linear-gradient(45deg, #667eea, #764ba2);"></div>'
            else:
                return '<img src="https://via.placeholder.com/250x250/4A90E2/ffffff?text=LOGO" class="professional-img" alt="تصویر">'
        
        try:
            # در نسخه ساده، فقط مسیر فایل رو برمی‌گردونیم
            # در نسخه پیشرفته‌تر می‌تونیم تبدیل به base64 کنیم
            filename = os.path.basename(image_path)
            # کپی کردن عکس به پوشه خروجی
            output_dir = "generated_pages"
            os.makedirs(output_dir, exist_ok=True)
            shutil.copy2(image_path, os.path.join(output_dir, filename))
            
            if template_type == "مدرن":
                return f'<img src="{filename}" class="profile-img" alt="{self.name_entry.get()}">'
            elif template_type == "خلاقانه":
                return f'<img src="{filename}" class="creative-img" alt="{self.name_entry.get()}">'
            else:
                return f'<img src="{filename}" class="professional-img" alt="{self.name_entry.get()}">'
                
        except Exception as e:
            print(f"Error processing image: {e}")
            return '<div class="profile-img" style="background: linear-gradient(45deg, #667eea, #764ba2);"></div>'
    
    def generate_page(self):
        """ساخت صفحه لندینگ"""
        # دریافت داده‌ها
        name = self.name_entry.get().strip()
        text = self.text_text.get("1.0", tk.END).strip()
        filename = self.filename_entry.get().strip()
        template_type = self.template_var.get()
        
        # اعتبارسنجی
        if not name:
            messagebox.showerror("خطا", "لطفاً نام را وارد کنید!")
            return
        
        if not text:
            messagebox.showerror("خطا", "لطفاً متن اصلی را وارد کنید!")
            return
        
        if not filename:
            filename = "landing_page"
        
        # انتخاب تمپلیت
        template = self.templates[template_type]
        
        # پردازش عکس
        img_html = self.process_image(self.image_path, template_type)
        
        # جایگزینی متغیرها
        html = template
        html = html.replace("{{نام}}", name)
        html = html.replace("{{متن}}", text)
        html = html.replace("{{رنگ1}}", self.colors[0])
        html = html.replace("{{رنگ2}}", self.colors[1])
        html = html.replace("{{رنگ3}}", self.colors[2])
        html = html.replace("{{سال}}", str(datetime.now().year))
        
        # جایگزینی عکس‌ها
        if template_type == "مدرن":
            html = html.replace("{{عکس_هدر}}", img_html)
        else:
            html = html.replace("{{عکس_محتوا}}", img_html)
        
        # ذخیره فایل
        output_dir = "generated_pages"
        os.makedirs(output_dir, exist_ok=True)
        
        # اگر فایل html نبود، اضافه کن
        if not filename.endswith('.html'):
            filename += '.html'
        
        output_path = os.path.join(output_dir, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # نمایش موفقیت
        messagebox.showinfo(
            "موفقیت! 🎉",
            f"لندینگ پیج شما با موفقیت ساخته شد!\n\n"
            f"فایل: {output_path}\n"
            f"قالب: {template_type}\n\n"
            f"برای مشاهده، فایل HTML را در مرورگر باز کنید."
        )
        
        # باز کردن پوشه خروجی
        try:
            os.startfile(output_dir)
        except:
            # برای لینوکس و مک
            try:
                os.system(f'open "{output_dir}"')
            except:
                pass

def main():
    root = tk.Tk()
    app = LandingPageCreator(root)
    root.mainloop()

if __name__ == "__main__":
    main()