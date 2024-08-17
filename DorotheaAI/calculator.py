def calculate(query):
    """
    Function to calculate basic mathematical expressions
    """
    # Convert the input query to a string
    term = str(query)

    # Replace specific words with mathematical operators
    term = term.replace("dorothea", "")
    term = term.replace("multiply", "*")
    term = term.replace("plus", "+")
    term = term.replace("minus", "-")
    term = term.replace("divided", "/")

    try:
        # Evaluate the mathematical expression
        result = eval(term)
        return result

    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."

    except Exception as e:
        return f"Error: Invalid input. {e}"

