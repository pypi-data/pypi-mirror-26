import re

import jinja2
import six
import yaml as pyyaml
from yaql.language import exceptions as yaql_exc
from yaql.language import factory


def _find_line(match, contents):

    for lineno, line in enumerate(contents.splitlines(), start=1):
        if match in line:
            return lineno


def description(path, string, yaml):
    """Verify that Workbooks and Workflows have descriptions"""

    if 'workflows' not in yaml:
        yield "Probably not a workbook. Not supported. {}".format(path)
        raise StopIteration

    W101 = "W101: Workbook {} has no description"
    W102 = "W102: Workflow {}.{} has no description"

    workbook = yaml['name']

    if 'description' not in yaml:
        yield W101.format(workbook)

    for workflow, struct in yaml['workflows'].items():
        if 'description' not in struct:
            yield W102.format(workbook, workflow)


def type_(path, string, yaml):
    """Check that type 'direct' isn't specified as it isn't needed"""

    if 'workflows' not in yaml:
        yield "Probably not a workbook. Not supported. {}".format(path)
        return

    W103 = ("W103: Type 'direct' is the default and can be removed from "
            "Workflow {}.{}")

    workbook = yaml['name']
    for workflow, struct in yaml['workflows'].items():
        if struct.get('type') == "direct":
            yield W103.format(workbook, workflow)


def inputs(path, string, yaml):
    """Check that the workflow inputs are used"""

    if 'workflows' not in yaml:
        yield "Probably not a workbook. Not supported. {}".format(path)
        return

    E101 = "E101: Input {} is not used in Workflow {}.{}"

    workbook = yaml['name']
    for workflow, struct in yaml['workflows'].items():

        inputs = struct.get('input')
        if not inputs:
            continue

        for i in inputs:
            i = next(iter(i.keys())) if not isinstance(i, str) else i
            if i not in pyyaml.dump(struct.get('tasks')):
                yield E101.format(i, workbook, workflow)


def _check_exists(task, key, names):

    ENGINE_COMMANDS = ["fail", "pause", "succeed"]

    task_list = task.get(key)

    if not task_list:
        return

    E102 = "E102: Call to task {} in {} which isn't found"

    if isinstance(task_list, str):
        task_list = task_list.split(' ', 1)[0]
        if task_list not in names:
            if task_list in ENGINE_COMMANDS:
                return
            yield E102.format(task_list, key)
    elif isinstance(task_list, (list, dict)):
        for task in task_list:
            if isinstance(task, dict):
                task = next(iter(task.keys()))
            if task in ENGINE_COMMANDS:
                continue
            if task not in names:
                yield E102.format(task, key)
    else:
        raise Exception(task_list)


def tasks(path, string, yaml):
    """Check that all tasks exist"""

    if 'workflows' not in yaml:
        yield "Probably not a workbook. Not supported. {}".format(path)
        return

    for workflow_name, workflow in yaml['workflows'].items():

        tasks = list(workflow['tasks'].keys())

        for task_name, task in workflow['tasks'].items():
            _check_exists(task, 'on-success', tasks)
            _check_exists(task, 'on-error', tasks)
            _check_exists(task, 'on-complete', tasks)


def _find_strings(value):
    if value is None or isinstance(value, int):
        pass
    elif isinstance(value, six.string_types):
        yield value
    elif isinstance(value, list):
        for thing in value:
            for s in _find_strings(thing):
                yield s
    elif isinstance(value, dict):
        for k, v in value.items():
            for s in _find_strings(k):
                yield s
            for s in _find_strings(v):
                yield s
    else:
        raise Exception(type(value))


def _find_key(value, key):
    if isinstance(value, list):
        for item in value:
            for r in _find_key(item, key):
                yield r
    if isinstance(value, dict):
        for k, v in value.items():
            if k == key and isinstance(v, dict):
                for tk, tv in v.items():
                    yield tk, tv
            else:
                for r in _find_key(v, key):
                    yield r


def _find_workflows(value):
    for workflow_name, workflow_value in _find_key(value, "workflows"):
        yield workflow_name, workflow_value


def _find_tasks(value):
    for task_name, task_value in _find_key(value, "tasks"):
        yield task_name, task_value


def task_names(path, string, yaml):

    W104 = ("W104: task '{0}' should reference itself with task() and not "
            "include its own name line task({0}). In workflow {1}")

    for workflow_name, workflow_value in _find_workflows(yaml):
        for task_name, task_value in _find_tasks(workflow_value):
            for string in _find_strings(task_value):
                if "task({})".format(task_name) in string:
                    yield W104.format(task_name, workflow_name)


# These are copied from Mistral. That is bad.
JINJA_REGEXP = re.compile('({{(.*)}})')
JINJA_BLOCK_REGEXP = re.compile('({%(.*)%})')
YAQL_REGEXP = re.compile('<%.*?%>')


def _validate_jinja2(template, string, path):
    try:
        env = jinja2.Environment()
        env.parse(string)
    except jinja2.TemplateError:
        lineno = _find_line(template, string)
        return ("E104: Failed to parse jinja2 expression '{}' on line {} in {}"
                .format(template, lineno, path))


YAQL_ENGINE = factory.YaqlFactory().create()


def _validate_yaql(template, string, path):
    try:
        for found in YAQL_REGEXP.findall(template):
            YAQL_ENGINE(found.strip("<%>"))
    except (yaql_exc.YaqlException, KeyError, ValueError, TypeError):
        lineno = _find_line(template, string)
        return ("E105: Failed to parse yaql expression '{}' on line {} in {}"
                .format(template, lineno, path))


def expressions(path, string, yaml):

    for expr in _find_strings(yaml):
        E103 = "E103: Expression brackets don't match '{}' on line {} in {}"

        if expr.count("<%") != expr.count("%>"):
            lineno = _find_line(expr, string)
            yield E103.format(expr, lineno, path)
        elif expr.count("{{") != expr.count("}}"):
            lineno = _find_line(expr, string)
            yield E103.format(expr, lineno, path)
        elif JINJA_REGEXP.search(expr) or JINJA_BLOCK_REGEXP.search(expr):
            yield _validate_jinja2(expr, string, path)
        elif YAQL_REGEXP.search(expr):
            yield _validate_yaql(expr, string, path)
