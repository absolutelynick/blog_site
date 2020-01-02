from django import template

register = template.Library()


@register.filter(name="chunks_of")
def chunks_of(data, chunk_sizes):
    return [data[i : i + chunk_sizes] for i in range(0, len(data), chunk_sizes)]
