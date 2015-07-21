#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#
import os, sys, time, ast, datetime
import string
import random

from string import Template
from java.lang import String
from java.util import Arrays
from org.apache.commons.collections.list import FixedSizeList;
from overtherepy import SshConnectionOptions, OverthereHost, OverthereHostSession, BashScriptBuilder

from buildserver.UnixBuildServerUtil import UnixBuildServerUtil

class UnixBuildWorkspace(object):
    def __init__(self, server, name):
        self.name = name
        self.server = UnixBuildServerUtil.createUnixBuildServer(server)
        self.server.set_working_directory(self.name)


    @staticmethod

    def createWorkspace(server, name):

        return UnixBuildWorkspace(server, name)


    def execute_command(self,command):

       return server.execute_command(command)

    # session related methods

