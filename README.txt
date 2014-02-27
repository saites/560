------------------------------------
RPC Bank Client and Server
------------------------------------
Alexander Saites
Cris Capdevila

------------------------------------
Files
------------------------------------
README.txt      this file
accounts.txt    the accounts "database"
client.py       the client program
cmds.txt        a list of commands to test client
correcttext.txt the correct output from cmds.txt
design.txt		a document explaining relevant design choices
server.py       the server program
test.py         a program that will test the client/server


------------------------------------
Installation and Execution
------------------------------------
These simple python scipts require no installation or building, but rely on
python 2.7. To run them, simply call the scripts using python and provide the
programs with the correct input, as defined below.


------------------------------------
Server
------------------------------------
Start the server on a UTK EECS machine (the program will automatically get the
hostname and will append '.eecs.utk.edu') with the following command:

    >> python server.py 6666

This will start the server on port 6666; the server will run forever, so to 
shut it down, you must kill the process directly (either Ctrl+c or kill).


------------------------------------
Client
------------------------------------
Run the client program from any internet-connected PC, providing the hostname
and port on which you started the server. The following command executes a list 
of commands provided in an external file:

    >> python client.py hydra17.eecs.utk.edu:6666 cmds.txt

Several commands are available:
    inquire 1000
        returns the balance of account 1000
    deposit 1001 100
        deposits $100 in account 1000
    withdraw 1001 100
        withdraws $100 from account 1000
    transfer 1001 1002 $100
        transfers $100 from account 1001 to account 1002
    cmds.txt
        executes commands in cmds.txt; if a command fails, it is skipped, and
        execution continues at the next command. This process is not
        transactional (i.e., if some command will fail, other commands are
        still fully executed, and the state may be different after the commands
        are executed, dispite these failures).


------------------------------------
Testing
------------------------------------
There are two ways to test this program. The first and simplist way is to start
the server on hydra17, port 6666, then run the test program using:

    >> python test.py

If all tests passed, then a nice message will print. If a test fails, then the
program will report the line on which the tests failed along with the failed
assertion. The program also executes the client program using cmds.txt and
compares the output to "correcttext.txt". If they differ, it will report the
issue and print the diff.

You can also test the client program directly the same way the above program
does. This will cover fewer cases, but nevertheless does a decent job of
testing. To do so, simply run:
    
    >> python client.py hydra17.eecs.utk.edu:6666 > output.txt
    >> diff output.txt correcttext.txt

If the files differ, then there is a problem.

Note that if the server is not running, the test program will correctly fail,
namely by reporting the exception and stack trace caused by the socket error.
