import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image,ImageSequence
# 2. 截图HTML内容
overlap_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'xianyu_overlap.png')
overlap_path='E:/Songcf/Desktop/code/nonebot/chem-bot-plus/chem-bot-plus/plugins/chem_bot_main/xianyu_overlap.png'
def capture_html_screenshot(image_path,overlap_text):
    file_name = os.path.basename(image_path)
    file_dir = os.path.dirname(image_path)
    file_name_without_extension, file_extension = os.path.splitext(file_name)
    html_file_path=file_dir+'/'+file_name_without_extension+'_'+overlap_text+'.html'
    output_image_path=file_dir+'/'+file_name_without_extension+'_'+overlap_text+'_output.png'
    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write("""
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {position: relative;margin: 0;}
        .backimage {width: 100%;filter: saturate(0.3);}
        canvas {width: 100%;position: absolute;
            top: 50%;right: -50%;transform: translate(-50%, -50%);}
    </style>
    <title>Canvas Text Mask Example</title>
</head>
<body>
    <img src='"""+image_path+"""' class="backimage">
    <canvas id="canvas"></canvas>
    <script>
        const canvas = document.getElementById('canvas');
        canvas.width = 600;
        canvas.height = 600;
        const ctx = canvas.getContext('2d');
        const image = new Image();
        image.src = '"""+overlap_path+"""'; 
        image.onload = function() {
            ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
            ctx.font = 'bold 96px "Source Han Sans"';
            ctx.fillStyle = 'white'; 
            ctx.textAlign = 'center'; 
            ctx.textBaseline = 'middle';
            ctx.translate(canvas.width / 2, canvas.height / 2);
            ctx.transform(0.8, -0.22, 0.05, 0.9, -20, 0);
            const text = '"""+overlap_text+"""'
            if(ctx.measureText(text).width>300)ctx.transform(0.9,0,0,1,0,0);
            ctx.globalCompositeOperation = 'destination-out';
            ctx.fillText(text, 0, 0);
        };
    </script>
</body>
</html>
""")
    print(f"HTML file created at: {html_file_path}")
    # 设置Selenium WebDriver
    width=600
    height=600
    with Image.open(image_path) as img:
        width=img.width
        height=img.height
    if(width>height):
        width=int(width*600/height+1)+22
        height=600+150
    else:
        height=int(height*600/width)+150
        width=600+22
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 无头模式
    options.add_argument("--disable-gpu")
    options.add_argument(f"--window-size={width},{height}")  # 设置窗口大小

    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 加载HTML文件
        driver.get(f"file://{os.path.abspath(html_file_path)}")

        # 等待页面加载完成
        driver.implicitly_wait(2)
        driver.execute_script("""
        document.documentElement.style.overflowY = 'hidden';
        document.documentElement.style.overflowX = 'hidden';
        """)
        current_size = driver.get_window_size()
        print(f"当前窗口宽度: {current_size['width']}")
        print(f"当前窗口高度: {current_size['height']}")
        # 截图并保存
        driver.save_screenshot(output_image_path)
        print(f"Screenshot saved to: {output_image_path}")
        return output_image_path
    finally:
        # 关闭WebDriver
        driver.quit()
