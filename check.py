def calculate_checksum(data):
    checksum = sum(data) & 0xFF
    return checksum

# Full command in Hex from the first row in the table
full_command_hex = "41542B52444D455445523D554C1116"

# Remove the last 2 bytes (4 hex digits)
command_hex = full_command_hex[:-4]

# Convert the command from hex to bytes
command_bytes = bytes.fromhex(command_hex)

# Calculate the checksum
checksum = calculate_checksum(command_bytes)

# Convert the checksum to hex and print
print(hex(checksum))
