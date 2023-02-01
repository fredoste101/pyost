import pexpect

class SCPSession:
    """
        Class for transfering a file from a remote location to local machine
        using SCP with pexpect.
    """

    def __init__(self):
        self.ip             = ""
        self.user           = ""
        self.password       = ""
        self.timeout        = 600 #Timeout in seconds
        self.scpSession     = None
 

    def getFile(self, srcFile, dstFile):
        """
            Copies the srcFile (ex /this/is/myfile.txt) from remote host, 
            to dstFile (ex /this/is/anotherFile.txt or /this/is/adir) on local host
        """
        self.scpSession = pexpect.spawn("scp " + self.user + "@" + self.ip + ":" + srcFile + " " + dstFile)

        self.__expectAndSendPassword()


    def setFile(self, srcFile, dstFile):
        """
            Copies the srcFile (ex /this/is/myfile.txt) from local host,
            to dstFile (ex /this/is/anotherFile.txt or /this/is/adir) on remote host
        """
        self.scpSession = pexpect.spawn("scp " + srcFile + " " + self.user + "@" + self.ip + ":" + dstFile)

        self.__expectAndSendPassword()



    def getDir(self, srcDir, dstDir):
        """
            Copies the entire directory at srcDir (ex /path/to/dir) from remote host,
            into dstDir (ex /destination/dir) on local host
        """
        self.scpSession = pexpect.spawn("scp -r " + self.user + "@" + self.ip + ":" + srcDir + " " + dstDir)
        
        self.__expectAndSendPassword()


    
    def setDir(self, srcDir, dstDir):
        """
            Copies the srcFile (ex /this/is/myfile.txt) 
            to dstFile (ex /this/is/anotherFile.txt or /this/is/adir)
        """
        self.scpSession = pexpect.spawn("scp -r " + srcDir + " " + self.user + "@" + self.ip + ":" + dstDir)        
        
        self.__expectAndSendPassword()



    def __expectAndSendPassword(self):
        """
            Authenticate, and then wait for transfer complete.
            Waits for timeout seconds before giving up.
        """
        self.scpSession.expect("password:")
        self.scpSession.sendline(self.password)
        self.scpSession.expect(pexpect.EOF, timeout=self.timeout)