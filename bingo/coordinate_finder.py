import pyautogui

# x, y, dx, dy = pyautogui.locateOnScreen('tile.png')
# im = pyautogui.screenshot(region=(x+2, y+1, dx-4, dy+40))
# im.save('test.png')

# Find images and number them
coor_str = ''
for pos in pyautogui.locateAll("box.png", "Bingoplate_november_2.png"):
    x, y, dx, dy = pos
    coor_str += f"({x+18}, {y+18}), "

print(coor_str)
