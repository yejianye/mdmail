import re
import six

def sanitize_email_address(address):
    if address is None:
        return None

    if isinstance(address, (list, tuple)):
        return [sanitize_email_address(a) for a in address]

    if ',' in address:
        return sanitize_email_address(address.split(','))

    address = address.strip()

    match = re.match('^(.*)<(.*)>$', address)
    if match:
        name, address = match.groups()
        return name.strip(), address.strip()
    else:
        return address

def is_string(val):
    return isinstance(val, six.string_types)

def to_bool(val):
    if is_string(val):
        return val.lower() in ('1', 'true', 'yes', 'y')
    return bool(val)
