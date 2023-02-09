import subprocess
import os

if not os.path.exists('venv'):  # If not interpreter -> exit
    print("\nNo interpreter!\n Add in settings virtualenv!")
    exit()

way = os.path.join(os.getcwd(), r'venv\Scripts\python.exe')  # Const == way to python.exe
print(f'\tWay to python.exe: {way}\n')

if not os.path.exists('requirements.txt'):  # Create requirements.txt
    with open(file='requirements.txt', mode='w', encoding='utf-8') as _:
        pass


def generate_req():  # Generating req.txt with installed modules
    subprocess.check_call([way, '-m', 'pip', 'freeze'])  # 0

    str_bytes = subprocess.check_output([way, '-m', 'pip', 'freeze'])
    modules = str_bytes.decode('utf-8').split('\n')
    print(f'\nTotal modules: {len(modules) - 1}')
    if len(modules) - 1 > 0:
        with open(file='req.txt', mode='w', encoding='utf-8') as file:
            for module in modules:
                file.write(module)
        print(f"\n\t Generate req.txt -> Done!")
    print('*' * 50)


def install_module(module='mysql-connector-python'):  # Installing the module manually
    subprocess.check_call([way, '-m', 'pip', 'install', '--upgrade', 'pip'])
    print(f"\t Upgrade pip -> Done!")
    subprocess.check_call([way, '-m', 'pip', 'install', module])
    print(f"\t Install module '{module}' -> Done!")
    print('*' * 50)


def uninstall_module(module='mysql-connector-python'):  # Uninstalling the module manually
    subprocess.check_call([way, '-m', 'pip', 'uninstall', module])
    print(f"\t Uninstall module '{module}' -> Done!")
    print('*' * 50)


def install_modules():  # Module installer from a file
    subprocess.check_call([way, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([way, '-m', 'pip', 'install', '-U', 'pip', 'setuptools'])
    subprocess.check_call([way, '-m', 'pip', 'install', 'matplotlib'])
    subprocess.check_call([way, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    print(f"\n\t Install modules from requirements.txt -> Done!")
    print('*' * 50)


if __name__ == '__main__':
    generate_req()
    # install_module('mysql-connector-python')
    # uninstall_module('mysql-connector-python')
    # install_modules()
    print(f"\n{'*' * 20} Done! {'*' * 20}")
