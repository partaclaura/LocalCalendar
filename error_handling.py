
def handle_exceptions(exception, exception_message):
    try:
        raise exception(exception_message)
    except exception as e:
        print("Error: ", e)
