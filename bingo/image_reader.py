import pyautogui

# x, y, dx, dy = pyautogui.locateOnScreen('tile.png')
# im = pyautogui.screenshot(region=(x+2, y+1, dx-4, dy+40))
# im.save('test.png')

# Find images and number them
for i, pos in enumerate(pyautogui.locateAllOnScreen('tile.png', confidence=0.96), 22):
    x, y, dx, dy = pos
    im = pyautogui.screenshot(region=(x+2, y+1, dx-4, dy+40))
    im.save(f"{i}.png")
    print(f'{i}.png saved')
