'''
Created on 2012-9-22

@author: jun
'''
if __name__ == '__main__':
    import socket  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect(('localhost', 51888))  
    import time  
    time.sleep(2)  
    sock.send('###run##java#-cp#D:\BaiduCloud\develop\java#Test###')  
    print sock.recv(1024)
    time.sleep(2)  
    sock.send('###run##java#-cp#D:\BaiduCloud\develop\java#Test###')  
    print sock.recv(1024)
    time.sleep(2)
    sock.send('###killall###')
    print sock.recv(1024) 
    time.sleep(2)
    sock.close()  