# from memory_profiler import profile
import time
import random
import bisect
from array import array

# @profile
# def main():

# Create an int array, and a list.
rand = [i for i in range(10**5)]
random.shuffle(rand)

lst = rand
arr = array("i", lst)

start_array = time.time()
# Version 1: loop over array.
for i in range(10**5):
    idx = arr.remove(i)

end_array = start_list = time.time()
# Version 2: loop over list.
for i in range(10**5):
    idx = lst.remove(i)

end_list = time.time()

print("array:" + str(end_array-start_array))
print("list:" + str(end_list-start_list))

# if __name__ == '__main__':
#     main()