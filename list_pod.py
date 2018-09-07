#!/usr/bin/python
#-*- coding: utf-8 -*-

from kubernetes import client, config
from kubernetes.client.apis import core_v1_api
from kubernetes.stream import stream
import threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()


v1 = client.CoreV1Api()



def Get_Pods(namespace, svc_id):
    ret = v1.list_namespaced_pod(namespace)
    return [ i.metadata.name   for i in ret.items if i.metadata.labels["svc_id"] == svc_id ]

def doCommand(lock, thread_resps, namespace, name, command):
    exec_command = [
            "/bin/sh",
            "-c",
            command]
    api = core_v1_api.CoreV1Api()
    ret =  api.read_namespaced_pod(name=name,
            namespace=namespace)
    resp = stream(api.connect_get_namespaced_pod_exec, name, namespace,
            command=exec_command,
            container=ret.spec.containers[0].name,
            stderr=True, stdin=False,
            stdout=True, tty=False)
    lock.acquire()
    thread_resps.append(namespace + "/" + name + ":\n")
    thread_resps.append(resp)
    lock.release()

def doBatchCommand(namespace, svc_id, command):
    thread_list = []
    thread_resps = []
    lock = threading.Lock()
    for pod in Get_Pods(namespace, svc_id):
        #doCommand(namespace, pod, command)
        t = threading.Thread(target=doCommand, args=(lock, thread_resps, namespace,pod, command))
        thread_list.append(t)
        t.start()


    for i in thread_list:
        i.join()

    return ''.join(thread_resps)

    


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/text/plain')
        self.end_headers()

    def do_GET(self):
        
        self._set_headers()
        req = self.requestline.split()[1]
        parsed = urlparse.urlparse(req)
        params = urlparse.parse_qs(parsed.query)

        if 'namespace' in params.keys():

            namespace = params['namespace']
            svc_id = params['svc_id']
            commands = params['commands']
            if len(namespace) == 0:
                return
            print "doBatchCommand(" , namespace[0] ,  svc_id[0] ,  commands[0] , ")"
            ret = doBatchCommand(namespace[0], svc_id[0], commands[0])
            self.wfile.write(ret)
        

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

doBatchCommand("yellowpage", "yellowpage-data", "ls")
server_address = ('', 8888)
httpd = HTTPServer(server_address, S)
httpd.serve_forever()
