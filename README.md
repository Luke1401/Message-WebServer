# PART 1
- For part 1, I have 1 python file named msg_server, 5 json test files and 2 html test files
- To run the server, you need to run this command on the terminal (or command prompt): 
# python3 msg_server.py <PORT_NUMBER> <-m> (for multi-threaded)

* Test:
While the server is running on terminal, you can test the server by several ways

1. Go to any web browser and testing with the several links:
- http://HOST_NAME:PORT_NUMBER/ -> should return an html web page with all the links go to message board
- http://HOST_NAME:PORT_NUMBER/list1.json/ -> should return a json board file with full of messages from this board
- http://HOST_NAME:PORT_NUMBER/list1.json/1 -> should return a single json message at the given index from json board file: list1.json
- http://HOST_NAME:PORT_NUMBER/html_test.html/ -> should return an html board file with with full of messages from this board
- http://HOST_NAME:PORT_NUMBER/html_test.html/1 -> should return an html single message at the given index from html board file: html_test.html

- http://HOST_NAME:PORT_NUMBER/list1.json/4 -> should return 'Message not found', you can try with '1', '2' or '3'
- http://HOST_NAME:PORT_NUMBER/hello.json/ -> should return 'Board not found', you can try with 'list2.json', 'list3.json', 'list4.json'. 'list5.json' or 'html_test.html'


* Note: 
- for the Content-Type request path, I choose to specify the "file extension" in the URL of GET request (.json or .html)
- HOST_NAME could be localhost or name@cs.umanitoba.ca if you run the server on aviary machine

2. Use the command curl:
- curl --get http://<host>:<port>/ -> return an html file with link to all message board
- curl --get http://<host>:<port>/list1.json/ -> return a json file with all messages
- curl --get http://<host>:<port>/list1.json/1 -> return a json single message at the given index
- curl --get http://<host>:<port>/html_test.html/ -> return an html file with all messages
- curl --get http://<host>:<port>/html_test.html/1 -> return an html single message at the given index

- curl -d '{"key1":"foo", "key2":"bar"}' -H "Content-Type: application/json" http://<host>:<port>/test-data-board.json/ -> create new file test-data-board.json which include json message: '{"key1":"foo", "key2":"bar"}' and add new link into board.html which redirect to test-data-board.json

- curl -d '<h2>hello world!</h2>' -H "Content-Type: text/html" http://<host>:<port>/test-data-board.html/ -> create new file test-data-board.html which include  message: 'hello world' and add new link into board.html which redirect to test-data-board.html


# PART 2
- For part 2, I have 2 python files named test_server.py and run_test.py
- For test_server.py, I did make a request to the hyper link to request data from the server and collect the time for each run time and load into the excel file. 
- For run_test.py, I did allow to run the test_server.py 1000 time to collect time data.
- To test part 2, you just need to run the server first as the above instruction and run the file run_test.py and wait for it to generate 1000 collected time data and load it into .csv file.
# python3 run_test.py
