from struct import pack
from bech32py import bech32
from random import randrange
from secp256k1py import secp256k1
import hashlib
# UTXO from chapter 6 step 1 (mining pool payout)
txid = "8a081631c920636ed71f9de5ca24cb9da316c2653f4dc87c9a1616451c53748e"
vout = 1
value = 161000000

# From chapter 4 (we will reuse address for change)
priv = 0x93485bbe0f0b2810937fc90e8145b2352b233fbd3dd7167525401dd30738503e
compressed_pub = bytes.fromhex("038cd0455a2719bf72dc1414ef8f1675cd09dfd24442cb32ae6e8c8bbf18aaf5af")
pubkey_hash = "b234aee5ee74d7615c075b4fe81fd8ace54137f2"
addr = "bc1qkg62ae0wwntkzhq8td87s87c4nj5zdlj2ga8j7"

# Explained in step 6
scriptcode = "1976a914" + pubkey_hash + "88ac"

class Outpoint:
    def __init__(self, txid: bytes, index: int):
        assert isinstance(txid, bytes)
        assert len(txid) == 32
        assert isinstance(index, int)
        self.txid = txid
        self.index = index

    def serialize(self):
        r = b""
        r += self.txid
        r += pack("<I", self.index)
        return r

class Input:
    def __init__(self):
        self.outpoint = None
        self.script = b""
        self.sequence = 0xffffffff
        self.value = 0
        self.scriptcode = b""

    @classmethod
    def from_output(cls, txid: str, vout: int, value: int, scriptcode: bytes):
        self = cls()
        self.outpoint = Outpoint(bytes.fromhex(txid)[::-1], vout)
        self.value = value
        self.scriptcode = bytes.fromhex(scriptcode)
        return self

    def serialize(self):
        r = b""
        r += self.outpoint.serialize()
        r += pack("<B", len(self.script))
        r += pack("<I", self.sequence)
        return r
# Use the bech32 library to find the version and data components from the address
# See the library source code for the exact definition
# https://github.com/saving-satoshi/bech32py/blob/main/bech32py/bech32.py

class Output:
    def __init__(self):
      self.value = 0
      self.witness_version = 0
      self.witness_data = b""

    @classmethod
    def from_options(cls, addr: str, value: int):
        assert isinstance(value, int)
        self = cls()
        self.value = value

        if addr.startswith("tb1"):
          hrp = "tb"
        elif addr.startswith("bc1"):
          hrp = "bc"
        else:
          print("invalid address hrp value")


        self.witness_version, witprog = bech32.decode(hrp, addr)
  
        self.witness_data = bytes(witprog)

        return self

    def serialize(self):
        r = b""
        
        # 1. Value (8 bytes, Little Endian)
        # 'Q' = unsigned long long (8 bytes)
        r += pack("<Q", self.value)
        
        # 2. Total Script Length (1 byte)
        # Script = [Version (1 byte)] + [Push Length (1 byte)] + [Data (N bytes)]
        total_script_len = 1 + 1 + len(self.witness_data)
        r += pack("<B", total_script_len)
        
        # 3. Witness Version (1 byte)
        r += pack("<B", self.witness_version)
        
        # 4. Data Length (1 byte)
        r += pack("<B", len(self.witness_data))
        
        # 5. Witness Data (Variable bytes)
        r += self.witness_data
        
        return r


class Witness:
    def __init__(self):
        self.items = []

    def push_item(self, data):
        self.items.append(data)

    def serialize(self):
        r = b""
        r += pack("<B", len(self.items))
        for item in self.items:
            r += pack("<B", len(item))
            r += item
        return r

class Transaction:
    def __init__(self):
        self.version = 2
        self.flags = bytes.fromhex("0001")
        self.inputs = []
        self.outputs = []
        self.witnesses = []
        self.locktime = 0

    def digest(self, input_index: int):
        # Helper: Double SHA-256
        def dsha256(data):
            return hashlib.sha256(hashlib.sha256(data).digest()).digest()

        # Start with an empty bytes object
        b = b""

        # 1. Version (4 bytes, Little Endian, Signed int 'i')
        b += pack("<i", self.version)

        # 2. Hash of All Outpoints (32 bytes)
        outpoints_buf = b""
        for tx_input in self.inputs:
            outpoints_buf += tx_input.outpoint.serialize()
        b += dsha256(outpoints_buf)

        # 3. Hash of All Sequences (32 bytes)
        sequences_buf = b""
        for tx_input in self.inputs:
            sequences_buf += pack("<I", tx_input.sequence)
        b += dsha256(sequences_buf)

        # --- Target Input Data ---
        target_input = self.inputs[input_index]

        # 4. Outpoint of the specific input (36 bytes)
        b += target_input.outpoint.serialize()

        # 5. ScriptCode (Variable bytes)
        b += target_input.scriptcode

        # 6. Value (8 bytes, Little Endian 'Q')
        b += pack("<Q", target_input.value)

        # 7. Sequence (4 bytes, Little Endian 'I')
        b += pack("<I", target_input.sequence)

        # --- End Target Input Data ---

        # 8. Hash of All Outputs (32 bytes)
        outputs_buf = b""
        for tx_output in self.outputs:
            outputs_buf += tx_output.serialize()
        b += dsha256(outputs_buf)

        # 9. Locktime (4 bytes, Little Endian 'I')
        b += pack("<I", self.locktime)

        # 10. Sighash Type (4 bytes, Little Endian 'I')
        # We use 1 (SIGHASH_ALL)
        b += pack("<I", 1)

        # Finally, return the double-SHA256 of the entire buffer
        return dsha256(b)




    def compute_input_signature(self, index: int, key: int):
        GE = secp256k1.GE
        G = secp256k1.G
        n = GE.ORDER

        assert isinstance(key, int)

        # 1. Get the message hash (m) as an integer
        digest_bytes = self.digest(index)
        m = int.from_bytes(digest_bytes, 'big')

        # 2. Generate random k (nonce)
        k = randrange(1, n)

        # 3. Calculate Point R = k * G
        R = GE.mul((k, G))

        # 4. Calculate r
        # CRITICAL FIX: Convert R.x (Field Element) to an int before modulo
        r = int(R.x) % n

        # 5. Calculate s
        k_inv = pow(k, -1, n)
        s = (k_inv * (r * key + m)) % n

        # 6. Enforce "Low S" (BIP 146)
        if s > n // 2:
            s = n - s

        return (r, s)

    def sign_input(self, index, priv, pub, sighash=1):
        def encode_der(r, s):
            # Represent in DER format. The byte representations of r and s have length rounded up
            # (255 bits becomes 32 bytes and 256 bits becomes 33 bytes).
            rb = r.to_bytes((r.bit_length() + 8) // 8, 'big')
            sb = s.to_bytes((s.bit_length() + 8) // 8, 'big')
            return b'\x30' + bytes([4 + len(rb) + len(sb), 2, len(rb)]) + rb + bytes([2, len(sb)]) + sb
        
        # 1. Compute the raw ECDSA signature (r, s)
        r, s = self.compute_input_signature(index, priv)
        
        # 2. Encode to DER format
        der_sig = encode_der(r, s)
        
        # 3. Append Sighash Type
        # Bitcoin requires the sighash byte (0x01 for ALL) at the end of the DER signature.
        final_sig = der_sig + bytes([sighash])
        
        # 4. Create the Witness Object
        # Structure: [Signature, Public Key]
        witness = Witness()
        witness.push_item(final_sig)
        
        # Handle Public Key (convert hex string to bytes if necessary)
        if isinstance(pub, str):
            witness.push_item(bytes.fromhex(pub))
        else:
            witness.push_item(pub)
            
        # 5. Attach the witness to the transaction
        self.witnesses.append(witness)

    def serialize(self):
        r = b""
        
        # 1. Version (4 bytes, little-endian)
        r += pack("<I", self.version)
        
        # 2. SegWit flags (2 bytes: 0x0001)
        r += self.flags
        
        # 3. Input count (1 byte varint)
        r += pack("<B", len(self.inputs))
        
        # 4. All inputs serialized
        for inp in self.inputs:
            r += inp.serialize()
        
        # 5. Output count (1 byte varint)
        r += pack("<B", len(self.outputs))
        
        # 6. All outputs serialized
        for out in self.outputs:
            r += out.serialize()
        
        # 7. All witnesses serialized (one per input)
        for wit in self.witnesses:
            r += wit.serialize()
        
        # 8. Locktime (4 bytes, little-endian)
        r += pack("<I", self.locktime)
        
        return r

tx = Transaction()
in0 = Input.from_output(txid, vout, value, scriptcode)
out0 = Output.from_options("bc1qgghq08syehkym52ueu9nl5x8gth23vr8hurv9dyfcmhaqk4lrlgs28epwj", 100000000)
# Change output: 60,999,000 sats (leaving 1,000 sats as miner fee)
out1 = Output.from_options(addr, 60999000)
tx.inputs.append(in0)
tx.outputs.append(out0)
tx.outputs.append(out1)
tx.sign_input(0, priv, compressed_pub)

print(tx.serialize().hex())
