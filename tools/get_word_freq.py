import sys

from wordfreq import word_frequency


def main():
    print(word_frequency(sys.argv[1], "en"))


if __name__ == "__main__":
    main()
