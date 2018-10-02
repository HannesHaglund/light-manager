import argparse
import subprocess
import os
import sys
import datetime

def subprocess_run(*popenargs, input=None, check=False, **kwargs):
    if input is not None:
        if 'stdin' in kwargs:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = subprocess.PIPE

    process = subprocess.Popen(*popenargs, **kwargs)
    try:
        stdout, stderr = process.communicate(input)
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise subprocess.CalledProcessError(
            retcode, process.args, output=stdout, stderr=stderr)
    return retcode, stdout, stderr

def run_light_manager(lmpath, args):
    cmdstr = " ".join(args)
    os.system('python3 ' + lmpath + " ")
    code, stdout, stderr = subprocess_run('python3 ' + lmpath + " " + cmdstr, shell=True, stdout=subprocess.PIPE)
    if code == 0:
        print(stdout.decode('Utf-8'))
    else:
        raise RuntimeError('Subprocess failure: ' + stderr)

def do_update(lmpath, conf, last_command, update_command):
    auto_mode = False
    DRY_RUN = False
    dry_run_str = '--dry-run' if DRY_RUN else ''
    print(datetime.datetime.now())
    if update_command in '0123456789':
        run_light_manager(lmpath, ['toggle', dry_run_str, update_command, conf])
    elif update_command == 'a':
        run_light_manager(lmpath, ['refresh', dry_run_str, conf])
        auto_mode = True
    elif update_command == 'r':
        if last_command == '' or last_command == 'a':
            auto_mode = True
            run_light_manager(lmpath, ['refresh', dry_run_str, conf])
    run_light_manager(lmpath, ['art', conf])
    print("Mode: " + ("Automatic" if auto_mode else "Manual"))
    print("Upcoming events: ...")
    run_light_manager(lmpath, ['upcoming-events', conf, '-n 8'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('light_manager_path', type=str,
                        help='Path to light-manager.py')
    parser.add_argument('config_path', type=str,
                        help='Path to light-manager config file')
    parser.add_argument('last_command', type=str,
                        help='Last update command used')
    parser.add_argument('update_command', type=str,
                        help='Update command to use')
    args = parser.parse_args()
    do_update(args.light_manager_path, args.config_path, args.last_command, args.update_command)



if __name__ == '__main__':
    main()
