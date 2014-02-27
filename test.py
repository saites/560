from client import *
import tempfile, sys
from random import randint

# check server connection
s = ServerConnection('hydra17.eecs.utk.edu:6666')
assert(s.port_num == '6666')
assert(s.address == 'hydra17.eecs.utk.edu')

# check the expected values in the table
# note that th== fails if inquire itself fails (that's a good thing)
for i in range(9):
    assert(s.server.inquire(1000+i) == (i+1)*1000)
assert(s.server.inquire(1010) == 0)

# now test inquire for a false value
assert(s.server.inquire(37) == None)

# check deposit and withdraw
for i in range(9):
    amt = randint(1,100)
    assert(s.server.deposit(1000+i,amt) == True)
    assert(s.server.inquire(1000+i) == (i+1)*1000+amt)
    assert(s.server.withdraw(1000+i,amt) == True)
    assert(s.server.inquire(1000+i) == ((i+1)*1000))

# check transfer
amt = randint(1,100)
amt1001 = s.server.inquire(1001)
amt1002 = s.server.inquire(1002)
print s.server.transfer(1001, 1002, amt)
assert(s.server.transfer(1001, 1002, amt) == (True, True))
assert(s.server.inquire(1001) + amt == amt1001)
assert(s.server.inquire(1002) - amt == amt1002)
assert(s.server.transfer(1002, 1001, amt) == (True, True))
assert(s.server.inquire(1001) == amt1001)
assert(s.server.inquire(1002) == amt1002)
assert(s.server.transfer(1001, 37, amt) == (True, False))
assert(s.server.transfer(37, 1001, amt) == (False, False))

# check client functions
cmdoutput = tempfile.NamedTemporaryFile()
diffoutput = tempfile.NamedTemporaryFile()
cmd = 'python client.py cmds.txt'
# th== cmd will halt if it fails:
subprocess.check_call(cmd.split(' '), stdout=cmdoutput)
subprocess.check_call('diff',  'correcttext.txt', cmdoutput.name, 
    stdout=diffoutput)
if os.stat(diffoutput).st_size != 0:
    print "diff output is different:"
    with open(cmdoutput.name) as f:
        for line in f:
            print line
