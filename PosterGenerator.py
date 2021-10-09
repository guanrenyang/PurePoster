
from ast import parse
from pyexpat import ErrorString
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import argparse

dict_Font_Path = {  'XiangSu'           : './font/zpix.ttf',
                    'FangSong'          : './font/FangSong.ttf',
                    'HeiTi'             : './font/HeiTi.ttf',
                    'HuaWenFangSong'    : './font/HuaWenFangSong.ttf',
                    'HuaWenHeiTi'       : './font/HuaWenHeiTi.ttf',
                    'HuaWenKaiTi'       : './font/HuaWenKaiTi.ttf',
                    'HuaWenLiShu'       : './font/HuaWenLiShu.ttf',
                    'HuaWenSongTi'      : './font/HuaWenSongTi.ttf',
                    'KaiTi'             : './font/KaiTi.ttf',
                    'LiShu'             : './font/LiShu.ttf',
                    'YouYuan'           : './font/YouYuan.ttf'}

dict_Resolution_Ratio = {'iphone11': (828, 1792)}

'''text
text是一个列表, 例如['abc de','/','fg','hij']表示:
adc de

gf
hij'''

def init_args():
    '''initialize arguments'''
    parser = argparse.ArgumentParser()

    parser.add_argument('--text', default='Therefore,,send-not-to-know,,For-who-the-bell-tolls,,It tolls for thee.')
    parser.add_argument('--device', default='iphone11')
    parser.add_argument('--fontColor', default='#ED955F')
    parser.add_argument('--backgroundColor', default='#467794')
    parser.add_argument('--fontSize', default='80')
    parser.add_argument('--fontType', default='KaiTi')
    parser.add_argument('--resolutionRatio',default='(1920,1080)')

    return parser.parse_args()

def preprocess(text):
    processed_text = ''
    for char in text:
        processed_text += (char if char!='-' else ' ')
    
    processed_text = processed_text.split(',')
    
    for index, item in enumerate(processed_text):
        if item=='':
            processed_text[index] = ' '

    return processed_text
def str_to_tuple(string):
    result_tuple = tuple()
    string = string.replace('(','')
    string = string.replace(')','')
    
    list = string.split(',')
    for item in list:
        result_tuple += (int(item),)
    
    return result_tuple
def get_text_position(text, font, background_size): # 这个画图计算一下
    
    text_position = []

    background_width, background_height = background_size[0], background_size[1]
    
    textWidthList = [font.getsize(line)[0] for line in text]
    textHeightList = [font.getsize(line)[1] for line in text]

    total_text_width = max(textWidthList)
    total_text_height = sum(textHeightList) # why difference

    base_y = (background_height-total_text_height)/2
    base_x = (background_width-total_text_width)/2

    for line_index, line in enumerate(text):
        text_x = base_x + abs(total_text_width-textWidthList[line_index])/2
        text_y = base_y + sum(textHeightList[0:line_index])
        text_position.append((text_x, text_y))
    
    return text_position


    
def make_poster(text, resolutionRatio, fontType, fontSize, fontColor, backgroundColor):

    fontPath = dict_Font_Path[fontType]
    pictureSize = resolutionRatio
    background_width, background_height = pictureSize[0], pictureSize[1]

    # create `background` object
    image = Image.new('RGB', (background_width, background_height), color=backgroundColor)

    # create `Font` object
    font = ImageFont.truetype(fontPath, fontSize, encoding='utf-8')

    # create `Draw` object
    draw = ImageDraw.Draw(image)
    

    textPositionList = get_text_position(text, font, (background_width, background_height))
    '''textSize是一个list，里面每一个元素都是2-tuple，表示每一句话的起始位置'''
    for line_index, line in enumerate(text):
        draw.text(textPositionList[line_index], text[line_index], fill=fontColor, font=font)

    image.save('PurePoster.jpg', 'jpeg')

if __name__ == '__main__':

    args = init_args()

    text = preprocess(args.text)
    device = args.device
    fontColor = args.fontColor
    backgroundColor = args.backgroundColor
    fontType = args.fontType
    fontSize = int(args.fontSize)
    resolutionRatio = str_to_tuple(args.resolutionRatio) # Temporarily, the argument is not used. We use `device` indeed

    '''`text` should be such format: 'eat food,,today':
    eat food

    today'''

    make_poster(text=text, resolutionRatio=resolutionRatio, fontType=fontType,fontSize=fontSize, fontColor=fontColor, backgroundColor=backgroundColor)

    print('==========Finish==========')