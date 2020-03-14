from django import template

register = template.Library()

@register.simple_tag
def question_bank_search_filter(value_arg):
    string_value = "?"
    for key, value in value_arg.items():
        if key != "page":
            if len(value_arg.dict().items()) > 1:
                string_value += "{arg_value_key}={arg_value}".format(arg_value_key=key, arg_value=value)
                string_value += "&"
            else:
                string_value += "{arg_value_key}={arg_value}".format(arg_value_key=key, arg_value=value)
                string_value += "&"
    return string_value[:-1]


@register.filter
def index(indexable, i):
    return indexable[i]["batch__label"]