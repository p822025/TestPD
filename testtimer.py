import time
import threading
def fun_timer():
    print("exec timer!!")
    global timer
    timer = threading.Timer(5.5, fun_timer)
    timer.start()

timer = threading.Timer(1, fun_timer)
timer.start()

time.sleep(15) # 15秒后停止定时器
timer.cancel()