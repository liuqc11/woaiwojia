from multiprocessing import Pool
import os

def genetic_one(index):
  sys_str='nohup python genetic.py 2000 0.6 0.6 1000 2>&1 > .nohup.out%02d &'%index
  os.system(sys_str)

if __name__ == '__main__':
    pool = Pool(processes=10)
    num = 10
    result = pool.map(genetic_one, range(num))
    print 'before close'
    pool.close()
    print 'before join'
    pool.join()
    print 'before exit'
