import pexpect

class BashSCPSession:
    """
        Class for transfering a file from a remote location to local machine
        using SCP with pexpect.
    """
    def __init__(self):
        self.ip             = ""
        self.user           = ""
        self.password       = ""
 
    def copyFile(self, srcFile, dstFile):
        scpSession = pexpect.spawn("scp " + self.user + "@" + self.ip + ":" + srcFile + " " + dstFile)        
        scpSession.expect("password:")
        scpSession.sendline(self.password)
        scpSession.expect(pexpect.EOF, timeout=600)

    def copyDir(self, srcDir, dstDir):
        scpSession = pexpect.spawn("scp -r " + self.user + "@" + self.ip + ":" + srcDir + " " + dstDir)
        scpSession.expect("password:")
        scpSession.sendline(self.password)
        scpSession.expect(pexpect.EOF, timeout=600)


         
