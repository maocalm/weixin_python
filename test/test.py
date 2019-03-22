def yield_test(n):

    for i  in range(n) :
        print("hanhanhan")
        yield call(i)
        print("yiele behind")



def call(i):
    print("yield value  ....>>>>>>>", i)


def for_test(n):
    for i in yield_test(n):
        print("正常for循环 >>>>>")
    # print(yield_test(10))


if __name__ == '__main__':
    yield_test(10)

    for_test(10)
