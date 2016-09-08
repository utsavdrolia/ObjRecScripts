from ClientServerExp import run_iters

BF_HAM_NN = "1"
BF_HAM_NB = "2"
BF_L2 = "3"
LSH = "4"

ORB = "1"
SIFT = "2"

#dataset_size = [10, 50, 100, 200]#, 400]
nearby_objects_size = [10]
descriptor_size = 800
cache_sizes = [10]

if __name__ == '__main__':
    for num_objects in nearby_objects_size:
        print "Running for Dataset size:{}".format(num_objects)
        for cache_size in cache_sizes:
            run_iters(1, 1, num_objects, descriptor_size, ORB, LSH, LSH, cache_size)
            print("### FINISHED DATASET:{} CACHE:{} ###".format(num_objects, cache_size))

