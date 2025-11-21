from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.conf import settings

from yandex.service  import YandexGpt
from yandex.service import GPTError

from .models import Node
from .forms import ParentNodeForm


def main(request):

    form = ParentNodeForm()

    # создаем корневой узел
    if request.method == 'POST':
        form = ParentNodeForm(request.POST)

        if form.is_valid():
            Node.objects.create(name=form.cleaned_data['name'])
            form = ParentNodeForm()

    # получили корневые узлы
    nodes = Node.objects.filter(level=0).order_by('level', '-id')

    return render(request, 'main.html', {'nodes': nodes, 'form': form})


@require_POST
def add_node(request, node_id):

    first_node = get_object_or_404(Node, id=node_id)

    # находим последнее слово в цепочке
    if first_node.get_descendants():
        parent_node = first_node.get_descendants().order_by('level').last()
    else:
        parent_node = first_node
    print(parent_node)

    # получаем ассоциацию
    try:
        # берем всю цепочку, чтобы не нейросеть не повторялась 
        exclude = ",".join(first_node.get_descendants().values_list('name', flat=True))

        yandex_gpt = YandexGpt(settings.YANDEX_API_KEY, settings.YANDEX_CATALOG)
        word = yandex_gpt.get_association(parent_node.name, exclude)
    except GPTError as e:

        errors = f'Ошибка: {e}'
        nodes = Node.objects.filter(level=0).order_by('level', '-id')
        form = ParentNodeForm()

        return render(request, 'main.html', {'nodes': nodes, 'form': form, 'errors': errors})
    
    # добавляем слово
    Node.objects.create(parent=parent_node, name=word)

    return redirect('/')