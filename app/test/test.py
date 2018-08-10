import multiprocessing
import time

class A():
    def __init__(self, i):
        super(A, self).__init__()
        self.i = i

    def run(t):
        time.sleep(10-t)
        print(t)
        return t


def main():
    pool = multiprocessing.Pool(processes=10)
    x = lambda t: A.run(t)
    processes = [pool.apply_async(x, [i]) for i in range(10)]
    for p in processes:
        print p.get(timeout=5)
    pass

if __name__ == '__main__':
    main()
