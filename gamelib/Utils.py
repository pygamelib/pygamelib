from colorama import Fore, Back, Style

def warn(message):
    print(Fore.BLACK + Back.YELLOW + 'WARNING' + Style.RESET_ALL + ': '+message)

def fatal(message):
    print(Fore.WHITE + Back.RED + Style.BRIGHT + 'FATAL' + Style.RESET_ALL + ': '+message)

def info(message):
    print(Fore.WHITE + Back.BLUE + 'INFO' + Style.RESET_ALL + ': '+message)

def debug(message):
    print(Fore.BLUE + Back.GREEN + Style.BRIGHT + 'DEBUG' + Style.RESET_ALL + ': '+message)