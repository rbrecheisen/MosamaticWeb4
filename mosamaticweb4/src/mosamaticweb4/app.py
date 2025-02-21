import os
import sys
import argparse

from django.core.management import execute_from_command_line


def run_server():
    appPath = os.path.join(os.path.abspath(__file__))
    appPath = os.path.dirname(appPath)
    appPath = os.path.join(appPath, 'backend')
    
    sys.path.append(appPath)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    os.environ.setdefault('OAUTHLIB_INSECURE_TRANSPORT', '1')
    
    os.chdir(appPath)
    
    print('##############################################################################')
    print('#                   M O S A M A T I C   W E B  4                             #')
    print('##############################################################################')
    
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    execute_from_command_line(['manage.py', 'create_admin_user'])
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])


def run_dicomserver():
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dicom-server', action='store_true', help='Runs in server mode')
    args = parser.parse_args()
    if args.dicom_server:
        print('Running DICOM server...')
        run_dicomserver()
    else:
        print('Running Mosamatic Web 4 server...')
        run_server()