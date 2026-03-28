import secp256k1py.secp256k1 as SECP256K1
# View the library source code
# https://github.com/saving-satoshi/secp256k1py/blob/main/secp256k1py/secp256k1.py

GE = SECP256K1.GE
G = SECP256K1.G

# Message digest from step 5:
msg = 0x7a05c6145f10101e9d6325494245adf1297d80f8f38d4d576d57cdba220bcb19

# Signature values from step 6:
sig_r = 0x4e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd41
sig_s = 0x181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d09

# Public key values from step 7:
pubkey_x = 0x11db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5c
pubkey_y = 0xb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3

def verify(sig_r, sig_s, pubkey_x, pubkey_y, msg):
    # Verify an ECDSA signature given a public key and a message.
    # All input values will be 32-byte integers.

    # Start by creating a curve point representation of the public key
    key = GE(pubkey_x, pubkey_y)

    # Next, check the range limits of the signature values
    if sig_r == 0 or sig_r >= GE.ORDER:
        print("invalid r value")
        return False
	
    if sig_s == 0 or sig_s >= GE.ORDER:
        print("invalid s value")
        return False
    
    #get sig s inverse
    sig_s_inv = pow(sig_s, -1, GE.ORDER)

    #calculate values for u1 and u2
    u1 = (msg * sig_s_inv) % GE.ORDER
    u2 = (sig_r * sig_s_inv) % GE.ORDER
    
    #calculate co-ordinates
    R = GE.mul((u1, G), (u2, key))

    #extracting the x coordinate from R
    r = int(R.x) % GE.ORDER

    #comparing the extracted coordinate to sig_r
    return r == sig_r

    # Implement ECDSA and return a boolean
    # The Math:
    #   u1 = m / s mod n
    #   u2 = r / s mod n
    #   R = G * u1 + A * u2
    #   r == x(R) mod n
    # Hints:
    #   n = the order of the curve GE.ORDER
    #   s, r = sig_s and sig_r, the two components of an ECDSA signature
    #   m = msg, the message to sign
    #   A = key, a key point constructed from pubkey_x and pubkey_y
    #   Use the python's built-in pow() function to invert s and turn division into multiplication!
    # YOUR CODE HERE!

print(verify(sig_r, sig_s, pubkey_x, pubkey_y, msg))
#print(dir(SECP256K1))
#print(f"G type: {type(G)}")
#print(f"Fast G type: {type(SECP256K1.FAST_G)}")
#print(f"G.mul signature: {G.mul.__doc__}")
#print(f"FAST_G.mul signature: {SECP256K1.FAST_G.mul.__doc__}")