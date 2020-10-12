"""
https://pymotw.com/2/xml/etree/ElementTree/create.html
"""
from xml.etree import ElementTree as xet
import io
import typing as ta
import xml

from .. import dataclasses as dc
from .. import lang


class Exclusion(dc.Pure):
    group_id: str
    artifact_id: str


class Scope(lang.AutoEnum):
    COMPILE = ...
    PROVIDED = ...
    RUNTIME = ...
    TEST = ...


class Dependency(dc.Pure):
    group_id: str
    artifact_id: str
    version: str
    exclusions: ta.Optional[ta.Sequence['Exclusion']] = None
    scope: ta.Optional[Scope] = None


NestedStrMap = ta.Mapping[str, ta.Union[str, 'NestedStrMap', ta.Sequence['NestedStrMap']]]  # type: ignore


class Goal(dc.Pure):
    goal: str


class Execution(dc.Pure):
    goals: ta.Sequence[Goal]


class Plugin(dc.Pure):
    group_id: str
    artifact_id: str
    version: str
    configuration: ta.Optional[NestedStrMap] = None
    executions: ta.Optional[ta.Sequence[Execution]] = None


class Project(dc.Data):
    preamble: NestedStrMap
    properties: ta.Optional[ta.Mapping[str, str]] = None
    dependencies: ta.Optional[ta.Sequence[Dependency]] = None
    plugins: ta.Optional[ta.Sequence[Plugin]] = None


PROJECT_ATTRIBUTES = {
    'xmlns': 'http://maven.apache.org/POM/4.0.0',
    'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xsi:schemaLocation': 'http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd',
}


def build_project_tree(project: Project) -> xet.Element:
    root = xet.Element('project')

    for k, v in PROJECT_ATTRIBUTES.items():
        root.set(k, v)

    for k, v in project.preamble.items():
        child = xet.SubElement(root, k)
        child.text = v

    if project.properties:
        props = xet.SubElement(root, 'properties')
        for k, v in project.properties.items():
            child = xet.SubElement(props, k)
            child.text = v

    if project.dependencies:
        deps = xet.SubElement(root, 'dependencies')
        for dep in project.dependencies:
            child = xet.SubElement(deps, 'dependency')

            subchild = xet.SubElement(child, 'groupId')
            subchild.text = dep.group_id

            subchild = xet.SubElement(child, 'artifactId')
            subchild.text = dep.artifact_id

            if dep.version:
                subchild = xet.SubElement(child, 'version')
                subchild.text = dep.version

    if project.plugins:
        build = xet.SubElement(root, 'build')

        plgs = xet.SubElement(build, 'plugins')
        for plg in project.plugins:
            child = xet.SubElement(plgs, 'plugin')

            subchild = xet.SubElement(child, 'groupId')
            subchild.text = plg.group_id

            subchild = xet.SubElement(child, 'artifactId')
            subchild.text = plg.artifact_id

            if plg.version:
                subchild = xet.SubElement(child, 'version')
                subchild.text = plg.version

    return root


def prettify(elem: xet.Element) -> str:
    rough_string = xet.tostring(elem, 'utf-8')

    __import__('xml.dom.minidom')
    reparsed = xml.dom.minidom.parseString(rough_string)  # type: ignore

    indent = '    '
    writer = io.StringIO()

    for node in reparsed.childNodes:
        node.writexml(writer, indent, '', '\n')

    return writer.getvalue()
