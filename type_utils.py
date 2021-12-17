import re


def get_digits_from_string(string: str) -> Union[None, int, list]:
    """Get digit(s) embeded in a string

    Parameters
    ----------
    string : str
        The string to find digits in

    Returns
    -------
    Union[int, list]
        The digit(s) found in the string
    """

    digits = list(int(s) for s in re.findall(r"\d+", string))

    if len(digits) == 0:
        return None
    elif len(digits) == 1:
        return digits[0]
    else:
        return digits
