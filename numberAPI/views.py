import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def classify_number(request):
    number = request.GET.get('number')

    # Input validation
    if not number or not number.lstrip('-').isdigit():
        return JsonResponse({
            "number": number if number else "null",
            "error": True
        }, status=400)

    number = int(number)
    is_prime = check_prime(number)
    is_perfect = check_perfect(number)
    is_armstrong = check_armstrong(number)
    digit_sum = sum(int(digit) for digit in str(abs(number)))
    parity = "even" if number % 2 == 0 else "odd"

    # Fetch fun fact
    fun_fact = get_fun_fact(number)

    # Determine properties
    properties = []
    if is_armstrong:
        properties.append("armstrong")
    properties.append(parity)

    return JsonResponse({
        "number": number,
        "is_prime": is_prime,
        "is_perfect": is_perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    })

def check_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def check_perfect(n):
    if n < 2:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def check_armstrong(n):
    digits = [int(d) for d in str(abs(n))]
    length = len(digits)
    return sum(d**length for d in digits) == n

def get_fun_fact(n):
    # Check if the number is an Armstrong number
    if check_armstrong(n):
        digits = [int(d) for d in str(abs(n))]
        length = len(digits)
        fact = f"{n} is an Armstrong number because "
        fact += " + ".join(f"{d}^{length}" for d in digits)
        fact += f" = {n}"
        return fact

    # Fetch fun fact from Numbers API for non-Armstrong numbers
    url = f"http://numbersapi.com/{n}/math"
    response = requests.get(url)
    return response.text if response.status_code == 200 else "No fun fact available."
