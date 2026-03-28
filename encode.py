import hashlib
# Defined by Bitcoin message signing protocol
# Provided by Vanderpoole
text = "I am Vanderpoole and I have control of the private key Satoshi\n"
text += "used to sign the first-ever Bitcoin transaction confirmed in block #170.\n"
text += "This message is signed with the same private key."

def encode_message(text):
    # Given an ascii-encoded text message, serialize a byte array
    # with the Bitcoin protocol prefix string followed by the text
    # and both components preceded by a length byte.
    # Returns a 32-byte hex value.
    prefix = "Bitcoin Signed Message:\n"
    prefix_byte = prefix.encode()
    text_byte = text.encode()
    pxlen_byte = bytes([len(prefix_byte)])
    txlen_byte = bytes([len(text_byte)])
    blob = pxlen_byte + prefix_byte + txlen_byte + text_byte
    gethash_digest = hashlib.sha256(blob).digest()
    second_hash = hashlib.sha256(gethash_digest).hexdigest()

    return second_hash

print(encode_message(text))