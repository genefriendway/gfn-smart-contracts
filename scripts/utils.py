
def assert_equal(value1, value2, title):
    if value1 == value2:
        print(f'=> [OK] {title}: {value1} = {value2}')
    else:
        print(f'=> [FAILED] {title}: {value1} # {value2}')