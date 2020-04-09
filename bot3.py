#! python3
import pyautogui, sys, time

def seq_retangular():
	distance = 50
	while distance > 0:
	    pyautogui.drag(distance, 0, duration=0.5)   # move right
	    distance -= 5
	    pyautogui.drag(0, distance, duration=0.5)   # move down
	    pyautogui.drag(-distance, 0, duration=0.5)  # move left
	    distance -= 5
	    pyautogui.drag(0, -distance, duration=0.5)  # move up

def pos_mouse():
	print('Press Ctrl-C to quit.')
	try:
	    while True:
	        x, y = pyautogui.position()
	        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
	        print(positionStr, end='')
	        print('\b' * len(positionStr), end='', flush=True)
	except KeyboardInterrupt:
	    print('\n')

def escrita():
	time.sleep(3)
	pyautogui.write('Hello world!', interval=0.25)
	pyautogui.press('enter')


def screen():
	im2 = pyautogui.screenshot('my_screenshot.png')

def fast_write():
	tempo = 0.3
	time.sleep(3)
	for i in range(1,60):
		pyautogui.write('palavra'+str(i))
		pyautogui.press('enter')
		time.sleep(tempo)


def tesDraw():
	time.sleep(2)
	pyautogui.drag(200, 0, duration=1)   # move right

# seq_retangular()
pos_mouse()
# escrita()
# screen()
# fast_write()
# tesDraw()
