import random
from time import sleep

while True:
    sleep(1.0)
    prng_service = open('prng-service.txt', 'r')
    if prng_service.readline() == 'run':
        prng_output = random.randint(1, 4)
        prng_service.close()
        prng_service = open('prng-service.txt', 'w')
        prng_service.write(f"{prng_output}")
    prng_service.close()