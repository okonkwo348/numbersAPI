from django.http import JsonResponse
import requests
import math

# Helper functions
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    return n > 0 and sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

def get_fun_fact(n):
    url = f"http://numbersapi.com/{n}/math?json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("text", "No fun fact available.")
    except requests.RequestException:
        return "No fun fact available."

# Main API view
def classify_number(request):
    number = request.GET.get("number", None)
    if not number:
        return JsonResponse({"error": True, "message": "No number provided."}, status=400)
    try:
        number = int(number)
    except ValueError:
        return JsonResponse({"error": True, "message": "Invalid number."}, status=400)

    is_armstrong_flag = is_armstrong(number)
    properties = ["armstrong" if is_armstrong_flag else None, "odd" if number % 2 != 0 else "even"]
    properties = [prop for prop in properties if prop is not None]  # Remove None values

    # Constructing custom fun_fact for Armstrong numbers
    if is_armstrong_flag:
        digits = [int(d) for d in str(number)]
        power = len(digits)
        armstrong_calc = " + ".join(f"{d}^{power}" for d in digits)
        fun_fact = f"{number} is an Armstrong number because {armstrong_calc} = {number} //gotten from the numbers API"
    else:
        fun_fact = get_fun_fact(number)

    response_data = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum":f"{ sum(int(d) for d in str(number))} // sum of its digits",
        "fun_fact": fun_fact,
    }

    return JsonResponse(response_data, status=200)
