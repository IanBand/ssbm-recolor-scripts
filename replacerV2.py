
import shutil
import math
from palette_tools import encode16bitColor, decode16bitColor, transformHSV 

# ssbm electric recoloring script
#
# Thanks to: OmnipotentSpoon, Lanceinthepants, Achilles1515
#
# OFFSETS STILL MISSING: 
# electric hitstun character model overlay offset, likely in EfCoData.dat
# string-like blue and white effect in pikachu's fsmash

#https://smashboards.com/threads/changing-color-effects-in-melee.313177/post-13573241
#https://smashboards.com/threads/changing-color-effects-in-melee.313177/post-18577363
#source files for every relevant electric effect in the game
EfCoData = "EfCoData.dat" #all common
EfFxData = "EfFxData.dat" #spacies common 
PlFc = "PlFc.dat" #falco
PlFx = "PlFx.dat" #fox
EfPkData = "EfPkData.dat" #pika common
PlPk = "PlPk.dat" #pikachu
PlPc = "PlPc.dat" #pichu
EfNsData = "EfNsData.dat"
PlNs = "PlNs.dat" #ness
EfSsData = "EfSsData.dat"
PlSs = "PlSs.dat" #samus 
#add zelda (neutral b)

#bowser (up & side b)
#yoshi egg break sparkles
#ICs up b
#DK neutral B, side b
#peach float
#link, arrow trail
#g&w 9

modName = "purple-electric-" #prefix for output files
elecColor1 = [0xff, 0xff, 0xff] #generally the inner color
elecColor2 = [174, 0, 255] #generally the outter color
hueShift = 300 #hue shift for paletted textures and matrix offsets

createdFiles = {}

#palette info
paletteData = {
    "PlSs.dat" :[
        (0x18480, 103),
        (0x193a0, 81),
        (0x19480, 83),
        (0x1b3a0, 103),
        (0x34ee0, 81),
        (0x34fc0, 83)
    ]
} 

def touchOutFile(filename):
    if not (modName + filename) in createdFiles:
        shutil.copy(filename, modName + filename)
        createdFiles[modName + filename] = True

def shiftPaletteColors(filename):
    
    touchOutFile(filename)
    with open(modName + filename, mode='r+b') as f:
        for data in paletteData[filename]:
            for i in range(0, data[1]):
                f.seek(data[0] + i * 2)
                color16 = f.read(2)
                color = decode16bitColor(color16)

                newColors = transformHSV(color, hueShift)
                if(len(color) == 4):
                    newColors.append(color[3])

                f.seek(data[0] + i * 2)
                f.write(encode16bitColor(newColors))





#the reason we shift hues for palettes and 98 structures is because the colors that are already there contain "intensity" information 
def shift98colors(filename, offset, pad, hue):

    touchOutFile(filename)

    with open(modName + filename, mode='r+b') as f:
        f.seek(offset + 1)
        length = int.from_bytes(f.read(2), 'big')

        for i in range(0, length):
            f.seek(offset + 4 + i * (2 + pad))
            color16 = f.read(2)
            color = decode16bitColor(color16)

            newColors = transformHSV(color, hueShift)
            if(len(color) == 4):
                newColors.append(color[3])

            f.seek(offset + 4 + i * (2 + pad))
            f.write(encode16bitColor(newColors))

def replace98colors(filename, offset, pad, colormap):

    touchOutFile(filename)

    with open(modName + filename, mode='r+b') as f:
        f.seek(offset + 1)
        length = int.from_bytes(f.read(2), 'big')

        for i in range(0, length):
            f.seek(offset + 4 + i * (2 + pad))
            color16 = f.read(2)
            color = decode16bitColor(color16)

            newColors = []
            if(len(color) == 4):
                newColors.append(color[3])

            f.seek(offset + 4 + i * (2 + pad))
            f.write(encode16bitColor(newColors))
            


    
def writeColors(filename, offsets, cf1, cf2):

    touchOutFile(filename)

    with open(modName + filename, mode='r+b') as f: 
        for offset in offsets:
            f.seek(offset + cf1)
            f.write(bytes(elecColor1))
            f.seek(offset + cf2)
            f.write(bytes(elecColor2))



# CF XX format, color offsets are 2 and 9 
# 07 07 07 format, color offsets are 4 and 8 
# 42 48 format, color offsets are -16 and -12 
# 98 matrix format...

######### Common #########
EfCoDataElectricCFXX = [

    #electric hitlag
    0x1484, #aura 1
    0x1557, #bolt 1
    0x15b0, #spark balls
    0x1498, #aura 2
    0x141c, #bolt 2
    0x13a2, #splat 2
    0x13b8, #splat 2
    0x13ce, #splat 3

    #electric hitstun
    0x1600, #bolts
    0xa1d4, #spark balls

    #other
    0x12a6, #glint effect used everywhere
    0x14ec, #small glint effect, appears upon shine hit
    0x55af, #spacie side b startup
    0x554e, #spacie side b startup
    0x2f0c, #inside of sparkel that appears on mewtwo, ness and pika "psy spark"
    0x102a, #electric bolt on mewtwo up b

    #puff neutral b charging
    0xcdae, #single sparkle 1
    0xcfea, #fading color of sparkle?
    0xce1c, #fading color of sparkle?
    0xce0f, #fading color of sparkle?
    0xce82, #small sparkles
    0xceed, #small sparkles, center color is 0xcfea?


    #magic explosion effect (zelda upair, ness up b, etc)
    0x1cf6, #shimmering sparkles???
    0x1c0e, #beginning color of small depleting sparkles
    0x1c1b, #ending color of small depleting sparkles
    0x1c84, #beginning color of shockwave
    0x1c91, #ending color of shockwave?

    #large shockwave effect (beginning of ness up b, etc)
    0x10017, #beginning color of wave 
    0x10024, #ending color of wave

    #slash hitlag, effect
    0x9776, #streaks coming from hard hit (may be regular hitlag?)
    0x8545, #starting color of small bilboard slash graphic
    0x8552, #ending color of small bilboard slash graphic
    0x860c, #blue energy effects
    0x85b3, #streaks coming from hit    
    0xd874, #spawn lightning second color
    0xd88e, #spawn lightning first color
    0x1382, #a splat

    #regular hitlag
    0xdbc, #splat f1
    0xdd2, #splat f2
    0xde8, #splat f3
    0xe06, #expanding splat f4
    0xea4, #bolt f5
    0xe14, #unsure f6 (splat inside?)
    0xde8, #unsure f6 (splat outside?)

]
EfCoData4248 = [
    #slash hitlag
    #probably special cases, blending mode is probably weird
    #they are "4248" matches number 25 and 26 in efcodata, matches around them are likely of interest too
    0x115b84, #match 26
    0x115ab8 #match 25
]
writeColors(EfCoData, EfCoDataElectricCFXX, 2, 9)
writeColors(EfCoData, EfCoData4248, -16, -12)

######### Fox and Falco #########
EfFxDataCFXX = [
    0x125, #shine sparkles
    0x4a9, #side b trail
]

EfFxData98 = [
    #various frames of shine
    0x1c2a0, #shine                                         primary: 0xab9f boarder: 0x621f
    0x1c8e0, #First Frames of Shine: Inner Hexagon
    0x1c91f, #First Frames of Shine: Outer Hexagon Glow
    0x1c95e, #First Frames of Shine: Outer Hexagon Border

]

shineColorMap = {
    0xab9f:[], # light blue fill of shine 
    0x621f:[], # darker blue boarder of shine
}

for offset in EfFxData98:
    shift98colors(EfFxData, offset, 2, hueShift)


writeColors(EfFxData, EfFxDataCFXX, 2, 9)

######### Falco #########
PlFc4248 = [
    0x1EC58, #falco side b illusion ccolor
]
writeColors(PlFc, PlFc4248, -16, -12)

######### Fox ##########
PlFx4248 = [
    0x2205C, #fox side b illusion color
]
writeColors(PlFx, PlFx4248, -16, -12)

######### Pika & Pichu #########
EfPkDataCFXX = [
    0x166, #Middle of Aerial Neutral B
    0x1CE, #Outer Lens Flare of Aerial Neutral B
    0x236, #Middle Lens Flare of Aerial Neutral B
    0x29E, #Inner Border of Aerial Neutral B
    0x2AB  #Inner Triangles of Aerial Neutral B
]
EfPkData4248 = [
    0x13F24, #Down B Aura, may need some tinkering? its half blue
]
EfPkData070707 = [
    0x148DC, #pikachu Pre Forward Smash Lightning
    0x14C80, #pikachu Half of Forward Smash Aura
    0x14D4C, #pikachu Other Half of Forward Smash Aura
    0x14E0C, #pikachu Forward Smash Ball/Head

    0x17c5c, #pichu bolts during fsmsash anticipation
    0x18000, #pichu bolts at head of fsmash
    0x180cc, #pichu bolts at head of fsmash
    0x1818c, #pichu center of fsmash
]
writeColors(EfPkData, EfPkDataCFXX, 2, 9)
writeColors(EfPkData, EfPkData4248, -16, -12)
writeColors(EfPkData, EfPkData070707, 4, 8)

######## Pikachu ###########
PlPk070707 = [
    0xC354,  #down b bolt
    0x14DFC, #part of ground nautral b
    0x14EC8, #part of ground nautral b
    0x14F94, #part of ground nautral b
    0x15060, #tail of ground nautral b
    0x151EC, #head of ground nautral b
]
PlPk4248 = [
    0x151ac, #grounded projectile aura
    0x1526c, #grounded projectile head (also controlled by another offset???)
]
writeColors(PlPk, PlPk4248, -16, -12)
writeColors(PlPk, PlPk070707, 4, 8)

######## Pichu ##########
PlPc070707 = [
    0xbf14,  #down b bolt
    0x14dac, #part of ground neutral b
    0x14c20, #part of ground neutral b
    0x149bc, #part of ground neutral b
    0x14a88, #part of ground neutral b
    0x14b54, #part of ground neutral b
]

PlPc4248 = [
    0x14e2c, #grounded projectile aura
    0x14d6c, #grounded projectile head (also controlled by another offset???)
]
writeColors(PlPc, PlPc4248, -16, -12)
writeColors(PlPc, PlPc070707, 4, 8)

######## Ness Effect ########
EfNsData070707 = [
    0x16474, #down b ring
    0x16534, #down b ring
    0x165f4, #down b ring
    0x166b4, #down b ring
    # either missing a down b ring or the outter one is messed up???

    0x16774, #down b inner sphere
    0x16834, #down b inner texture
    0x163b4, #down b aura
    0x13270, #up b inital sphere bolt texture
    0x13330, #up b inital sphere bolt texture
    0x14390, #up b contact texture
    0x14210, #up b contact texture
    0x142d0, #up b sphere
    0x13d84, #up b radiating bolt
    0x13fc4, #up b radiating bolt
    0x13f04, #up b radiating bolt
    0x14144, #up b radiating bolt
    0x13e44, #up b radiating bolt
    0x14084, #up b radiating bolt

]
writeColors(EfNsData, EfNsData070707, 4, 8)

######## Ness ###############
PlNs070707 = [
    0x24038, #very tip of the Up B
    0x24034, #Part of the Up B tail
    0x2c3f4, #Part of the Up B tail
    0x2c774, #Part of the Up B tail
    0x2caf4, #Most of the Up B tail
    0x2d3c8, #Part of the Up B Aura
    0x2d528, #Part of the Up B Aura and ball color
    0x2d5e8, #Alternating Lightning around Up B ball
    0x2d6a8, #Alternating Lightning around Up B ball
    0x2d768, #Alternating Lightning around Up B ball
    0x2d828, #Alternating Lightning around Up B ball
]
writeColors(PlNs, PlNs070707, 4, 8)


############## Samus Effect #############
EfSsDataCFXX = [
    0x1dc, #Rays coming out of charge shot
    0x243, #Color of lightning on initial relase of charge shot
    0x2e7, #Main outer color of rays created during charging charge shot
    0x2f4, #Faint rays moving toward charge shot
    0x2fb, #Inner part of rays from 0x2e7
    0x34d, #faint color surrounding samus during charging
    0x366, #Aura around charging
]
EfSsData070707 = [
    0x11584, #Lightning around samus during screw attack
    0x11644, #Lightning around samus during screw attack
    0x11704, #Lightning around samus during screw attack
    0x117c4, #More lightning around up B
    0x120d0, #Inner part of ring around the blaster after charge shot
]
writeColors(EfSsData, EfSsDataCFXX, 2, 9)
writeColors(EfSsData, EfSsData070707, 4, 8)

############ Samus ############
PLSs070707 = [
    0x35b5c, #A ring that circles around charge shot
    0x35c28, #A ring that circles around charge shot
]
writeColors(PlSs, PLSs070707, 4, 8)
shiftPaletteColors(PlSs)



# Not used yet in this script
'''
EfCoDataHitlagCFXX = [
    #standard hit effect
    0xdbc, #splat f1
    0xdd2, #splat f2
    0xde8, #splat f3
    0xe06, #expanding splat f4
    0xea4, #bolt f5
    0xe14, #unsure f6 (splat inside?)
    0xde8, #unsure f6 (splat outside?)
    0xe2f #resulting hitstun cloud (not hitstun trail)
]
'''

print("Done! Created files:")
for f in createdFiles.keys():
    print(f)
        
    

    
