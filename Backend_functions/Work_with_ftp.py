# -*- coding: utf-8 -*-
import ftplib
from ftplib import FTP


def display_tree_paths(tree: list) -> None:
    print(f'Result: {tree} \nLen: {len(tree)}')
    for path, file, dirs in tree:
        if path == "/":
            print("/")
        else:
            print(f'{"  " * path.count("/")}{path}')


class ConnectionToFtp(FTP):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_pasv(False)
        self.timeout = 3
        self.host: str = ''
        self.port: int = 0
        self.user: str = ''
        self.password: str = ''

    def check_connect(self, host: str, port: int = None) -> tuple[bool, str]:
        try:
            if port is None:
                self.connect(host=host)
            else:
                self.connect(host=host, port=port)
            self.host = host
            self.port = port
            return True, 'Connect Successfully!'
        except ConnectionRefusedError:
            return False, f'Not connect to {host=}; {port=};'
        except TimeoutError:
            return False, f'The connection time has expired'
        except Exception as ex:
            return False, f'Error connect -> {ex}'

    def check_login(self, user: str = "", password: str = "") -> tuple[bool, str]:
        try:
            if user and password:
                self.login(user=user, passwd=password)
            else:
                self.login()
            self.user = user
            self.password = password
            return True, 'Login Successfully!'
        except ftplib.error_perm:
            return False, f'Not login with {user=}; {password=};'
        except TimeoutError:
            return False, f'The connection time has expired'
        except Exception as ex:
            return False, f'Error login -> {ex}'

    def full_connect_login(self, host: str, port: int = None, user: str = "", password: str = "") -> tuple[bool, str]:
        resp = self.check_connect(host=host, port=port)
        if resp[0]:
            resp = self.check_login(user=user, password=password)
            if resp[0]:
                return True, 'Full connect and login successfully!'
        return resp

    def gen_ftp_walk(self, initial_path: str = "", response=None) -> list:
        # print(f'\nBegin {initial_path=}; {self.pwd()=}')
        if response is None:
            response = []
        if initial_path:
            try:
                self.cwd(initial_path)
            except Exception as ex:
                print(f'Error in Work_with_ftp.py in func gen_ftp_walk with self.cwd({initial_path}) \n{ex}')
                return []
        path = self.pwd()
        dir_names, filenames = [], []
        files = []
        self.dir(lambda e: files.append(e))
        for file_desc in files:
            desc = file_desc.split(maxsplit=8)
            # print(f'\t{desc=}')
            if desc[0][0] == 'd':
                dir_names.append(desc[8])
            else:
                filenames.append(desc[8])
        response.append((path, dir_names, filenames))
        for dir_name in dir_names:
            # print(f'\t\t\tNext {self.pwd()=}; {dir_name=}; {(path+r"/"+dir_name)=}')
            self.gen_ftp_walk(initial_path=(path + r"/" + dir_name), response=response)
        return response

    def check_welcome(self) -> None:
        print(self.welcome)

    def close_connect(self) -> None:
        self.close()

    def __str__(self) -> str:
        return f"Connect to {self.host}:{self.port} with login={self.login} and password={self.password}"
