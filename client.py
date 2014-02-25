import xmlrpclib
import httplib
import sys
import socket

def deposit(acnt, amt):
    global server
    if amt <= 0:
        print("Amount should be positive")
    elif server.deposit(acnt, amt):
        print("Successfully deposit ${} to account {}!".format(amt, acnt))
    else:
        print("No such user or account, {}!".format(acnt))

def withdraw(acnt, amt):
    global server
    if amt <= 0:
        print("Amount should be positive")
    elif server.withdraw(acnt, amt):
        print("Successfully withdraw ${} from account {}!".format(amt,acnt))
    else:
        print("No such user or account, {}!".format(acnt))
    
def inquire(acnt):
    global server
    amt = server.inquire(acnt)
    if amt is not None:
        print("The current balance of user {} is ${}".format(acnt, amt))
    else:
        print("No such user or account, {}!".format(acnt))
        
def transfer(acnt1, acnt2, amt):
    global server
    if amt < 0:
        print("Amount should be positive")
        return
    ans = server.transfer(acnt1, acnt2, amt)
    if ans[0] is False:
        print("No such user or account, {}!".format(acnt1))
    elif ans[1] is False: 
        print("No such user or account, {}!".format(acnt2))
    else:
        print("Successfully transferred ${} from {} to {}!"
            .format(amt, acnt1, acnt2))
        
def parsecmd(cmd):
    if len(cmd) == 2 and cmd[0] == 'inquire':
        inquire(int(cmd[1]))
    elif len(cmd) == 3 and cmd[0] == 'deposit':
        deposit(int(cmd[1]), int(cmd[2]))
    elif len(cmd) == 3 and cmd[0] == 'withdraw':
        withdraw(int(cmd[1]), int(cmd[2]))
    elif len(cmd) == 4 and cmd[0] == 'transfer':
        transfer(int(cmd[1]), int(cmd[2]), int(cmd[3]))
    else:
        return False
    return True
        
def parsefile(file):
    try:
        f = open(file, 'r')
        for line in f:
            cmd = line.rstrip().split(' ')
            if not parsecmd(cmd):
                print("unknown command '{}'".format(" ".join(cmd)))
    except socket.timeout:
        raise
    except IOError as e:
        print("unable to open '{}'".format(file))

class TimeoutTransport(xmlrpclib.Transport):
    timeout = 10.0
    def set_timeout(self, timeout):
        self.timeout = timeout
    def make_connection(self, host):
        h = httplib.HTTPConnection(host, timeout=self.timeout)
        return h      

class ServerConnection():
    def __init__(self, address_port):
        (self.address, self.port_num) = address_port.split(':')
        self.server = xmlrpclib.ServerProxy(
            'http://'+self.address+':'+self.port_num,
            transport=TimeoutTransport())
        
def main():
    global server
    try:
        server = ServerConnection(sys.argv[1]).server
        if len(sys.argv) == 3:
            parsefile(sys.argv[2])
        elif not parsecmd(sys.argv[2:]):
            raise IndexError()
    except (IndexError, ValueError) as e:
        print("use: python client.py server:port [cmd acnt(s) amt(s) | file]")
        print("     where cmd is [deposit | withdraw | inquire | transfer]")
        print("")
        print("     examples:")
        print("       deposit 1000 100")
        print("       withdraw 1000 100")
        print("       inquire 1000")
        print("       transfer 1000 1001 100 (from 1000 to 1001)")
    except socket.error as e:
        print e
        print("Unable to establish connection. Try checking the port number")
    except (xmlrpclib.Fault, xmlrpclib.ProtocolError) as e:
        print e
        print("Unable to establish connection. Try checking the server address")
        print("or network connection")
    except Exception as e:
        print("Unknown error: ", e)
        
if __name__ == '__main__':
    main()
