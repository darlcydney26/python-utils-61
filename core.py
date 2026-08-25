def is_valid_input(value):
    if isinstance(value, str):
        try:
            val = int(value.strip())
            return val > 0
        except ValueError:
            return False
    return isinstance(value, int) and value > 0

def process_data(inputs):
    results = []
    i = 0
    while i < len(inputs):
        item = inputs[i]
        if not is_valid_input(item):
            i += 1
            continue
        num = int(item) if isinstance(item, str) else item
        def is_prime_like(n):
            if n < 2:
                return False
            for k in range(2, int(n**0.5) + 1):
                if n % k == 0:
                    return False
            return True
        if is_prime_like(num):
            processed_value = num * 2
        else:
            processed_value = num + 10
        results.append(processed_value)
        i += 1
    return results

if __name__ == "__main__":
    test_inputs = [3, "7", "4", 11, "abc", "2", 13, "1", 17]
    processed = process_data(test_inputs)
    print(processed)