import struct
from flask import Flask, render_template, request

app = Flask(__name__)

def endianChanger(endian_type, hex_data):
    hex_bytes = bytes.fromhex(hex_data)
    if endian_type.lower() == 'little_endian':
        hex_bytes = hex_bytes[::-1]
    return hex_bytes

def hexToBin(selected_bytes):
    binary_representation = ''.join(format(byte, '08b') for byte in selected_bytes)
    return binary_representation

def hexToFloat32(selected_bytes):
    if len(selected_bytes) != 4:
        return "not calculated"
    decoded_value = struct.unpack('<f', selected_bytes)[0]
    return decoded_value

def hexToSignedInt(selected_bytes):
    if len(selected_bytes) == 1:
        format_str = '>b'
    elif len(selected_bytes) == 2:
        format_str = '>h'
    elif len(selected_bytes) == 4:
        format_str = '>i'
    else:
        return "not calculated"
    decoded_value = struct.unpack(format_str, selected_bytes)[0]
    return decoded_value

def hexToUnSignedInt(selected_bytes):
    if len(selected_bytes) == 1:
        format_str = '>B'
    elif len(selected_bytes) == 2:
        format_str = '>H'
    elif len(selected_bytes) == 4:
        format_str = '>I'
    else:
        return "not calculated"

    decoded_value = struct.unpack(format_str, selected_bytes)[0]
    return decoded_value

def hexToChar(selected_bytes):
    try:
        decoded_value = selected_bytes.decode('utf-8')
        return decoded_value
    except UnicodeDecodeError:
        return "Invalid UTF-8 encoding"

def hexToDouble(selected_bytes):
    if len(selected_bytes) != 8:
        return None
    decoded_value = struct.unpack('>d', selected_bytes)[0]
    return decoded_value

# Define routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hex_veri = request.form['hex_veri']
        endian_tipi = request.form['endian_tipi']
        multiplier = (request.form['multiplier'])
        multiplier = eval(multiplier)

        hex_veri = endianChanger(endian_tipi, hex_veri)
        float_result = hexToFloat32(hex_veri) * multiplier
        signed_int_result = hexToSignedInt(hex_veri) * multiplier
        unsigned_int_result = hexToUnSignedInt(hex_veri) * multiplier
        char_result = hexToChar(hex_veri)
        double_result = hexToDouble(hex_veri)

        return render_template('index.html', float_result=float_result, signed_int_result=signed_int_result,
                               unsigned_int_result=unsigned_int_result, char_result=char_result, double_result=double_result)

    return render_template('index.html', float_result=None, signed_int_result=None,
                           unsigned_int_result=None)

if __name__ == '__main__':
    app.run(debug=True)


#todo: epoch time calculation, crc calculations, byte sayma, 