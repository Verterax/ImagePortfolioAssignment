# Group: 8-bit Federation (Team 8)	
# Christopher Caldwell	
# Date: 3/16/2018
# VERSION 1.00

import os
import string

""" CODE TO ACCESS WORKING DIRECTORY """
try:
  workingDir = os.path.dirname(os.path.abspath(__file__))
except:
  print "Please select the working directory"
  workingDir = pickAFolder()
  print workingDir
  
# Get Image by filename from SourceMedia directory.
def get_pic(fileName = ""): 
  try:
    path = workingDir + '\\SourceMedia\\' + fileName
    return makePicture(path)
  except:
    return makePicture(pickAFile())
    
def getImg(fileName):
  path = workingDir + '\\SourceMedia\\' + fileName
  print path
  return makePicture(path)
   
# Save an image to the OutputMedia Directory
def saveOutput(img, fileName):
  repaint(img)
  writePictureTo(img, workingDir + "\\OutputMedia\\" + fileName)
  
""" BEGIN PROJECT CODE"""
      
# Rose Colored Glasses
def roseColoredGlasses(pic):
  pixels = getPixels(pic)
  for p in pixels:
    r = getRed(p)
    g = getGreen(p)
    b = getBlue(p)
    setRed(p, r*0.9)
    setGreen(p, g*0.3)
    setBlue(p, b*0.6)
  return pic

# Negative
def makeNegative(img):
  pixels = getPixels(img)
  for p in pixels:
    r = 255 - getRed(p)
    g = 255 - getGreen(p)
    b = 255 - getBlue(p)
    setColor(p, makeColor(r, g, b))
  return img

# Better Black and White
def betterBnW(img):
  pixels = getPixels(img)
  for p in pixels:
    r = getRed(p)
    g = getGreen(p)
    b = getBlue(p)    
    avg = r*0.299 + g*0.587 + b*0.114     
    setRed(p, avg)
    setGreen(p, avg)
    setBlue(p,avg)
  return img

# Bottom-to-Top Mirror
def bottom_to_top(pic):
  pixels = getPixels(pic)
  height = getHeight(pic)
  width = getWidth(pic)
  halfHeight = height/2
  size = width * height - width
  for x in range(0, width):
    for y in range(0, halfHeight):
      pDest = pixels[x + y * width]
      pSource = pixels[size - width * y + x]
      setColor(pDest, getColor(pSource))
  return pic

# Shrink
def shrink(pic):
  shrunkPic = makeEmptyPicture(getWidth(pic)/2, getHeight(pic)/2)
  for x in range(0, getWidth(pic), 2):
    for y in range(0, getHeight(pic), 2):
      setColor(getPixel(shrunkPic, x/2, y/2), getColor(getPixel(pic, x,y)))
  return shrunkPic

# Collage
def lightenUp(pic):
  pixels = getPixels(pic)
  for p in pixels:
    setColor(p, makeLighter(getColor(p)))
  return pic

def right_to_left(pic):
  pixels = getPixels(pic)
  height = getHeight(pic)
  width = getWidth(pic)
  halfWidth = width/2
  for x in range(0, halfWidth):
    for y in range(0, height):
      pDest = pixels[x + y * width]
      pSource = pixels[width - x + width * y - 1]
      setColor(pDest, getColor(pSource))
  return pic

def top_to_bottom(pic):
  pixels = getPixels(pic)
  height = getHeight(pic)
  width = getWidth(pic)
  halfHeight = height/2
  size = width * height - width
  for x in range(0, width):
    for y in range(0, halfHeight):
      pSource = pixels[x + y * width]
      pDest = pixels[size - width * y + x]
      setColor(pDest, getColor(pSource))
  return pic

def noBlue(pic):
  pixels = getPixels(pic)
  for p in pixels:
    setBlue(p, 0)
  return pic

def moreRed(pic, perc2IncBy):
  pixels = getPixels(pic)
  perc2IncBy *= 0.01 # Convert to decimal
  for p in pixels:
    r = getRed(p)
    newVal = r + int(r * perc2IncBy)
    if newVal > 255: # Prevent values higher than 255
      newVal = 255
    elif newVal < 0: # Prevent values lower than 0
      newVal = 0
    setRed(p, newVal)
  return pic

def pyCopy(source, target, targetX, targetY):
  sY = 0  
  for tY in range(targetY, getHeight(source) + targetY): # Write source to target
    sX = 0
    if tY < 0 or tY >= getHeight(target):
      sY +=1
      continue
    for tX in range(targetX, getWidth(source)  + targetX):
      if tX < 0 or tX >= getWidth(target):
        sX += 1
        continue
      setColor(getPixel(target, tX, tY), getColor(getPixel(source, sX, sY)))
      sX +=1
    sY +=1    
  #repaint(target)
  return target


def makeCollage():
  blankPage = makeEmptyPicture(1500,2100)  
  
  pic = getImg("andromeda.jpg")
  pic = makeNegative(pic)
  blankPage = pyCopy(pic, blankPage, -300,0)

  pic = getImg("portrait.jpg")
  pic = betterBnW(pic)
  blankPage = pyCopy(pic, blankPage, 724,0)

  pic = getImg("otter.jpg")
  pic = moreRed(pic, 200)
  blankPage = pyCopy(pic, blankPage, -150,600)
  
  pic = getImg("team.jpg")
  pic = shrink(lightenUp(pic))
  blankPage = pyCopy(pic, blankPage, 450,350)

  pic = getImg("bear.jpg")
  pic = noBlue(pic)
  blankPage = pyCopy(pic, blankPage, 700,700)
  
  pic = getImg("cat.jpg")
  top_to_bottom(pic)
  blankPage = pyCopy(pic, blankPage, -20, 1320)
        
  pic = getImg("vixen.jpg")
  pic = shrink(pic)
  blankPage = pyCopy(pic, blankPage, 500,930)
  
  pic = getImg("nyan.jpg")
  pic = right_to_left(pic)
  blankPage = pyCopy(pic, blankPage, 760,1310)  
  return blankPage

# Red-Eye Reduction
def reduceRedeye(img, x1, y1, x2, y2):
  redEyeColor = makeColor(235, 115, 135)
  yellowEyeColor = makeColor(254, 226, 108)
  eyeGlow = makeColor(180,60,57)
  for x in range(x1, x2):
    for y in range(y1, y2):
      pixel = getPixel(img, x, y)
      color = getColor(pixel)
      if distance(color, redEyeColor) < 70.0:
        setColor(pixel, black)
      if distance(color, yellowEyeColor) < 75.0:
        setColor(pixel, black)
      if distance(color, eyeGlow) < 75.0:
        setColor(pixel, black)
  return img

# Color Artify
def artify(pic):
  for x in range(0, getWidth(pic)):
    for y in range(0, getHeight(pic)):
      p =  getPixel(pic, x, y)
      setRed(p, colorRange(getRed(p)))
      setGreen(p, colorRange(getGreen(p)))
      setBlue(p, colorRange(getBlue(p)))
  return pic
  
def colorRange(color):
  if color < 64:
    return 31
  if color < 128:	
    return 95
  if color < 192:
    return 159
  return 223

# Green Screen
def identifyColor(pixel):
    threshhold = 150
    r = getRed(pixel)
    g = getGreen(pixel)
    b = getBlue(pixel)
    if abs(r - b) < 25 and abs(g - b) > threshhold and abs(g - r) > threshhold:
      return "green"
    elif abs(g - b) < 25 and abs(r - b) > threshhold and abs(r - g) > threshhold:
      return "red"
    else:
      return "blue"

def colorPaste(source, target, targetX, targetY, colorToIgnore):
  sY = 0  
  for tY in range(targetY, getHeight(source) + targetY): # Write source to target
    sX = 0
    if tY < 0 or tY >= getHeight(target):
      sY +=1
      continue
    for tX in range(targetX, getWidth(source)  + targetX):
      if tX < 0 or tX >= getWidth(target):
        sX += 1
        continue
      pixel = getPixel(source, sX, sY)
      if colorToIgnore != identifyColor(pixel):
        setColor(getPixel(target, tX, tY), getColor(pixel))
      sX +=1
    sY +=1    
  return target
  
# Home made St. Patrick's Day
def makeCard():
  color = "red"
  base = getImg("rainbowgold.jpg")
  sprite = getImg("banner.jpg")
  base = colorPaste(sprite, base, 480, 225, color)
  sprite = getImg("patrick.jpg")
  base = colorPaste(sprite, base, 150, 673, color)
  sprite = getImg("hat.jpg")
  base = colorPaste(sprite, base, 290, 590, color)
  sprite = getImg("from.jpg")
  base = colorPaste(sprite, base, 758, 520, color)
  sprite = getImg("logo.jpg")
  base = colorPaste(sprite, base, 674, 681, color)
  sprite = getImg("clover.jpg")
  base = colorPaste(sprite, base, 98, 65, color)
  base = colorPaste(sprite, base, 1797, 56, color)
  base = colorPaste(sprite, base, 59, 433, color)
  base = colorPaste(sprite, base, 594, 43, color)
  return base
  
# Advanced Image Processing
def lineDrawing(pic):
  thresh = 7
  pic = betterBnW(pic)
  for x in range(0, getWidth(pic)-1):
    for y in range(0, getHeight(pic)-1):
      currPix = getPixel(pic, x , y)
      currLum =  getRed(currPix)
      rightLum = getRed(getPixel(pic, x + 1, y))
      bottomLum = getRed(getPixel(pic, x, y + 1))
      diff = abs(currLum - rightLum) + abs(currLum - bottomLum)
      if diff > thresh:
        setColor(currPix, black)
      else:
        setColor(currPix, white)
  return pic


""" TEST CODE SECTION """
# Color Artify
pic = getImg("cat.jpg")
pic = artify(pic)
repaint(pic)
saveOutput(pic, "artify.jpg")


# Rose Colored Glasses
pic = getImg("bear.jpg")
pic = roseColoredGlasses(pic)
repaint(pic)
saveOutput(pic, "Rose-colored glasses.jpg")

# Negative
pic = getImg("andromeda.jpg")
pic = makeNegative(pic)
repaint(pic)
saveOutput(pic, "negative.jpg")

# Better Black and White
pic = getImg("otter.jpg")
pic = betterBnW(pic)
repaint(pic)
saveOutput(pic, "betterBnW.jpg")

# Bottom-to-Top Mirror
pic = getImg("nyan.jpg")
pic = bottom_to_top(pic)
repaint(pic)
saveOutput(pic, "bottom-to-top.jpg")

# Shrink
pic = getImg("vixen.jpg")
pic = shrink(pic)
repaint(pic)
saveOutput(pic, "shrink.jpg")

# Collage
pic = makeCollage()
repaint(pic)
saveOutput(pic, "collage.jpg")

# Red-Eye Reduction
pic = getImg("rabbit.jpg")
pic = reduceRedeye(pic, 717, 216, 1071, 539) 
repaint(pic)
saveOutput(pic, "redeyeReduction.jpg")

# Color Artify
pic = getImg("cat.jpg")
pic = artify(pic)
repaint(pic)
saveOutput(pic, "artify.jpg")

# Green Screen
desert = getImg("desert.jpg")
snowman = getImg("snowman.jpg")
snowmanInDesert = colorPaste(snowman, desert, 509, 450, "green")
saveOutput(snowmanInDesert, "greenScreen.jpg")
repaint(snowmanInDesert)

# Home made St. Patrick's Day
card = makeCard()
saveOutput(card, "stPatricksDayCard.jpg")
repaint(card)

# Line Drawing
pic = getImg("portrait.jpg")
pic = lineDrawing(pic)
repaint(pic)
saveOutput(pic, "lineDrawing.jpg")
 