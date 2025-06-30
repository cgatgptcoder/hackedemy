from text import split_txt_by_words

def main():
    input_file = "output.txt"
    words_per_file = 500
    split_txt_by_words(input_file, words_per_file)

if __name__ == "__main__":
    main()
