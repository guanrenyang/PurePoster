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
    '''
    Initialize command line arguments:
    Arguments:
        `text`: The text that needs to be displayed. Endline character is ',' and you must use '-' instead of spaces. # 换行符最好改为.
        `fontColor`: The color of text, must in format '#00000' representing a color
        `backgroundColor`: The color of background, must in format `#000000` representing a color
        `fontSize`: The size of font, must be an `int`
        `fontType`: The type of font. You could refer to the table in the README.md to find the allowed parameters
        `resolutionRatio`: The resolution ratio of the picture. Suggested format is '(1920,1080)`
        `save`: The file type of saved type, e.g. 'png'
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument('--text', default='Therefore,,send-not-to-know,,For-who-the-bell-tolls,,It tolls for thee.')
    parser.add_argument('--device', default='iphone11') # The argument makes no sense
    parser.add_argument('--fontColor', default='#ED955F')
    parser.add_argument('--backgroundColor', default='#467794')
    parser.add_argument('--fontSize', default='80')
    parser.add_argument('--fontType', default='KaiTi')
    parser.add_argument('--resolutionRatio',default='(1920,1080)')
    parser.add_argument('--save', default='png')

    return parser.parse_args()

def preprocess(text: str):
    '''
    Replace '-' in text with ' ' and split the string with ','. 
    Return a list of strings, each of which represents a line.
    Args:
        `text` is the raw text, e.g. 'Hi-Mike,,How are you?'
    Return:
        ->list, e.g.['Hi Mike', ' ', 'How are you?']
    '''
    processed_text = ''
    for char in text:
        processed_text += (char if char!='-' else ' ')
    
    processed_text = processed_text.split(',')
    
    for index, item in enumerate(processed_text):
        if item=='':
            processed_text[index] = ' '

    return processed_text
def str_to_tuple(string: str):
    '''
    Convert the resolution in `str` into `tuple` format, e.g. '(1920,1080)'->(1920,1080)
    Args:
        string: a string in format '(1920,1080)'
    Return:
        ->tuple: (1920,1080)
        '''
    result_tuple = tuple()
    string = string.replace('(','')
    string = string.replace(')','')
    
    list = string.split(',')
    for item in list:
        result_tuple += (int(item),)
    
    return result_tuple



    
def make_poster(text, resolutionRatio, fontType, fontSize, fontColor, backgroundColor, saveFileType='png'):
    '''
    Make a poster according to the input arguments.
    Arguments:
        `text`: The text that needs to be displayed. In `list` format, each list entry is in `str` format representing a line.
        `fontColor`: The color of text, must in format '#00000' representing a color
        `backgroundColor`: The color of background, must in format `#000000` representing a color
        `fontSize`: The size of font, must be an `int`
        `fontType`: The type of font. You could refer to the table in the README.md to find the allowed parameters
        `resolutionRatio`: The resolution ratio of the picture. In format `tuple`, e.g. (1920,1080)
        `save`: The file type of saved type, e.g. 'png'
        '''
    def get_text_position(text, font, background_size): # 这个画图计算一下
        '''
        Returns the starting coordinates of each line in pixel coordinate with text displayed in the center.
        Args:
            `text`: The text that needs to be displayed. In `list` format, each list entry is in `str` format representing a line.
            `font`: A `PIL` `FreeFontType` instance.
            `backgournd_size`: A `tuple` representing the background size, e.g. (1920,1080), which is equal to the resolution ratio.
        Return:
            ->`list`. Each entry is a `tuple`, the ith entry representing the starting coordinate of the ith line.
                    e.g. [(0,0), (100,100)]
        '''
        
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

    fontPath = dict_Font_Path[fontType] # The path of the font size
    pictureSize = resolutionRatio 
    background_width, background_height = pictureSize[0], pictureSize[1]

    # create `background` object
    image = Image.new('RGB', (background_width, background_height), color=backgroundColor)

    # create `Font` object
    font = ImageFont.truetype(fontPath, fontSize, encoding='utf-8')

    # create `Draw` object
    draw = ImageDraw.Draw(image)
    

    textPositionList = get_text_position(text, font, (background_width, background_height))

    
    for line_index, line in enumerate(text):
        draw.text(textPositionList[line_index], text[line_index], fill=fontColor, font=font)

    image.save('PurePoster.'+saveFileType, saveFileType)
    
    
    

if __name__ == '__main__':

    # initialize arguments
    args = init_args()

    # set arguments
    text = preprocess(args.text)
    device = args.device
    fontColor = args.fontColor
    backgroundColor = args.backgroundColor
    fontType = args.fontType
    fontSize = int(args.fontSize)
    resolutionRatio = str_to_tuple(args.resolutionRatio) # Temporarily, the argument is not used. We use `device` indeed
    saveFileType = args.save

    # generate poster
    make_poster(text=text, resolutionRatio=resolutionRatio, fontType=fontType,fontSize=fontSize, fontColor=fontColor, backgroundColor=backgroundColor, saveFileType=saveFileType)

