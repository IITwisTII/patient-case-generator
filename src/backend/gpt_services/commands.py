

def diagnosis_command(input):
    match(input):
        case "@":
            return True;
    return False;

def test_command(input):
    match(input):
        case "!":
            return True;
    return False;
