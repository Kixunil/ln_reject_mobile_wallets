from estimate_mobile_wallet import is_mobile_wallet

MIN_CAPACITY_SATS = 500000
MAX_CAPACITY_SATS = 10000000

def is_capacity_in_range(request):
    return request.capacity_sats() >= MIN_CAPACITY_SATS and request.capacity_sats() <= MAX_CAPACITY_SATS

def is_channel_allowed(request):
    return is_capacity_in_range(request) and not is_mobile_wallet(request)
