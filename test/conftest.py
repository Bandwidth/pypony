"""
Documentation for hooks:
https://docs.pytest.org/en/6.2.x/reference.html#hooks
"""

import os
import platform
import subprocess

server_process: subprocess.Popen
PORT = 8000


def pytest_configure():
    """
    Allow plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest file after command line options have been parsed.
    After that, the hook is called for other conftest files as they are imported.
    """

    # Find Python executable
    if platform.system() == 'Windows':
        try:
            proc = subprocess.run(['where', 'python'], capture_output=True)
        except subprocess.CalledProcessError:
            proc = subprocess.run(['where', 'python3'], capture_output=True)
        python = proc.stdout.split(b'\r\n')[0]
    else:
        proc = subprocess.run(['python3', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        python = 'python3' if proc.returncode == 0 else 'python'

    # Directories
    server_root = os.path.join('test', 'api', 'openapi')
    server_file = os.path.join(server_root, 'manage.py')

    # Migrate server database
    database_file = os.path.join(server_root, 'db.sqlite3')
    print('Migrating database')
    if os.path.exists(database_file):
        os.remove(database_file)
    subprocess.run([python, server_file, 'migrate'])

    # Run server
    os.environ["DJANGO_SETTINGS_MODULE"] = "openapi.settings"
    print(f'Running server at port {PORT}')
    global server_process

    # Enable --nothreading otherwise it will leave orphan processes
    server_process = subprocess.Popen([python, server_file, 'runserver', str(PORT), '--noreload', '--nothreading'])


def pytest_unconfigure():
    """
    Called before test process is exited.
    """

    print('Shutting down server')
    server_process.kill()
