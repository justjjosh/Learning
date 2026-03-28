# Import from python standard libraries
import hashlib

def msg_to_integer(msg):
    # Given a hex string to sign, convert that string to bytes,
    # double-SHA256 the bytes and then return an integer from the 32-byte digest.
    
    # Step 1: Convert hex string to bytes
    msg_bytes = bytes.fromhex(msg)
    
    # Step 2: First SHA256 hash
    first_hash = hashlib.sha256(msg_bytes).digest()
    
    # Step 3: Second SHA256 hash (hash the hash)
    second_hash = hashlib.sha256(first_hash).digest()
    
    # Step 4: Convert the 32-byte digest to hex string
    hash_hex = second_hash.hex()
    
    # Step 5: Convert hex string to integer
    hash_int = int(hash_hex, 16)
    
    return hash_int


# Test with a simple transaction message
test_msg = "0100000001c997a5e5"
result = msg_to_integer(test_msg)

print(f"Input (hex): {test_msg}")
print(f"Output (integer): {result}")
print(f"Output (hex): {hex(result)}")
print(f"\nThis huge integer is what ECDSA will sign!")
