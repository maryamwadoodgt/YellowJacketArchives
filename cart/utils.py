def calculate_total_items(cart, movies_in_cart):
    """Return total number of items in the cart (sum of quantities)."""
    total = 0
    for movie in movies_in_cart:
        quantity = cart[str(movie.id)]
        total += int(quantity)
    return total