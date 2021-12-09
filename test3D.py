import pickle

def main():
    with open('outfile', 'rb') as fp:
        itemlist = pickle.load(fp)

if __name__ == "__main__":
    main()