import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0,2,3'

for i in range(100):
    print(i)
