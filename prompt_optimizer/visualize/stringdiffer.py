from difflib import ndiff
class StringDiffer:
    def __init__(self):
        pass
    def __call__(self, original: str, optimized: str) -> None:
        original = str(original)
        optimized = str(optimized)
        diff = list(ndiff(original, optimized))
        output = ""
        for op, _, value in diff:
            if op == "-":
                output += f"\033[91m{value}\033[0m"
            elif op == "+":
                output += f"\033[92m{value}\033[0m"
            else:
                output += value
        print(output)