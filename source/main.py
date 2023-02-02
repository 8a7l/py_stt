import sounddevice as sd
import vosk
import json
import queue
import keyboard
import pyautogui
import time
import win32api
win32api.LoadKeyboardLayout("00000409",1)
#=========================================================================================================================================================

run1=True
run2=False

start_key='+'
pause_key='-'
end_key='*'

n=['`', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', 
'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 
'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', ' ']

n1=["'", 'й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ї', 
'ф', 'і', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'є', 
'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', '.', ' ' ]


info_start='Запущено'
info_pause='Зупинено'

#=========================================================================================================================================================
def on_pause():
    pyautogui.press('backspace')
    global run2
    if run2==True:
        run2=False
        print('['+time.asctime()+']'+' '+info_pause)


def on_start():
    pyautogui.press('backspace')
    global run2
    if run2==False:
        run2=True
        print('['+time.asctime()+']'+' '+info_start)


def on_esc():
    pyautogui.press('backspace')
    global run1
    if run1==True:
        run1=False


def on_press(string):
    data = list(string)
    for i in data:
        for j in n1:
            if i == j:
                pyautogui.press(str(n[n1.index(j)]))

#=========================================================================================================================================================
q = queue.Queue()
model = vosk.Model('vosk_model')
device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def main():
    with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=device[0], dtype='int16', channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while run2:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                data = str(data)
                on_press(data)
                print(data)
#=========================================================================================================================================================


#=========================================================================================================================================================

#=========================================================================================================================================================
        
keyboard.add_hotkey(start_key, on_start)
keyboard.add_hotkey(pause_key, on_pause)
keyboard.add_hotkey(end_key, on_esc)


pyautogui.PAUSE = 0.1

#=========================================================================================================================================================
if __name__ == '__main__':
    while run1:
        while run2:
            main()

#=========================================================================================================================================================



    




