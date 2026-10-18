from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import includes
from inspect_ai.solver import generate

@task
def lab_smoke():
    return Task(dataset=[Sample(input="Say hello", target="Default output")], solver=generate(), scorer=includes())
