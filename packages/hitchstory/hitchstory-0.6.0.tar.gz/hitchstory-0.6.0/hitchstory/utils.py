from strictyaml import Regex
from re import compile


PARAM_REGEX = r"^\(\((.*?)\)\)$"


YAML_Param = Regex(PARAM_REGEX)


def is_parameter(text):
    """
    Is the chunk of YAML data passed to us a parameter?

    i.e. like so (( parametername ))
    """
    return isinstance(text, str) and compile(PARAM_REGEX).match(text) is not None


def parameter_name(text):
    """
    Return parameter name from parameter text.

    e.g. (( param_name )) -> "param_name"
    """
    return compile(PARAM_REGEX).match(text).group(1).strip()


def to_underscore_style(text):
    """Changes "Something like this" to "something_like_this"."""
    text = text.lower().replace(" ", "_").replace("-", "_")
    return ''.join(x for x in text if x.isalpha() or x.isdigit() or x == "_")


def replace_parameter(thing, param_name, param):
    """
    Replace parameter name in (( and )) with value in step arguments and preconditions.
    """
    if type(thing) is str:
        if "(( {0} ))".format(param_name) in str(thing):
            return thing.replace("(( {0} ))".format(str(param_name)), str(param))
        else:
            return thing
    else:
        if type(thing) is list:
            new_thing = []

            for i, item in enumerate(thing):
                new_thing.append(replace_parameter(item, param_name, param))

            return new_thing
        elif type(thing) is dict:
            new_thing = {}

            for key, value in thing.items():
                new_thing[key] = replace_parameter(value, param_name, param)

            return new_thing
        else:
            return thing
