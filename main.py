# -*- coding: utf-8 -*-
from PIL import Image,  ImageFont, ImageDraw
import pandas as pd
import numpy as np
from textwrap import TextWrapper
from younet_rnd_infrastructure.tri.common import utils
X = 390
Y = 200
Y_MIN = 100
X_MIN = 200
WIDTH = 586
HEIGHT = 268
NUMBER_CHARACTERS_PER_LINE = 40
FONT_SIZE = 30

if __name__ == '__main__':
    # Loader
    resources_path = './resources/'
    color = pd.read_csv(resources_path + 'color.csv')
    quote = pd.read_json(resources_path + 'quotes.json', encoding='utf-8')
    number_image = 300
    for i in range(number_image):
        color_picked = np.random.randint(0, color.shape[0])
        quote_picked = np.random.randint(0, quote.shape[0])

        new_image = Image.new('RGB', (1366, 768), color.loc[color_picked, 'background'])
        d = ImageDraw.Draw(new_image)
        font_size = FONT_SIZE

        fnt = ImageFont.truetype(resources_path + 'font/Merriweather-Light.ttf', font_size)

        text_origin = quote.loc[quote_picked, 'quote']
        text_size = d.textsize(text=text_origin, font=fnt)

        wrapper = TextWrapper()
        wrapper.width = int(NUMBER_CHARACTERS_PER_LINE)
        text = wrapper.fill(quote.loc[quote_picked, 'quote'])
        text_size = d.textsize(text=text, font=fnt)
        Y = (768 - text_size[1]) / 2
        number_character_per_line = NUMBER_CHARACTERS_PER_LINE
        while Y < Y_MIN:
            wrapper.width += 1
            text = wrapper.fill(text_origin)
            text_size = d.textsize(text=text, font=fnt)
            X = (1366 - text_size[0]) / 2
            Y = (768 - text_size[1]) / 2
            if X < X_MIN:
                break

        while (X < X_MIN) or (Y < Y_MIN):
            font_size -= 1
            fnt = ImageFont.truetype(resources_path + 'font/Merriweather-Light.ttf', font_size)
            text_size = d.textsize(text=text, font=fnt)
            X = (1366 - text_size[0]) / 2
            Y = (768 - text_size[1]) / 2

        d.text(xy=(X, Y), text=text, font=fnt, fill=color.loc[color_picked, 'text'])

        fnt = ImageFont.truetype(resources_path + 'font/Merriweather-Bold.ttf', font_size)
        d.text(xy=(X + WIDTH*2/3, Y + text_size[1] + 15), text=u'— %s' % quote.loc[quote_picked, 'author'], font=fnt,
               fill=color.loc[color_picked, 'text'])

        new_image.save('E:\\images\\quotes_background\\%s_%s_%s.png' %
                       (utils.get_time_now_str().replace(':', ''), color_picked, quote_picked))
        print 'Done %s/%s' % (i, number_image)