import unittest
import os
import re
import subprocess
from commands.utilities.config import Config

def local_path():
    return os.path.realpath('.')

def run_manager(argstr, test_case=None):
    cmd = 'python3 ' + local_path() + '/light_manager.py ' + argstr
    cmd_as_list = cmd.split(' ')
    proc = subprocess.Popen(cmd_as_list, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    exitcode = proc.returncode
    if test_case is not None:
        if exitcode != 0:
            print('=== Process exited with non-zero exit code ' + str(exitcode))
            print(cmd)
            print('=== stdout:')
            print(out)
            print('=== stderr:')
            print(err)
            test_case.assertTrue(False)
    return out

def test_config():
    return Config(local_path() + '/test_config.conf')

class TestCommands(unittest.TestCase):

    def test_help(self):
        t = run_manager('-h', self)
        self.assertTrue('usage' in t)
        self.assertTrue('positional arguments' in t)
        self.assertTrue('optional arguments' in t)

    def test_art(self):
        t = run_manager('set-art ' + \
                    local_path() + '/test_art_a.txt ' + \
                    local_path() + '/test_config.conf', self)
        t = run_manager('art ' + local_path() + '/test_config.conf', self)
        self.assertTrue('ArtA!' in t, self)
        run_manager('set-art ' + \
                    local_path() + '/test_art_b.txt ' + \
                    local_path() + '/test_config.conf', self)
        t = run_manager('art ' + local_path() + '/test_config.conf', self)
        self.assertTrue('ArtB!' in t)

    def test_upcoming_events(self):
        t = run_manager('upcoming-events ' + \
                        local_path() + '/test_config.conf', self)
        self.assertTrue('Monday' in t)
        self.assertTrue('1300' in t)
        self.assertTrue('#0' in t)

    def test_turn(self):
        t = run_manager('turn 0 off --dry-run ' + \
                        local_path() + '/test_config.conf', self)
        self.assertFalse(test_config().light_on(0))
        t = run_manager('turn 0 on --dry-run ' + \
                        local_path() + '/test_config.conf', self)
        self.assertTrue(test_config().light_on(0))
        t = run_manager('reset --dry-run ' + \
                        '-t 0100 -d 20180903 ' + # A monday, 0100 \
                        local_path() + '/test_config.conf', self)
        self.assertFalse(test_config().light_on(0))


    def test_refresh_no_crash(self):
        run_manager('refresh --dry-run ' + \
                    local_path() + '/test_config.conf', self)




if __name__ == '__main__':
    unittest.main()
