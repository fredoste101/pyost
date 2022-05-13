import pexpect
from random import choice as randomChoice 
import string


class BashSSHSession:
    """
        Class for creating a ssh-session to a server using bash-shell.
        Commands for sending bash-commands, and hadling their output.
    """

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
        """
            Create a random prompt to match against in other commands.
            This is to see when output from a command has reached its end.
        """

        pool = string.letters + string.digits

        self.prompt = "".join(randomChoice(pool) for i in xrange(40)) + ":" 
        
        self.ssh.sendline("PS1=" + self.prompt)
    
        self.ssh.expect("\r\n" + self.prompt)


    def executeCommand(self, command):
        """
            Execute given command (string).
            Returns the output as well as the return status of the command (0 - True, other - False)
            in a tuple!
        """

        self.ssh.sendline(command)

        self.ssh.expect(self.prompt)        

        output = self.__getCommandOutput() 

        returnStatus = self.__getCommandStatus()

        return (output, returnStatus)


    def __getCommandOutput(self):
        outputList = self.ssh.before.split(self.newLineString)

        output = ""

        if len(outputList) > 2:
            output = "\n".join(outputList[1:-1])

        return output


    def __getCommandStatus(self):
        """
            Returns True if command returned with status 0.
            Returns False otherwise.
        """
        self.ssh.sendline("echo $?")

        self.ssh.expect(self.prompt)

        output = self.__getCommandOutput()
    
        retstat = False

        if output == "0":
            retstat = True

        return retstat 
        

if __name__ == "__main__":
    print("no thanks") 
