#!/usr/bin/python3
import hashlib
import sys

#colors
W = "\033[1;38;48m"
R = "\033[1;31;48m"
G = "\033[1;30;48m"
HG = "\033[1;38;100m"






class hashcrack():

    def __init__(self):
        #---------defining parameters-------------#
        try:
            self.hash_to_crack = sys.argv[1]
            self.wordlist_file = sys.argv[2]
            self.hashed_password_list = []
            self.display_failed_attempts = 0
        except IndexError:
            print(f"{W} usage : Hashcrack.py <hash>  <wordlist> ")
            exit()
        except Exception as e:
            print(str(e))

    #----------display banner-----------------#
    def display_banner(self):

        print(f"""{W}\n
            H͟a͟s͟h͟c͟r͟a͟c͟k {R}
            01001000 01100001
             01110011 01101000
              01100011 01110010
               01100001 01100011
                01101011 {W} hash cracking tool - created by ( o-sec ) 

                """)


    #----------------------- determine the hash algorithm -----------------------------#
    def hash_Algo(self,Hash):
        if len(Hash) == 32:
            return "md5"
        elif len(Hash) == 40:
            return "sha1"
        elif len(Hash) == 64:
            return "sha256"
        elif len(Hash) == 96:
            return "sha384"
        elif len(Hash) == 128:
            return "sha512"
        elif len(Hash) == 0:
            return
        else :
            return


    #----------------- read passwords from wordlist file and convert them to hashes ---------------------#
    def read_wordlist_file(self,wordlist):

        try:
            with open(wordlist, "r") as Wordlist:
                self.password_list = Wordlist.read().split("\n")
                print(f"[+] - parsing the wordlist ...")
                #------- validate the given hash  -----#
                if len(self.hash_to_crack) >= 32 and len(self.hash_to_crack) <= 128 :
                    for password in self.password_list:
                        hashlib_object = hashlib.new(self.hash_Algo(self.hash_to_crack))
                        hashlib_object.update(password.encode('utf-8'))
                        hashed_password = hashlib_object.hexdigest()
                        self.hashed_password_list.append(hashed_password)
                else :
                    print(f"{R}[!] invalid hash format !")
                    exit()
        except FileNotFoundError :
            print(f"{R}[!] wordlist file not found !")
            exit()
        except TypeError:
            print(f"{R}[!] invalid hash format !")
            exit()



    #----------------- compare the given hash with the hash of each word in the list --------------#
    def compare(self):
        hash_algorithm = self.hash_Algo(self.hash_to_crack)
        print(f"{W}[+] - cracking [ {HG}{self.hash_to_crack}{W} ]\n")
        try:
            for hashed_passwd in self.hashed_password_list:
                INDEX = self.hashed_password_list.index(hashed_passwd)
                if hashed_passwd == self.hash_to_crack:
                    passwd = self.password_list[INDEX]
                    #password found
                    print("\n")
                    print(f"{W} [-] password : {G}{passwd} ")
                    print(f"{W} [-] hash algorithm : {G}{hash_algorithm} ")
                    print(f"{W} [-] hash : \n{G}{hashed_passwd} \n")
                    break

                elif hashed_passwd != self.hash_to_crack and self.display_failed_attempts :
                    print(f"{R} [!] no match  --> {self.password_list[INDEX]} ")
        except KeyboardInterrupt as k:
            print(f"{R} [!] - KeyboardInterrupt ! ")

try:
    hash_cracker = hashcrack()
    hash_cracker.display_banner()
    #start cracking
    hash_cracker.read_wordlist_file(hash_cracker.wordlist_file)
    hash_cracker.compare()
except Exception as e:
    print(str(e))
