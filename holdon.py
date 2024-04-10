from subprocess import Popen, PIPE

if __name__ == '__main__':
    i = 0
    while True:
        i += 1
        p = Popen(['python', 'run.py', '--batch_id', str(i)], shell=True)
        p.wait()
        print('Restarting ...')
