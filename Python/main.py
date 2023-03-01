import binascii

def binary_to_hex(file_path):
    with open(file_path, 'rb') as binary_file:
        binary_data = binary_file.read()
        hex_data = binascii.hexlify(binary_data)
        return hex_data.decode()

hex_values = binary_to_hex('ethernet.result_data')
print(hex_values[0:16]) # Bench 1
print(hex_values[16:32]) # Frame Date
print(hex_values[32:40]) # Bench 3
print(hex_values[40:48]) # Bench 4,5,6
print(hex_values[48:56]) # Frame size
print(hex_values[56:68]) # Mac Dest
print(hex_values[68:80]) # Mac Source
print(hex_values[80:84]) # Field 1
print(hex_values[84:88]) # Field 2
print(hex_values[88:92]) # Field 3
print(hex_values[92:96]) # Field 4
print(hex_values[96:100]) # Field 5
print(hex_values[100:102]) # Field 6
print(hex_values[102:104]) # Field 7
print(hex_values[108:116]) # Source IP
print(hex_values[116:124]) # Dest IP
print(hex_values[124:128]) # Field 9
print(hex_values[128:132]) # Field 10
print(hex_values[132:136]) # Field 11
print(hex_values[140:144]) # Field 13,14,15,16,17,18
print(hex_values[144:148]) # Field 19,20
print(hex_values[148:152]) # Field 21
print(hex_values[152:154]) # Field 22,23,24,25,26
print(hex_values[154:158]) # Field 27,28
print(hex_values[158:162]) # Field 29,30
print(hex_values[164:166]) # Field 32
print(hex_values[166:170]) # Field 33
print(hex_values[170:174]) # Field 34
print(hex_values[174:178]) # Field 35
#print(hex_values[178:182]) # Field 36
print(hex_values[182:480]) # Field 35