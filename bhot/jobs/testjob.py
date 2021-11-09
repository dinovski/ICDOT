from bhot.jobs import rq
from time import sleep


@rq.job
def testjob():
    for x in range(10):
        print("Round",x)
        sleep(1)
    return 1
