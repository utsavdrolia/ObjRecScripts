from DescDatasetExp import run_iters

BF_HAM_NN = "1"
BF_HAM_NB = "2"
BF_L2 = "3"
LSH = "4"

ORB = "1"
SIFT = "2"

#dataset_size = [10, 50, 100, 200]#, 400]
dataset_size = [20]
#descriptor_size = [100, 200, 400, 600, 800, 1000]
descriptor_size = [800]#, 50, 100, 150]


if __name__ == '__main__':
    for num_objects in dataset_size:
        print "Running for Dataset size:{}".format(num_objects)
        for num_desc in descriptor_size:
            run_iters(1, 2, num_objects, num_desc, BF_HAM_NB, ORB)
            print("### FINISHED DATASET:{} DESCRIPTOR:{} ###".format(num_objects, num_desc))

