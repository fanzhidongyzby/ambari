#!/bin/bash
import BaseHTTPServer
from SocketServer import ThreadingMixIn
import threading
import sys

mutex = threading.Lock()
# all registered topics
topic_list = []


class TopicRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        """handle POST request"""
        length = self.headers.getheader('content-length')
        data_bytes = int(length)
        # topic name to register
        data = self.rfile.read(data_bytes)

        data = data.split('=')
        option = data[0]

        return_code = 200
        if option == "add_topic":
            return_message = self.add_topic(data[1])
        elif option == "rm_topic":
            return_message = self.remove_topic(data[1])
        elif option == "reset":
            return_message = self.reset_topic()
        else:
            return_message = "there is not {0} option for topic".format(option)
            return_code = 404

        self.log_message("all topics: {0}".format(topic_list))
        self.send_response(return_code)
        self.end_headers()
        self.wfile.write(return_message)

    def do_GET(self):
        """handle GET request"""
        self.send_response(200)
        self.end_headers()
        self.wfile.write(topic_list)

    def add_topic(self, new_topic):
        """add new topic"""
        if mutex.acquire():
            # topic name must different
            if new_topic in topic_list:
                message = "{0} topic has already existed\n".format(new_topic)
            else:
                topic_list.append(new_topic)
                message = "{0} topic registered succeeded\n".format(new_topic)
            mutex.release()

        return message

    def remove_topic(self, topic_name):
        """remove a topic"""
        if mutex.acquire():
            try:
                topic_list.remove(topic_name)
                message = "{0} topic removed succeeded\n".format(topic_name)
            except ValueError:
                message = "{0} topic did not exist\n".format(topic_name)
            mutex.release()
        return message

    def reset_topic(self):
        """reset tube cluster, clear all topics"""
        if mutex.acquire():
                del topic_list[:]
                message = "clear all topics succeeded\n"
        mutex.release()
        return message


class ThreadingHttpServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ("usage :{0}  HOST_IP  PORT".format(sys.argv[0]))
        sys.exit(1)
    HOST_IP = sys.argv[1]
    PORT = int(sys.argv[2])
    server = ThreadingHttpServer((HOST_IP, PORT), TopicRequestHandler)
    # Start a thread with the server
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.setDaemon(True)
    server_thread.start()
    print ("topic tools server started\nhost ip:{0}\tport:{1}".format(HOST_IP, PORT))
    while True:
        pass