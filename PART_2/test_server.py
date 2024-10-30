
import requests
import threading
import time
import csv


# test on aviary machine
url = 'http://loon.cs.umanitoba.ca:8000/list1.json/1'

# test on my local machine
#url = 'http://localhost:8000/list1.json/1'

def make_request(url):
    response = requests.get(url)

def main():
    threads = []
    time_start = time.time()

    # Make 100 different threads
    for i in range(100):
        
        thread = threading.Thread(target = make_request, args = (url,))
        thread.start()
        threads.append(thread)


    # Run all threads concurrently
    for thread in threads:
        thread.join()

    time_end = time.time()
    print('The time is:', time_end - time_start)

    # with open('./multi_threaded_summary.csv', 'a', newline=''):
    with open('./single_threaded_summary.csv', 'a', newline='') as csv_file:
        csv_write = csv.writer(csv_file)
        csv_write.writerow([time_end-time_start])
    

if __name__ == "__main__":
    main()






