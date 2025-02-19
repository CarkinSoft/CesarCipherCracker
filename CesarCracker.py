import os
#I'm using Pickle to increment my test file name
import pickle
import string

#loads the dictionary file, initially i thought this needed to be entered by the user but it got annoying in testing and i realized you
#don't need to do it that way in the instructions so i just hardcoded the variable down in the main
def load_dictionary(dictionary_file):
    with open(dictionary_file, 'r') as file:
        words = set(word.strip().lower() for word in file)
    return words

#shifts the letters once the shift amount has been found
def decrypt_caesar_cipher(ciphertext, shift):
    #this is a predefined string of all letters a-z
    alphabet = string.ascii_lowercase
    #slices the alphabet to the right and concatenates it with another alphabet sliced to the left to make the shifted alphabet
    #resource used for this trick: https://www.geeksforgeeks.org/python-right-and-left-shift-characters-in-string/
    shifted_alphabet = alphabet[-shift:] + alphabet[:-shift]
    #using a translation table to replace each character in the string with the corresponding shifted alphabet version
    table = str.maketrans(shifted_alphabet, alphabet)
    return ciphertext.translate(table)


def is_valid_plaintext(plaintext, dictionary, threshold):
    words = plaintext.split()
    if not words:  #in case of empty string
        return False

#checks the dictionary for the current words that are found in the dictionary contained in the sentence
    valid_words_count = sum(1 for word in words if word.strip().lower() in dictionary)
    proportion_valid = valid_words_count / len(words)

    #threshold percentage is located below in main but this ensures at least 75% of the words in the sentence are found in the dictionary
    return proportion_valid >= threshold


def break_caesar_cipher(ciphertexts_file, dictionary_file, output_file):
    #load the English dictionary
    dictionary = load_dictionary(dictionary_file)

    #open the ciphertexts file and output file
    with open(ciphertexts_file, 'r') as infile, open(output_file, 'w') as outfile:
        print("Processing ciphertexts...")
        ciphertexts = infile.readlines()  #reads the ciphertext

        for index, ciphertext in enumerate(ciphertexts):
            ciphertext = ciphertext.strip()
            if not ciphertext:  #skip empty lines
                continue

            found = False
            for shift in range(26):
                plaintext = decrypt_caesar_cipher(ciphertext.lower(), shift)
                if is_valid_plaintext(plaintext, dictionary, threshold=0.75):
                    outfile.write(f"{shift};{plaintext}\n")
                    print(f"Line {index + 1}: {shift};{plaintext}")
                    found = True
                    break

            if not found:
                print(f"Error! Line {index + 1}: Could not decrypt.")

#I decided not to have this active in my submission because it's unecessary
def get_next_output_filename(base_name="testsolution", start_number=10):
    output_file_name = "decrypted_message.txt"
    return output_file_name

    """counter_file = "output_counter.pkl"

    #check if the counter file exists
    if os.path.exists(counter_file):
        #load the current counter value
        with open(counter_file, "rb") as file:
            current_number = pickle.load(file)
    else:
        #initialize the counter if it doesn't exist
        current_number = start_number

    #create the next output file name
    output_file_name = f"{base_name}{current_number}.txt"

    #increment the counter and save it back to the file
    with open(counter_file, "wb") as file:
        pickle.dump(current_number + 1, file)

    return output_file_name
"""

if __name__ == "__main__":
    #hardcoded dictionary file
    DICTIONARY_FILE = "en-US.dic"

    #prompt the user for the input ciphertext file
    ciphertexts_file = input("Enter the ciphertexts file: ").strip()

    #generate the output file name
    output_file = get_next_output_filename()

    try:
        break_caesar_cipher(ciphertexts_file, DICTIONARY_FILE, output_file)
        print(f"Decrypted message saved: {output_file}")
    except FileNotFoundError as e:
        print(f"Error: {e}. File not found.")
    except Exception as e:
        print(f"Error: {e}")