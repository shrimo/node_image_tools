import time

class Decorators():

    def __init__(self):
        return

    @staticmethod
    def timer(f):
        def tmp(*args, **kwargs):
            t = time.time()
            res = f(*args, **kwargs)
            print "Function '%s' Run-Time: %f" % ( f.__name__, time.time()-t )
            return res

        return tmp

