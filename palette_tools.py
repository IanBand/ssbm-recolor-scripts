import shutil
import math
import numpy as np

#https://github.com/marco-calautti/Rainbow/blob/master/Rainbow.ImgLib/ImgLib/Common/ImageUtils.cs
#https://beesbuzz.biz/code/16-hsv-color-transforms, yes, the first example they give of matrix * vector multiplication is wrong

cc38 = [ # convert 3-bit color to 8-bit color
    0x00,0x24,0x49,0x6d, 0x92,0xb6,0xdb,0xff
]
cc48 = [ # convert 4-bit color to 8-bit color
    0x00,0x11,0x22,0x33, 0x44,0x55,0x66,0x77, 0x88,0x99,0xaa,0xbb, 0xcc,0xdd,0xee,0xff
]
cc58 = [ # convert 5-bit color to 8-bit color
    0x00,0x08,0x10,0x19, 0x21,0x29,0x31,0x3a, 0x42,0x4a,0x52,0x5a, 0x63,0x6b,0x73,0x7b,
    0x84,0x8c,0x94,0x9c, 0xa5,0xad,0xb5,0xbd, 0xc5,0xce,0xd6,0xde, 0xe6,0xef,0xf7,0xff
]
cc83 = [ # convert 8-bit color to 3-bit color
    0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x01, 0x01,0x01,0x01,0x01, 0x01,0x01,0x01,0x01, 0x01,0x01,0x01,0x01,
    0x01,0x01,0x01,0x01, 0x01,0x01,0x01,0x01, 0x01,0x01,0x01,0x01, 0x01,0x01,0x01,0x01,
    0x01,0x01,0x01,0x01, 0x01,0x01,0x01,0x02, 0x02,0x02,0x02,0x02, 0x02,0x02,0x02,0x02,
    0x02,0x02,0x02,0x02, 0x02,0x02,0x02,0x02, 0x02,0x02,0x02,0x02, 0x02,0x02,0x02,0x02,
    0x02,0x02,0x02,0x02, 0x02,0x02,0x02,0x02, 0x02,0x02,0x02,0x02, 0x03,0x03,0x03,0x03,
    0x03,0x03,0x03,0x03, 0x03,0x03,0x03,0x03, 0x03,0x03,0x03,0x03, 0x03,0x03,0x03,0x03,
    0x03,0x03,0x03,0x03, 0x03,0x03,0x03,0x03, 0x03,0x03,0x03,0x03, 0x03,0x03,0x03,0x03,
    0x04,0x04,0x04,0x04, 0x04,0x04,0x04,0x04, 0x04,0x04,0x04,0x04, 0x04,0x04,0x04,0x04,
    0x04,0x04,0x04,0x04, 0x04,0x04,0x04,0x04, 0x04,0x04,0x04,0x04, 0x04,0x04,0x04,0x04,
    0x04,0x04,0x04,0x04, 0x05,0x05,0x05,0x05, 0x05,0x05,0x05,0x05, 0x05,0x05,0x05,0x05,
    0x05,0x05,0x05,0x05, 0x05,0x05,0x05,0x05, 0x05,0x05,0x05,0x05, 0x05,0x05,0x05,0x05,
    0x05,0x05,0x05,0x05, 0x05,0x05,0x05,0x05, 0x05,0x06,0x06,0x06, 0x06,0x06,0x06,0x06,
    0x06,0x06,0x06,0x06, 0x06,0x06,0x06,0x06, 0x06,0x06,0x06,0x06, 0x06,0x06,0x06,0x06,
    0x06,0x06,0x06,0x06, 0x06,0x06,0x06,0x06, 0x06,0x06,0x06,0x06, 0x06,0x07,0x07,0x07,
    0x07,0x07,0x07,0x07, 0x07,0x07,0x07,0x07, 0x07,0x07,0x07,0x07, 0x07,0x07,0x07,0x07
]
cc84 = [ # convert 8-bit color to 4-bit color
    0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00, 0x00,0x01,0x01,0x01, 0x01,0x01,0x01,0x01,
    0x01,0x01,0x01,0x01, 0x01,0x01,0x01,0x01, 0x01,0x01,0x02,0x02, 0x02,0x02,0x02,0x02,
    0x02,0x02,0x02,0x02, 0x02,0x02,0x02,0x02, 0x02,0x02,0x02,0x03, 0x03,0x03,0x03,0x03,
    0x03,0x03,0x03,0x03, 0x03,0x03,0x03,0x03, 0x03,0x03,0x03,0x03, 0x04,0x04,0x04,0x04,
    0x04,0x04,0x04,0x04, 0x04,0x04,0x04,0x04, 0x04,0x04,0x04,0x04, 0x04,0x05,0x05,0x05,
    0x05,0x05,0x05,0x05, 0x05,0x05,0x05,0x05, 0x05,0x05,0x05,0x05, 0x05,0x05,0x06,0x06,
    0x06,0x06,0x06,0x06, 0x06,0x06,0x06,0x06, 0x06,0x06,0x06,0x06, 0x06,0x06,0x06,0x07,
    0x07,0x07,0x07,0x07, 0x07,0x07,0x07,0x07, 0x07,0x07,0x07,0x07, 0x07,0x07,0x07,0x07,
    0x08,0x08,0x08,0x08, 0x08,0x08,0x08,0x08, 0x08,0x08,0x08,0x08, 0x08,0x08,0x08,0x08,
    0x08,0x09,0x09,0x09, 0x09,0x09,0x09,0x09, 0x09,0x09,0x09,0x09, 0x09,0x09,0x09,0x09,
    0x09,0x09,0x0a,0x0a, 0x0a,0x0a,0x0a,0x0a, 0x0a,0x0a,0x0a,0x0a, 0x0a,0x0a,0x0a,0x0a,
    0x0a,0x0a,0x0a,0x0b, 0x0b,0x0b,0x0b,0x0b, 0x0b,0x0b,0x0b,0x0b, 0x0b,0x0b,0x0b,0x0b,
    0x0b,0x0b,0x0b,0x0b, 0x0c,0x0c,0x0c,0x0c, 0x0c,0x0c,0x0c,0x0c, 0x0c,0x0c,0x0c,0x0c,
    0x0c,0x0c,0x0c,0x0c, 0x0c,0x0d,0x0d,0x0d, 0x0d,0x0d,0x0d,0x0d, 0x0d,0x0d,0x0d,0x0d,
    0x0d,0x0d,0x0d,0x0d, 0x0d,0x0d,0x0e,0x0e, 0x0e,0x0e,0x0e,0x0e, 0x0e,0x0e,0x0e,0x0e,
    0x0e,0x0e,0x0e,0x0e, 0x0e,0x0e,0x0e,0x0f, 0x0f,0x0f,0x0f,0x0f, 0x0f,0x0f,0x0f,0x0f
]
cc85 = [ # convert 8-bit color to 5-bit color
    0x00,0x00,0x00,0x00, 0x00,0x01,0x01,0x01, 0x01,0x01,0x01,0x01, 0x01,0x02,0x02,0x02,
    0x02,0x02,0x02,0x02, 0x02,0x03,0x03,0x03, 0x03,0x03,0x03,0x03, 0x03,0x04,0x04,0x04,
    0x04,0x04,0x04,0x04, 0x04,0x04,0x05,0x05, 0x05,0x05,0x05,0x05, 0x05,0x05,0x06,0x06,
    0x06,0x06,0x06,0x06, 0x06,0x06,0x07,0x07, 0x07,0x07,0x07,0x07, 0x07,0x07,0x08,0x08,
    0x08,0x08,0x08,0x08, 0x08,0x08,0x09,0x09, 0x09,0x09,0x09,0x09, 0x09,0x09,0x09,0x0a,
    0x0a,0x0a,0x0a,0x0a, 0x0a,0x0a,0x0a,0x0b, 0x0b,0x0b,0x0b,0x0b, 0x0b,0x0b,0x0b,0x0c,
    0x0c,0x0c,0x0c,0x0c, 0x0c,0x0c,0x0c,0x0d, 0x0d,0x0d,0x0d,0x0d, 0x0d,0x0d,0x0d,0x0d,
    0x0e,0x0e,0x0e,0x0e, 0x0e,0x0e,0x0e,0x0e, 0x0f,0x0f,0x0f,0x0f, 0x0f,0x0f,0x0f,0x0f,
    0x10,0x10,0x10,0x10, 0x10,0x10,0x10,0x10, 0x11,0x11,0x11,0x11, 0x11,0x11,0x11,0x11,
    0x12,0x12,0x12,0x12, 0x12,0x12,0x12,0x12, 0x12,0x13,0x13,0x13, 0x13,0x13,0x13,0x13,
    0x13,0x14,0x14,0x14, 0x14,0x14,0x14,0x14, 0x14,0x15,0x15,0x15, 0x15,0x15,0x15,0x15,
    0x15,0x16,0x16,0x16, 0x16,0x16,0x16,0x16, 0x16,0x16,0x17,0x17, 0x17,0x17,0x17,0x17,
    0x17,0x17,0x18,0x18, 0x18,0x18,0x18,0x18, 0x18,0x18,0x19,0x19, 0x19,0x19,0x19,0x19,
    0x19,0x19,0x1a,0x1a, 0x1a,0x1a,0x1a,0x1a, 0x1a,0x1a,0x1b,0x1b, 0x1b,0x1b,0x1b,0x1b,
    0x1b,0x1b,0x1b,0x1c, 0x1c,0x1c,0x1c,0x1c, 0x1c,0x1c,0x1c,0x1d, 0x1d,0x1d,0x1d,0x1d,
    0x1d,0x1d,0x1d,0x1e, 0x1e,0x1e,0x1e,0x1e, 0x1e,0x1e,0x1e,0x1f, 0x1f,0x1f,0x1f,0x1f
]

#uint16 color = 1RRRRRGGGGGBBBBB
#uint16 color = 0AAARRRRGGGGBBBB

def encode16bitColor(color):
    uint16 = 0
    #check if alpha channel is supplied and is not too large
    if len(color) == 4 and color[3] < 224: #224 is the threshold that DTW uses
        r = cc84[color[0]]
        g = cc84[color[1]]
        b = cc84[color[2]]
        a = cc83[color[3]]
        uint16 = (a << 12) + (r << 8) + (g << 4) + b

    else:
        r = cc85[color[0]]
        g = cc85[color[1]]
        b = cc85[color[2]]
        uint16 = (1 << 15) + (r << 10) + (g << 5) + b
    
    return bytes([uint16 >> 8, uint16 & 0xff])
        

def decode16bitColor(uint16):
    
    word = int.from_bytes(uint16, "big") 

    color = [0,0,0]

    #check if alpha channel is used
    if word >> 15 == 1:
        color[0] = cc58[word >> 10 & 0b11111]
        color[1] = cc58[word >> 5  & 0b11111]
        color[2] = cc58[word       & 0b11111]
    else:
        color[0] = cc48[word >> 8 & 0b1111]
        color[1] = cc48[word >> 4  & 0b1111]
        color[2] = cc48[word       & 0b1111]
        color.append(cc38[word >> 12 & 0b111])
    return color

def transformHSV(color, hue, s=1, v=1):


    vsu = v*s*math.cos(hue*math.pi / 180)
    vsw = v*s*math.sin(hue*math.pi / 180)
    ret = [0,0,0]

    ret[0] = np.clip(round((.299*v + .701*vsu + .168*vsw)*color[0]
                         + (.587*v - .587*vsu + .330*vsw)*color[1]
                         + (.114*v - .114*vsu - .497*vsw)*color[2]), 0, 255)
    ret[1] = np.clip(round((.299*v - .299*vsu - .328*vsw)*color[0]
                         + (.587*v + .413*vsu + .035*vsw)*color[1]
                         + (.114*v - .114*vsu + .292*vsw)*color[2]), 0, 255)
    ret[2] = np.clip(round((.299*v - .300*vsu + 1.25*vsw)*color[0]
                         + (.587*v - .588*vsu - 1.05*vsw)*color[1]
                         + (.114*v + .886*vsu - .203*vsw)*color[2]), 0, 255)
    return ret

'''
with open(newName, mode='r+b') as file: # b is important -> binary


    for palette in palettes:

        offset = palette[0]
        colors = palette[1]

        for i in range(0, colors):
            file.seek(offset + clen * i)

            color16 = file.read(clen)
            colors = decode16bitColor(color16)

            newColors = transformHSV(colors, 313)
            if(len(colors) == 4):
                newColors.append(colors[3])

            file.seek(offset + clen * i)
            file.write(encode16bitColor(newColors))

print("done!")
'''




