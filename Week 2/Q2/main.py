import socket


def print_menu():
    print('Menu')
    print('1. Convert Domain Name to IP Address')
    print('2. Convert IP Address to Domain Name')
    print('3. Exit')


def main():
    while True:
        print_menu()
        choice = input("Choice: ")
        if choice == '1':
            domain_name = input('Domain Name: ')
            ip_address = socket.gethostbyname(domain_name)
            print(f'IP Address: {ip_address}')
        elif choice == '2':
            ip_address = input('IP Address: ')
            domain_name = socket.gethostbyaddr(ip_address)
            print(f'Domain Name: {domain_name}')
        elif choice == '3':
            return
        else:
            print('Enter valid choice.')


main()
