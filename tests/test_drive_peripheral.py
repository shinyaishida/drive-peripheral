import subprocess


def test_help_option():
    app_name = 'drive_peripheral.py'
    command = ['python', f'drive_peripheral/{app_name}', '-h']
    result = subprocess.run(command, capture_output=True)
    expected_output = f'''\
usage: {app_name} [-h]

Drive peripheral

options:
  -h, --help  show this help message and exit
'''
    assert result.stdout.decode('ASCII') == expected_output
