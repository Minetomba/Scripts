import sys
import subprocess
import base64
import os
operating = sys.platform

class Cryptography:
    def encode(message: str) -> str:
        base64_encoded = base64.b64encode(message.encode()).decode()
        binary_encoded = ''.join(format(ord(char), '08b') for char in base64_encoded)
        hex_encoded = hex(int(binary_encoded, 2))[2:]
        reversed_hex = hex_encoded[::-1]
        encoded_message = f"s+{reversed_hex}="
        
        return encoded_message

    def decode(encoded_message: str) -> str:
        stripped_message = encoded_message[2:-1]
        reversed_hex = stripped_message[::-1]
        binary_encoded = bin(int(reversed_hex, 16))[2:].zfill(len(reversed_hex) * 4)
        base64_encoded = ''.join(chr(int(binary_encoded[i:i+8], 2)) for i in range(0, len(binary_encoded), 8))
        decoded_message = base64.b64decode(base64_encoded).decode()
        
        return decoded_message

class Bundler:
    @staticmethod
    def bundle(dir_to_bundle: str, output_file: str, enc='utf-8'):
        print("Creating bundle")
        
        with open(output_file, 'w') as bundle_file:
            # Write the header for the bundle script
            print("Writing headers")
            print("Writing OS Header")
            bundle_file.write('import os\n')
            print("Writing Base64 Header")
            bundle_file.write('import base64\n')

            # Function to recreate the directory and its files
            print("Creating extract function")
            bundle_file.write('def recreate_directory():\n')

            # Write code to create the root directory where everything will be extracted
            print(f"Creating root directory: {dir_to_bundle}")
            bundle_file.write(f'    os.makedirs(r"{dir_to_bundle}", exist_ok=True)\n')
            print("Parsing files")
            # Walk through the directory to find all files and subdirectories
            for root, dirs, files in os.walk(dir_to_bundle):
                # Create corresponding directories (use raw strings to avoid escape sequence issues)
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    relative_dir_path = os.path.relpath(dir_path, dir_to_bundle)
                    print(f"Creating directory: {relative_dir_path}")
                    print("Writing directory creation function")
                    bundle_file.write(f'    os.makedirs(r"{os.path.join(dir_to_bundle, relative_dir_path)}", exist_ok=True)\n')

                # Write files into the bundle script
                for file_name in files:
                    print(f"Processing file: {file_name}")
                    file_path = os.path.join(root, file_name)
                    relative_path = os.path.relpath(file_path, dir_to_bundle)
                    print(f"Reading and encoding file: {file_name}")
                    
                    # Read the file content and encode it
                    with open(file_path, 'rb') as f:
                        file_content = f.read()
                        print(f"Using {enc.upper()} Encoding and base64")
                        encoded_content = base64.b64encode(file_content).decode(enc)

                    # Write the file creation code into the bundle script
                    print("Writing creation usage...")
                    bundle_file.write(f'    with open(os.path.join(r"{dir_to_bundle}", r"{relative_path}"), "wb") as f:\n')
                    bundle_file.write(f'        f.write(base64.b64decode("{encoded_content}"))\n')

            # Call the function to recreate the directory and files
            print("Function creation finished")
            print("Writing function execution")
            bundle_file.write('if __name__ == "__main__":\n')
            bundle_file.write('    recreate_directory()\n')

        print("Created bundle")
class OSLinker:
    def system(command: str, output: bool):
        try:
            executed = str(command)
            if executed == "clear":
                if operating in ("win32", "win64", "win86"):
                    return subprocess.run("cls", shell=True, text=bool(output))
                elif operating in ("linux", "darwin"):
                    return subprocess.run("clear", shell=True, text=bool(output))
                else:
                    print("==== - Invalid OS - ====")
                    raise OSError
            if executed == "ipconfig":
                if operating in ("win32", "win64", "win86"):
                    return subprocess.run("ipconfig", shell=True, text=bool(output))
                elif operating in ("linux", "darwin"):
                    return subprocess.run("ifconfig", shell=True, text=bool(output))
                else:
                    print("==== - Invalid OS - ====")
                    raise OSError
            if executed == "ls":
                if operating in ("win32", "win64", "win86"):
                    return subprocess.run("dir", shell=True, text=bool(output))
                elif operating in ("linux", "darwin"):
                    return subprocess.run("ls", shell=True, text=bool(output))
                else:
                    print("==== - Invalid OS - ====")
                    raise OSError
            if executed == "sl":
                if operating in ("win32", "win64", "win86"):
                    return subprocess.run("dir", shell=True, text=bool(output))
                elif operating in ("linux", "darwin"):
                    return subprocess.run("ls", shell=True, text=bool(output))
                else:
                    raise OSError("Invalid OS")
        except KeyboardInterrupt:
            print("Interrupted while executing a system command")
        except Exception as e:
            print(f"Error occured: {e}")
            return str(e)
class Utility:
    # Fix email verification function
    @staticmethod
    def verify_email(email: str):
        adresa = email
        if "@" in adresa and adresa.endswith((".com", ".net", ".ms", ".mail", ".ro")):
            return True
        else:
            return False

    # Function to check if a number is negative
    @staticmethod
    def is_negative(numb: int):
        return numb < 0

    # Radix Sort function that returns the sorted array
    @staticmethod
    def radix_sort(arr: list):
        if not arr:  # Handle edge case for empty list
            return arr

        def counting_sort(arr, exp):
            n = len(arr)
            output = [0] * n  # Output array to store sorted numbers
            count = [0] * 10  # Count array to store frequency of digits (0-9)

            # Store the count of occurrences for each digit in the numbers
            for i in range(n):
                index = (arr[i] // exp) % 10
                count[index] += 1

            # Update count[i] so that count[i] contains the actual position of this digit in output[]
            for i in range(1, 10):
                count[i] += count[i - 1]

            # Build the output array by placing the elements in their correct position
            i = n - 1
            while i >= 0:
                index = (arr[i] // exp) % 10
                output[count[index] - 1] = arr[i]
                count[index] -= 1
                i -= 1

            # Copy the sorted elements back into the original array
            for i in range(n):
                arr[i] = output[i]

        max_num = max(arr)
        exp = 1  # Represents the digit place (ones, tens, hundreds, etc.)
        while max_num // exp > 0:
            counting_sort(arr, exp)  # Call the nested counting_sort function
            exp *= 10

        return arr  # Ensure the sorted array is returned

    # Function to find the closest value in a list to a given value
    @staticmethod
    def closest_in(listt: list, to: int):
        # Convert tuple to list if necessary
        if isinstance(listt, tuple):
            listt = list(listt)

        # Filter out non-numeric items and convert strings to integers if possible
        numeric_list = []
        for item in listt:
            if isinstance(item, (int, float)):
                numeric_list.append(item)
            elif isinstance(item, str):
                try:
                    numeric_list.append(int(item))
                except ValueError:
                    continue  # Skip items that cannot be converted to integers

        # Sort the list using radix_sort (only works for non-negative integers)
        sorted_list = Utility.radix_sort(numeric_list)

        # Find the closest value to 'to'
        to = int(to)
        closest_value = min(sorted_list, key=lambda x: abs(x - to))

        return closest_value
    @staticmethod
    def get_prime_numbers(p: int):
        primes = []
        for i in range(2, p):
            isPrime = True
            for j in range(2, i//2 + 1):
                if i % j == 0:
                    isPrime = False
            if isPrime:
                primes.append(i)
        return primes
    @staticmethod
    def get_primes_in_list(arra: list):
        modifiable_arra = arra
        modifiable_arra = Utility.radix_sort(modifiable_arra)
        last = modifiable_arra[-1]
        primes = Utility.get_prime_numbers(last)
        result = []
        for item in arra:
            if item in primes:
                result.append(item)
        return result
    @staticmethod
    def is_prime(num: int):
        primes = Utility.get_prime_numbers(num)
        if num in primes:
            return True
        else:
            return False
    # @staticmethod
    # def get_time_zone(state: str, city: str):
    #     now = pendulum.now(f"{state.title()}/{city.title()}")
    #     now = now.to_datetime_string()
    #     result = {
    #         now.split(" ")[0]: now.split(" ")[1]
    #     }
