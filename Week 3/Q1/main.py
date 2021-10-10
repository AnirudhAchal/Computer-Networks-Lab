import os


def main():
    domain = input('Enter the domain: ').replace('www.', '')
    os.system(f'nslookup -query=MX {domain}')


main()
