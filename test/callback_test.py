import  time


def callback():
    print("这是一个callback函数")


def test_callback(callbackcallaaa):
    print("这是在test_callback中哦")
    #模拟延时效果
    time.sleep(1)
    print("开始调用callback函数")
    time.sleep(1)
    #开始回调
    callbackcallaaa()
    print("调用完成")

test_callback(callback)