from operator import itemgetter

from lxml import etree

from inxs import lib, lxml_utils, Rule, Transformation

from tests import equal_subtree, parse


wp_document = parse("""
<persons>
  <person username="JS1">
    <name>John</name>
    <family-name>Smith</family-name>
  </person>
  <person username="MI1">
    <name>Morka</name>
    <family-name>Ismincius</family-name>
  </person>
</persons>
""")


def test_wikipedia_example_1():
    expected = parse("""
        <root>
          <name username="JS1">John</name>
          <name username="MI1">Morka</name>
        </root>
    """)

    def extract_person(element):
        return element.attrib['username'], element.find('name').text

    def append_person(previous_result, result):
        lxml_utils.subelement(result, 'name', {'username': previous_result[0]},
                              text=previous_result[1])

    transformation = Transformation(
        Rule('person', (extract_person, append_person)),
        result_object='context.result', context={'result': etree.Element('root')})

    # that's five (or not counting line-breaks: nine) lines less sloc than the XSLT implementation

    assert equal_subtree(transformation(wp_document), expected)


def test_wikipedia_example_2():
    expected = parse("""
        <html xmlns="http://www.w3.org/1999/xhtml">
          <head> <title>Testing XML Example</title> </head>
          <body>
            <h1>Persons</h1>
              <ul>
                <li>Ismincius, Morka</li>
                <li>Smith, John</li>
              </ul>
          </body>
        </html>
    """)

    def generate_skeleton(context, e):
        context.persons_list = e.ul()
        context.html = e.html(
            e.head(e.title('Testing XML Example')),
            e.body(e.h1('Persons'), context.persons_list))

    def extract_person(element, persons):
        persons.append((element.find('name').text, element.find('family-name').text))

    def list_persons(previous_result, persons_list, e):
        persons_list.extend(e.li(f'{x[1]}, {x[0]}') for x in previous_result)

    transformation = Transformation(
        lib.init_elementmaker(namespace='http://www.w3.org/1999/xhtml'),
        generate_skeleton,
        Rule('person', extract_person),
        lib.sorter('persons', itemgetter(1)),
        list_persons,
        result_object='context.html', context={'persons': []})

    # that's eight (or not counting line-breaks: thirteen) lines less sloc
    # than the XSLT implementation

    assert equal_subtree(transformation(wp_document), expected)
