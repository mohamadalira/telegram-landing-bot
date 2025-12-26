def generate_landing(template_number, data):
    templates = {
        1: "template1.html",
        2: "template2.html", 
        3: "template3.html"
    }
    
    with open(templates[template_number], 'r', encoding='utf-8') as f:
        html = f.read()
    
    # جایگذاری متغیرها
    html = html.replace("{{نام}}", data['name'])
    html = html.replace("{{متن_اصلی}}", data['text'])
    html = html.replace("{{آدرس_عکس}}", data['image_url'])
    html = html.replace("{{رنگ_اول}}", data['colors'][0])
    html = html.replace("{{رنگ_دوم}}", data['colors'][1])
    html = html.replace("{{رنگ_سوم}}", data['colors'][2])
    html = html.replace("{{سال_جاری}}", str(datetime.now().year))
    
    return html