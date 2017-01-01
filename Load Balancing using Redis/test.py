def outer():
    message = "Hello World!"

    def inner():
        print message
    return inner

a = outer()  # a is equal to the inner function ready to be executed

