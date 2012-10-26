'''
@author: jun
'''
import socket  
import time  

if __name__ == '__main__':
    t = input("1:test agent, 2:test controler:\n")
    print("Hello,", t)
    if t == 1:    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        sock.connect(('localhost', 51888))  
        time.sleep(2)  
        sock.send('run##java#-cp#D:\BaiduCloud\develop\java#Test\n')  
        print sock.recv(1024)
        time.sleep(2)  
        sock.send('run##java#-cp#D:\BaiduCloud\develop\java#Test\n')  
        print sock.recv(1024)
        time.sleep(2)
        sock.send('killall\n')
        print sock.recv(1024) 
        time.sleep(2)
        sock.close()
    elif t == 2:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        sock.connect(('localhost', 51999))  
        time.sleep(2)  
        sock.send("{'Type':'ResponseTime','Time':0,'Value':[{'v0':0.8,'v1':1.16},{'v0':0.98,'v1':3.74}]}\n")  
        print sock.recv(1024)
        time.sleep(2)  
        sock.send('Test Services 2\n')  
        print sock.recv(1024)
        time.sleep(2)
        sock.send('Test Services 3\n')
        print sock.recv(1024) 
        time.sleep(2)
        sock.send('Test Services 4\nTest Services 5\nTest Services 6\nTest ')
        print sock.recv(1024) 
        time.sleep(2)
        sock.send('Services 7\n')
        print sock.recv(1024) 
        time.sleep(2)
        sock.close()  