from PIL import Image, ImageDraw, ImageFont

# Create Skills Screenshot
img = Image.new('RGB', (800, 500), color='white')
d = ImageDraw.Draw(img)

d.text((20, 20), 'SKILLS', fill='black')

skills = [
    'Python', 'JavaScript', 'Docker', 'Kubernetes', 'AWS', 
    'Google Cloud Platform', 'CI/CD', 'DevOps', 'React', 
    'Node.js', 'FastAPI', 'Terraform', 'PostgreSQL', 
    'Cloud Architecture', 'Microservices'
]

for i, skill in enumerate(skills):
    x = 20 + (i % 3) * 250
    y_pos = 60 + (i // 3) * 40
    d.rectangle([x, y_pos, x+230, y_pos+30], outline='#0077B5', width=2)
    d.text((x+10, y_pos+8), skill, fill='black')

img.save('test_data/linkedin_screenshot_2.png')
print('Created linkedin_screenshot_2.png')
