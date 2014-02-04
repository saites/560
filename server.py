from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from sys import argv
from socket import gethostname
ACCOUNT_FILE = "accounts.txt"

def deposit(acnt, amt): 
    return change_val(acnt, amt)

def withdraw(acnt, amt):
    return change_val(acnt, -1*amt)

def inquire(acnt):
    accnts = get_accounts()
    try:
        amt = accnts[acnt]
        return amt
    except KeyError:
        return None

def transfer(acnt1, acnt2, amt):
    accnts = get_accounts()
    try:
        accnts[acnt1] -= amt
    except KeyError:
        return (False, False)
    try:
        accnts[acnt2] += amt
    except KeyError:
        return(True, False)
    write_accounts(accnts)
    return True, True

def change_val(acnt, amt):
    accnts = get_accounts()
    try:
        accnts[acnt] += amt
        write_accounts(accnts)
        return True
    except(KeyError):
        return False

def get_accounts():
    accnts = {}
    try:
        f = open(ACCOUNT_FILE, 'r')
        for line in f:
            vals = line.rstrip().partition(',')
            accnts[int(vals[0])] = int(vals[2])
        f.close()
    except IOError:
        print("unable to open {}".format(ACCOUNT_FILE))
    return accnts
    
def write_accounts(accnts):
    try:
        f = open(ACCOUNT_FILE, 'w')
        for (key,val) in accnts.iteritems():
            f.write("{},{}\n".format(key,val))
        f.close()
    except IOError:
        print("unable to open {}".format(ACCOUNT_FILE))
        
def main():
    try:
        if len(argv) != 2:
            raise IndexError()
        port_num = int(argv[1])
    except IndexError:
        print("use: python server.py port_num")
        exit()
        
    try:    
        server = SimpleXMLRPCServer(
            (gethostname()+".eecs.utk.edu", port_num),
            allow_none=True)
    except:
        print("unable to create server")
        exit()
        
    server.register_introspection_functions()
    server.register_function(deposit)
    server.register_function(withdraw)
    server.register_function(inquire)
    server.register_function(transfer)
    server.serve_forever()
    
main()
