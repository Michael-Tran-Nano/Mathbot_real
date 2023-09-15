from PIL import Image
import pyautogui

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
canvas = Image.open("birthday_bingo.png").convert("RGB")
positions = []

for i, pos in enumerate(pyautogui.locateAll("tile.png", "birthday_bingo.png")):
    x, y, dx, dy = pos
    tile = Image.open(f"{numbers[i]}.png")
    positions.append((x+2, y+1))
    canvas.paste(tile, (x+2, y+1))

print(positions)
tile.close()
canvas.show()
canvas.save('test.png')
canvas.close()

# img1 = Image.open("canvas.png")
# img2 = Image.open("1.png")
  
# # No transparency mask specified, 
# # simulating an raster overlay
# img1.paste(img2, (0,0))


  
# for i, pos in enumerate(pyautogui.locateAllOnScreen('tile.png'), 22):
#     x, y, dx, dy = pos
#     im = pyautogui.screenshot(region=(x+2, y+1, dx-4, dy+40))
#     im.save(f"{i}.png")
