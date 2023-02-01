import pexpect
from random import choice as randomChoice 
import string


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
        
        self.ssh = pexpect.spawn("ssh " + self.user + "@" + self.ip)

        self.ssh.expect("password:")

        self.ssh.sendline(self.password)

        #TODO: wait some time, and then check if password was ok.

        self.__createRandomPrompt()


    def __createRandomPrompt(self):
        """
            Create a random prompt to match against in other commands.
            This is to see when output from a command has reached its end.
        """

        pool = string.ascii_letters + string.digits

        self.__prompt = "".join(randomChoice(pool) for i in range(40)) + ":" 
        
        self.ssh.sendline("PS1=" + self.__prompt)
    
        self.ssh.expect(self.newLineString + self.__prompt)


    def executeCommand(self, command):
        """
            Execute given command (string).
            Returns the output as well as the return status of the command (0 - True, other - False)
            in a tuple (output, status)
        """

        self.ssh.sendline(command)

        self.ssh.expect(self.__prompt)        

        output = self.__getCommandOutput() 

        self.__commandOutputList.append(output)

        returnStatus = self.__getCommandStatus()

        self.__commandStatusList.append(returnStatus)

        return (output, returnStatus)


    def exit(self):
        """
            Exit the ssh session
        """
        self.ssh.sendline("exit")

        self.ssh = None


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

        self.ssh.expect(self.__prompt)

        output = self.__getCommandOutput()
    
        retstat = False

        if output == "0":
            retstat = True

        return retstat 
        

if __name__ == "__main__":
    print("no thanks") 
