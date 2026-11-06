from functools import reduce

ONES = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
to_fahrenheit = lambda c: round(c * 9 / 5 + 32, 1)

def summary(temps, threshold):
    fahrenheit = list(map(to_fahrenheit, temps))
    over_limit = list(filter(lambda t: t >= threshold, temps))
    total = reduce(lambda a, b: a + b, temps)
    highest = reduce(lambda a, b: a if a > b else b, temps)
    average = total / len(temps)
    return {"fahrenheit": fahrenheit, "over_limit": over_limit, "total": round(total, 1), "max": highest, "average": round(average, 1)}

def in_words(number):
    if number < 20:
        return ONES[number]
    if number == 100:
        return "One Hundred"
    if number % 10 == 0:
        return TENS[number // 10]
    return TENS[number // 10] + "-" + ONES[number % 10]
