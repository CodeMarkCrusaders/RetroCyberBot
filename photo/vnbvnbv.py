from PIL import Image , ImageFilter, ImageDraw, ImageFont, ImageEnhance
from random import randint

font1 = ImageFont.truetype('Fallout.ttf',size= 45)

img = Image.open('apter.png').convert('RGBA')

idraw = ImageDraw.Draw(img)
font = ImageFont.truetype('Fallout.ttf',size= 55)

def line_wrapping(img , font , text , x_start, x_finish = None):

    x_img , y_img  = img.size

    if x_finish == None:

        x_finish = x_img

    text_box = x_finish - x_start

    split_text = ''
    line = ''

    for char in text:

        line += char 
        if font.getsize(line)[0] >= text_box:
            line += '\n'
            split_text += line
            line = ''

    return split_text

a = 'asdadassssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss'*100
text = line_wrapping(img , font , a ,0,1920)
idraw.multiline_text((440,24) , text , font = font, fill=(75,252,151), )
print(font.getsize('as')[1])
#idraw.text((795,743) , 'но не холодным.' , font = font, fill=(75,252,151))
#idraw.text((109,30) , 'Т' , font = font1, fill=(75,252,151))

img.save('photo\\apter12.png', quality=100, subsampling=0)
img.show()