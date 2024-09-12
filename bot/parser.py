def parse(command):
    args = command.split(' ')
    quantity = len(args)

    if quantity == 0:
        return { 'command': None }
    
    else:
        return { 'command': args[0], 'args': (None if quantity == 1 else args[1:]), 'quantity': quantity - 1 }