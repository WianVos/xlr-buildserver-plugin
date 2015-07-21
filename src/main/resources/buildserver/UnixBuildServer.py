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


class UnixBuildServer(object):
    def __init__(self, server):
        self.sshOpts = SshConnectionOptions(server['host'], username=server['username'],password=server['password'])
        self.host = OverthereHost(self.sshOpts)
        self.session = OverthereHostSession(self.host)

        self.base_working_directory = server['BaseWorkingDirectory']
        self.working_directory = self.base_working_directory

        self.create_working_directory(self.base_working_directory)
        workDir = self.session.remote_file(self.base_working_directory)
        self.session.get_conn().setWorkingDirectory(workDir)

    @staticmethod
    def createServer(server):

        return UnixBuildServer(server)


    def set_working_directory(self, relative_directory_path):
        self.working_directory = "%s/%s" % (self.base_working_directory, relative_directory_path)
        self.create_working_directory(self.working_directory)
        workDir = self.session.remote_file(self.working_directory)
        self.session.get_conn().setWorkingDirectory(workDir)

    # main interface


    # session related methods

    def close_session(selfs):
        self.session.close()

    def create_working_directory(self, dir_full_path):
        response = self.session.execute("/bin/mkdir -p %s" % (dir_full_path))

    # File Handeling
    def read_file_in_workspace(self, file_name):
        print "not yet implemented"

    def write_file_in_workspace(self, file_name, content):
        print "not yet implemented"

    def create_directory(self, directory_name):
        self.execute_command(["/bin/mkdir -p %s" % (directory_name)])


    # command Execution
    def filename_generator(self, size=9, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_tmp_script_filename(self):
        return "%s.sh" % self.filename_generator()

    def execute_command(self, command, environment_variables=None):
        # get a BashScriptBuilder object
        command_object = BashScriptBuilder()

        # copy in the environment variables
        if environment_variables is not None:
            for key, value in environment_variables.items():
                command_object.set_env_var(key, value)

        # add the rest of the possible multiline command
        command_object.add_lines(command)

        executable_command = command_object.build()

        print "executing command: %s " % (executable_command)

        tmp_script_filename = self.get_tmp_script_filename()

        self.session.upload_text_content_to_work_dir(command_object.build(), tmp_script_filename, executable=True)
    #
        response = self.session.execute("%s/%s" % (self.working_directory, tmp_script_filename), check_success=False, suppress_streaming_output=False)

        if response.rc != 0:
            print response.stderr
            print response.stdout
            print "unable to execute command %s" % (command)
            raise Exception('unable to execute command')
        else:
            print "Response:", str(response.stdout)
            return response





# Utility functions




    #
    #
    #
    #
    # def createServer(server):
    #     return UnixBuildServer(server)
    # #
    #
    # def init_dar(self, appName, appVersion):
    #     workspace_root = self.create_dar_directory(appName, appVersion)
    #     manifest_filename = "%s/deployit-manifest.xml" % workspace_root
    #     self.write_dar_manifest(appName, appVersion, workspace_root)
    #
    # def import_ear(self, appName, appVersion, deployable, url):
    #     self.download_file_into_dar(appName, appVersion,deployable, str(url))
    #
    # def create_dar_directory(self, appName, appVersion):
    #     dirName = "%s/%s" % (appVersion, appName)
    #
    #     # check if the directory exists .. if it does we should go do something else.
    #     # might want to do a better locking mechanism
    #     if self.dir_exists(dirName):
    #       print "unable to create dar directory: %s/%s/%s" % (self.workingDirectory, appVersion, appName)
    #       raise Exception('unable to create Dar Package Directory')
    #     else:
    #       self.create_directory(dirName)
    #
    #     return dirName
    #
    #
    # def download_file_into_dar(self, appName, appVersion, deployable, url):
    #     #filename = url.split('/')[-1]
    #     filename = os.path.basename(url)
    #     outfile = "%s/%s/%s/%s" % (appVersion, appName,deployable, filename)
    #     dirName =  "%s/%s/%s" % (appVersion, appName,deployable)
    #     if self.dir_exists(dirName):
    #       print "output dir already exists: %s" % (dirName)
    #     else:
    #       self.create_directory(dirName)
    #
    #     self.execute_command("/usr/bin/curl -L -o %s %s" % (outfile, url))
    #
    # def read_manifest(self, appName, appVersion):
    #     file_name = "%s/%s/%s/deployit-manifest.xml" % (self.workingDirectory, appVersion, appName)
    #     return self.session.read_file(file_name, encoding="UTF-8")
    #
    #
    # def write_manifest(self, appName, appVersion, content):
    #     file_name = "%s/%s/deployit-manifest.xml" % (appVersion, appName)
    #     self.write_to_file(file_name, content)
    #
    # def create_directory(self, dirName):
    #     self.execute_command("/bin/mkdir -p %s" % (dirName))
    #
    # def create_file(self, fileName, content=None):
    #     if content:
    #      self.write_to_file(fileName, str(content))
    #     else:
    #      self.execute_command("/bin/touch %s" % (fileName))
    #
    #
    # def write_to_file(self, fileName, content):
    #     remoteFile = self.session.remote_file("%s/%s" % (self.workingDirectory, fileName))
    #     self.session.copy_text_to_file(str(content), remoteFile)
    #
    # def dir_exists(self, dirName):
    #     print dirName
    #     command = "[ -d %s ]" % (dirName)
    #     response = self.session.execute(command, check_success=False, suppress_streaming_output=False)
    #
    #     if response.rc == 0 :
    #       return True
    #     else:
    #       return False
    #
    #
    # def execute_command(self, command):
    #     print "executing command: %s " % (command)
    #     response = self.session.execute(command, check_success=False, suppress_streaming_output=False)
    #
    #
    #     if response.rc != 0:
    #       print response.stderr
    #       print "unable to execute command %s" % (command)
    #       raise Exception('unable to execute command ')
    #     else:
    #       print "Response:", str(response.stdout)
    #
    #    # self.switch_working_directory()
    #     return response
    #
    #
    # def write_dar_manifest(self, appName, appVersion, workspace_root):
    #    filename = "./%s/deployit-manifest.xml" % (workspace_root)
    #    file_content = self.basic_dar_manifest_template().substitute(appVersion=appVersion, appName=appName)
    #    self.create_file(filename, file_content)
    #
    # def basic_dar_manifest_template(self):
    #    xml_template  = '<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n'
    #    xml_template += ' <udm.DeploymentPackage version=\"$appVersion\" application=\"$appName\"> \n'
    #    xml_template += '   <orchestrator /> \n'
    #    xml_template += '   <deployables/> \n'
    #    xml_template += ' </udm.DeploymentPackage> \n'
    #    return Template(xml_template)
    #
    # def package_dar(self, appName, appVersion):
    #     command = "if [ -f %s_%s.dar ] \n"
    #     command += " then rm -rf %s_%s.dar \n"
    #     command += "fi \n"
    #     command += "cd %s/%s \n" % (appVersion, appName)
    #     command += "/usr/bin/zip -r %s/%s_%s.dar *" % (self.workingDirectory, appName, appVersion.replace('.','_'))
    #     self.execute_multiline_command(command)
    #
    # def write_exec_script(self, commands, script):
    #     self.session.upload_text_content_to_work_dir(self, commands, script, executable=False)
    #
    # def execute_multiline_command(self, command):
    #
    #     tmp_filename = self.filename_generator()
    #     self.write_to_file(tmp_filename, command)
    #     self.execute_command("chmod +x %s" % (tmp_filename))
    #     self.execute_command("./%s" % (tmp_filename))
    #
    #
    # def filename_generator(self, size=9, chars=string.ascii_uppercase + string.digits):
    #     return ''.join(random.choice(chars) for _ in range(size))
    #
    # def upload_dar_package(self, appName, appVersion, xldeployServer):
    #     dar_file_name = "%s_%s.dar" % (appName, appVersion.replace('.','_'))
    #     command = "/usr/bin/curl -u %s:%s -X POST -H \"content-type:multipart/form-data\" %s/package/upload/%s -F fileData=@./%s " % (xldeployServer['username'], xldeployServer['password'], xldeployServer['url'], dar_file_name, dar_file_name)
    #     print command
    #     self.execute_command(command)
