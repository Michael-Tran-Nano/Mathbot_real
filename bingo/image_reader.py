import pyautogui

# x, y, dx, dy = pyautogui.locateOnScreen('tile.png')
# im = pyautogui.screenshot(region=(x+2, y+1, dx-4, dy+40))
# im.save('test.png')

for i, pos in enumerate(pyautogui.locateAllOnScreen('tile.png'), 35):
    x, y, dx, dy = pos
    im = pyautogui.screenshot(region=(x+2, y+1, dx-4, dy+40))
    im.save(f"{i}.png")
    print(f'{i}.png saved')
