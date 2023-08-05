import time
from datetime import datetime

class Timer:

    def count_down(s):
        s = int(s)
        for i in range(s):
            print(s - i)
            time.sleep(1)
        print(0)    

    def sleep(s):
        time.sleep(s)
        print(s) 

    def now():
        print(datetime.now())

    def count_function(function):
        time_start = datetime.now()
        function()
        time_end = datetime.now()
        time_used = str(time_end - time_start)
        function_name = function.__name__ 
        print('%s(): %s' % (function_name, time_used))

