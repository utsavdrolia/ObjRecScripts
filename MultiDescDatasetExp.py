from CompareMatcherExp import run_iters
import smtplib

#dataset_size = [10, 50, 100, 200, 400]
dataset_size = [50]
descriptor_size = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]


if __name__ == '__main__':
    for num_objects in dataset_size:
        print "Running for Dataset size:{}".format(num_objects)
        for num_desc in descriptor_size:
            run_iters(1, 16, num_objects, num_desc)

