import argparse
import string
import warnings
from request import Request
from hash_guesser import HashGuesser

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import crypt


def define_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='The shadow file we want to crack the password of.')
    parser.add_argument('users', nargs='*')

    request = Request()
    args = parser.parse_args()
    request.file = args.file
    request.users = args.users

    if len(request.users) < 1 or request.users is None:
        print("Must include usernames")
        quit()

    if request.file is None:
        print("Must include a shadow fie to look at the hash")
        quit()

    return request


def extract_etc_shadow(hashed_line):
    info_array = hashed_line.split(":")
    hash_details = info_array[1][1:].split('$')

    hash_guess = HashGuesser()
    hash_guess.username = info_array[0]
    hash_guess.id = hash_details[0]

    hash_guess.salt = hash_details[1]
    hash_guess.hashed = hash_details[2]
    hash_guess.last_updated = info_array[2]
    hash_guess.hashed_password = info_array[1]
    hash_guess.identify_hash()
    return hash_guess


def find_lines_from_user(req: Request, username):
    try:
        with open(req.file, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith(username):
                    return line
    except Exception as e:
        print(f'Exception: {e}')


# def start_guessing(guesses):


def find_lines(request, hashed_lines):
    for user in request.users:
        found = find_lines_from_user(request, user)
        if found:
            hashed_lines.append(found)


def generate_guessers(hashed_lines, guessers):
    for hashed_line in hashed_lines:
        guessers.append(extract_etc_shadow(hashed_line))


def start_cracking(guessers : list[HashGuesser]):

    letters_length = 1
    for hash_guesser in guessers:
        while hash_guesser.cracked_password is None:
            hash_guesser.crack_hash(list(string.ascii_letters), letters_length)
            letters_length += 1
        letters_length = 1



def main():
    request = define_arguments()
    hashed_lines = []
    guessers = []

    find_lines(request, hashed_lines)
    generate_guessers(hashed_lines, guessers)
    start_cracking(guessers)


if __name__ == '__main__':
    main()




