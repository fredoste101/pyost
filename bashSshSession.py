import pexpect
from random import choice as randomChoice 
import string


class BashSSHSession:
    def __init__(self):
        self.ip             = ""
        self.user           = ""
        self.password       = ""
        self.prompt         = ""
        self.newLineString  = "\r\n"


    def start(self):
        self.ssh = pexpect.spawn("ssh " + self.user + "@" + self.ip)

        self.ssh.expect("password:")

        self.ssh.sendline(self.password)

        self.createRandomPrompt()


    def createRandomPrompt(self):
        pool = string.letters + string.digits

        self.prompt = "".join(randomChoice(pool) for i in xrange(40)) + ":" 
        
        self.ssh.sendline("PS1=" + self.prompt)
    
        self.ssh.expect("\r\n" + self.prompt)


    def executeCommand(self, command):
        self.ssh.sendline(command)

        self.ssh.expect(self.prompt)        

        output = self.getCommandOutput() 

        returnStatus = self.getCommandStatus()

        return (output, returnStatus)


    def getCommandOutput(self):
        outputList = self.ssh.before.split(self.newLineString)

        output = ""

        if len(outputList) > 2:
            output = "\n".join(outputList[1:-1])

        return output


    def getCommandStatus(self):
        self.ssh.sendline("echo $?")

        self.ssh.expect(self.prompt)

        output = self.getCommandOutput()
    
        retstat = False

        if output == "0":
            retstat = True

        return retstat 
        

if __name__ == "__main__":
    print("no thanks") 
