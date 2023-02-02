import pexpect
from random import choice as randomChoice 
import string

from ..verboser.verboser import Verboser


class BashSSHSession:
    """
        Class for creating a ssh-session to a server using bash-shell.
        Commands for sending bash-commands, and handling their output.
    """

    def __init__(self):
        self.ip             = ""
        self.user           = ""
        self.password       = ""
        self.__prompt       = ""
        self.newLineString  = "\r\n"

        self.__commandStatusList = []
        self.__commandOutputList = []

        self.ssh = None


    def start(self):
        """
            Starts a ssh session to a remote host using ip, user, and password.
        """
        
        Verboser.debug("BEGIN: start", "BashSSHSession")

        self.ssh = pexpect.spawn("ssh " + self.user + "@" + self.ip)

        self.ssh.expect("password:")

        self.ssh.sendline(self.password)

        #TODO: wait some time, and then check if password was ok.

        self.__createRandomPrompt()

        Verboser.debug("END: start", "BashSSHSession")


    def __createRandomPrompt(self):
        """
            Create a random prompt to match against in other commands.
            This is to see when output from a command has reached its end.
        """

        Verboser.debug("BEGIN: __createRandomPrompt", "BashSSHSession")

        pool = string.ascii_letters + string.digits

        self.__prompt = "".join(randomChoice(pool) for i in range(40)) + ":" 
        
        Verboser.debug("prompt: " + self.__prompt, "BashSSHSession")

        self.ssh.sendline("PS1=" + self.__prompt)
    
        self.ssh.expect(self.newLineString + self.__prompt)

        Verboser.debug("END: __createRandomPrompt", "BashSSHSession")


    def executeCommand(self, command):
        """
            Execute given command (string).
            Returns the output as well as the return status of the command (0 - True, other - False)
            in a tuple (output, status)
        """

        Verboser.debug("BEGIN: executeCommand. command=" + str(command), "BashSSHSession")

        self.ssh.sendline(command)

        self.ssh.expect(self.__prompt)        

        output = self.__getCommandOutput() 

        self.__commandOutputList.append(output)

        returnStatus = self.__getCommandStatus()

        self.__commandStatusList.append(returnStatus)

        Verboser.debug("output=" + str(output) + "\nreturnStatus=" + str(returnStatus), "BashSSHSession")

        Verboser.debug("END: executeCommand", "BashSSHSession")

        return (output, returnStatus)


    def exit(self):
        """
            Exit the ssh session
        """
        self.ssh.sendline("exit")

        self.ssh = None


    def __getCommandOutput(self):
        if isinstance(self.ssh.before, bytes):
            outputList = self.ssh.before.decode("utf-8").split(self.newLineString)

        else:
            outputList = str(self.ssh.before).split(self.newLineString)

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

        self.ssh.expect(self.__prompt)

        output = self.__getCommandOutput()
    
        retstat = False

        if output == "0":
            retstat = True

        return retstat 
        

if __name__ == "__main__":
    print("no thanks") 
