def is_mobile_wallet(request):
    if request.is_public_channel():
        return False
    if request.node().public_channel_count() > 0:
        return False

    return True
