def generate_secret(secret, modulus, steps=2000):
    for _ in range(steps):
        secret ^= (secret * 64) % modulus
        secret ^= (secret // 32) % modulus
        secret ^= (secret * 2048) % modulus
    return secret


def sum_final_secrets(secrets, modulus, steps=2000):
    return sum(generate_secret(secret, modulus, steps) for secret in secrets)


if __name__ == "__main__":
    with open("input/day22.txt") as f:
        secrets = [int(line.strip()) for line in f]
    result = sum_final_secrets(secrets, 16777216, steps=2000)
    print("Sum of the 2000th secrets is:", result)
