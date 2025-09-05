#reads the raw text file
with open("raw_text.txt", "r") as Ofile:
    string = Ofile.read()
ecrypted_string = ""

#gets shift values from user
shift1 = int(input("Enter shift 1 value: "))
shift2 = int(input("Enter shift 2 value: "))
print("Pre-encryption\n"+string)
#encrypts the string
for char in string:
    counter = 0
    if char.islower():
        encrypted_letter = ord(char)
        #checks if letter is in first half of alphabet and shifts accordingly
        if ord("a") <= encrypted_letter <= ord("m"):
            while counter < shift1 * shift2:
                encrypted_letter += 1
                if encrypted_letter > ord("m"):
                    encrypted_letter = ord("a")
                counter += 1
            ecrypted_string += chr(encrypted_letter)
        #checks if letter is in second half of alphabet and shifts accordingly
        elif ord("n") <= encrypted_letter <= ord("z"):
            while counter < shift1 + shift2:
                encrypted_letter -= 1
                if encrypted_letter < ord("n"):
                    encrypted_letter = ord("z")
                counter += 1
            ecrypted_string += chr(encrypted_letter)

    elif char.isupper():
        encrypted_letter = ord(char)
        #checks if letter is in first half of alphabet and shifts accordingly
        if ord("A") <= encrypted_letter <= ord("M"):
            while counter < shift1:
                encrypted_letter -= 1
                if encrypted_letter < ord("A"):
                    encrypted_letter = ord("M")
                counter += 1
            ecrypted_string += chr(encrypted_letter)
        #checks if letter is in second half of alphabet and shifts accordingly
        elif ord("N") <= encrypted_letter <= ord("Z"):
            while counter < shift2 ** 2:
                encrypted_letter += 1
                if encrypted_letter > ord("Z"):
                    encrypted_letter = ord("N")
                counter += 1
            ecrypted_string += chr(encrypted_letter)
    else:
        ecrypted_string += char

#creates and writes the encrypted text to encrypted text file
print("\nEcrypted:\n"+ecrypted_string)
encrypted_txt = open("encrypted_text.txt", "w")
encrypted_txt.write(ecrypted_string)

string = ""
#decrypts the string
for char in ecrypted_string:
    counter = 0
    if char.islower():
        encrypted_letter = ord(char)
        #checks if letter is in first half of alphabet and shifts accordingly
        if ord("a") <= encrypted_letter <= ord("m"):
            while counter < shift1 * shift2:
                encrypted_letter -= 1
                if encrypted_letter < ord("a"):
                    encrypted_letter = ord("m")
                counter += 1
            string += chr(encrypted_letter)
        #checks if letter is in second half of alphabet and shifts accordingly    
        elif ord("n") <= encrypted_letter <= ord("z"):
            while counter < shift1 + shift2:
                encrypted_letter += 1
                if encrypted_letter > ord("z"):
                    encrypted_letter = ord("n")
                counter += 1
            string += chr(encrypted_letter)
               
    elif char.isupper():
        encrypted_letter = ord(char)
        #checks if letter is in first half of alphabet and shifts accordingly
        if ord("A") <= encrypted_letter <= ord("M"):
            while counter < shift1:
                encrypted_letter += 1
                if encrypted_letter > ord("M"):
                    encrypted_letter = ord("A")
                counter += 1
            string += chr(encrypted_letter)          
        #checks if letter is in second half of alphabet and shifts accordingly
        elif ord("N") <= encrypted_letter <= ord("Z"):
            while counter < shift2 ** 2:
                encrypted_letter -= 1
                if encrypted_letter < ord("N"):
                    encrypted_letter = ord("Z")
                counter += 1
            string += chr(encrypted_letter)
    else:
        string += char
#prints the decrypted string and writes it to the decrypted text file
print("\nDecrypted:\n"+string)
with open("raw_text.txt", "w") as Ofile:
    Ofile.write(string)
Decrypted_txt = open("Decrypted_text.txt", "w")
Decrypted_txt.write(string)


with open("raw_text.txt", "r") as Ofile:
    Ostring = Ofile.read()

#original string vs decrypted string check
if string == Ostring:
    print("The Decryption was a success!")