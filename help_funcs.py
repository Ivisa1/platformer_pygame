def clamp(value, low, high):
    """
    Возвращает число, заключенное между нижней и верхней границей
    """
    if low > high:
        a = low
        low = high
        high = a
    return max(low, min(value, high))