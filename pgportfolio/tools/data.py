def get_volume_forward(time_span, portion, portion_reserved):
    volume_forward = 0
    if not portion_reserved:
        volume_forward = time_span * portion
    return volume_forward
