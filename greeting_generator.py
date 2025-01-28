from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import os
import base64
from io import BytesIO

class GreetingGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), base_url=os.getenv('OPENAI_API_BASE'))
        self.font_path = os.path.join('static', 'fonts', 'STXINGKA.TTF')
        
        # Ensure the fonts directory exists
        os.makedirs(os.path.join('static', 'fonts'), exist_ok=True)
        
        # Download font if not exists
        if not os.path.exists(self.font_path):
            # Note: In production, you should download the font from a reliable source
            raise FileNotFoundError("Please download STXINGKA.TTF font and place it in the static/fonts directory")

    def generate_greeting(self, recipient, extra_requirements=""):
        prompt = f"""请为{recipient}生成一段温暖、独特且充满诚意的春节祝福语。
要求：
1. 祝福语要体现出对{recipient}的个性化关怀，最好能结合语境巧妙结合接受者的名字，让人眼前一亮。
2. 语言要优美、富有文采，但不要过于生硬
3. 长度在100字左右
4. 要包含传统节日元素
5. 今年是2025蛇年。
{f'6. 额外要求：{extra_requirements}' if extra_requirements else ''}
7. 不要输出其他内容"""
        print("getting blessing...")
        response = self.client.chat.completions.create(
            model="qwen-max-2025-01-25",
            messages=[
                {"role": "system", "content": "你是一个擅长写祝福语的文学家，特别擅长写应景且别出心裁的春节祝福。"},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        
        collected_messages = []
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end='', flush=True)
                collected_messages.append(content)
                
        return ''.join(collected_messages).strip()
    def generate_couplet(self, recipient):
        prompt = f"""请为{recipient}生成一副春联。
要求：
1. 上下联字数相同（建议7-9字）
2. 符合平仄要求
3. 意境优美
4. 可以巧妙地将{recipient}的名字融入其中
5. 横批要与上下联相呼应（4字以内）

请按照以下格式返回，不要输出其他内容：
上联：xxx
下联：xxx
横批：xxx"""
        print("getting couplet...")
        response = self.client.chat.completions.create(
            model="qwen-max-2025-01-25",
            messages=[
                {"role": "system", "content": "你是一个精通对联的AI助手，特别擅长创作符合平仄、意境优美的春联。"},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        
        collected_messages = []
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end='', flush=True)
                collected_messages.append(content)
                
        couplet_text = ''.join(collected_messages).strip()
        return self._parse_couplet(couplet_text)
    def _parse_couplet(self, couplet_text):
        lines = couplet_text.split('\n')
        horizontal = ""
        upper = ""
        lower = ""
        
        for line in lines:
            if '横批：' in line:
                horizontal = line.split('：')[1].strip()
            elif '上联：' in line:
                upper = line.split('：')[1].strip()
            elif '下联：' in line:
                lower = line.split('：')[1].strip()
        
        return horizontal, upper, lower

    def generate_couplet_image(self, horizontal, upper, lower):
        # Create a new image with a red background
        width = 800
        height = 1200
        img = Image.new('RGB', (width, height), color='#e60012')
        draw = ImageDraw.Draw(img)

        # Load the font
        horizontal_font = ImageFont.truetype(self.font_path, 80)
        couplet_font = ImageFont.truetype(self.font_path, 60)

        # Draw the horizontal text
        h_bbox = draw.textbbox((0, 0), horizontal, font=horizontal_font)
        h_width = h_bbox[2] - h_bbox[0]
        draw.text(((width - h_width) // 2, 50), horizontal, font=horizontal_font, fill='gold')

        # Draw the upper couplet
        u_bbox = draw.textbbox((0, 0), upper, font=couplet_font)
        u_height = u_bbox[3] - u_bbox[1]
        vertical_spacing = (height - 200 - u_height) // (len(upper) + 1)
        
        for i, char in enumerate(upper):
            char_bbox = draw.textbbox((0, 0), char, font=couplet_font)
            char_width = char_bbox[2] - char_bbox[0]
            x = 150 - char_width // 2
            y = 200 + i * vertical_spacing
            draw.text((x, y), char, font=couplet_font, fill='gold')

        # Draw the lower couplet
        for i, char in enumerate(lower):
            char_bbox = draw.textbbox((0, 0), char, font=couplet_font)
            char_width = char_bbox[2] - char_bbox[0]
            x = width - 150 - char_width // 2
            y = 200 + i * vertical_spacing
            draw.text((x, y), char, font=couplet_font, fill='gold')

        # Convert the image to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str 
