from monero.wallet import Wallet

def generate_monero_address(private_key):
    wallet = Wallet(private_key=private_key)
    address = wallet.get_address()
    return address

def main():
    private_key = "juicy annoyed irate lopped ripped flippant aplomb gumball coffee twofold gasp alerts giddy code mesh woken taboo trendy zebra terminal waist stellar gymnast inorganic giddy"
    address = generate_monero_address(private_key)
    print("Monero Address:", address)

if __name__ == '__main__':
    main()
