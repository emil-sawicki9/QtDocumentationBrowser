import re
import json
from xml.etree import ElementTree

import requests

from documentation_processing.constant import QT_BASE_URL


class QtItemHtmlParser:
    _title = ""
    _description = {}
    _function_descriptions = {}
    _current_url = ""
    _function_table = {}
    _description_table = {}

    # Parsed object keys
    LINKS = "links"
    TITLE = "title"
    NAME = "name"
    RETURN = "return"
    DESCRIPTION = "description"
    TEXT = "text"
    ACCESS_LINK = "access_link"
    IS_PROPERTY = "is_property"
    EXTENDED = "extended"
    SIMPLE = "simple"

    def parse_qt_item(self, url):
        self.clear()
        self._current_url = url
        html = requests.get(url).text
        html = self._remove_from_string('gcse:', html)
        if len(html) > 0:
            root = ElementTree.fromstring(html)
            context = self._get_element(root, './/*[@class="context"]')
            if context is not None:
                _title = self._get_element_text(context, './/*[@class="title"]')
                print(f'Parsing: {_title}')
                self._parse_function_descriptions(context)
                self._parse_description(context)
                # self._parse_description_table(context)
                # self._parse_properties(context)
                # self._parse_function_table(context, "public-functions")
                # self._parse_function_table(context, "signals")
                # self._parse_function_table(context, "protected-functions")
                print(json.dumps(self._description, indent=4, sort_keys=True))

        # TODO prepare data object
        data = {}
        return data

    def clear(self):
        self._title = ""
        self._description = {}
        self._function_descriptions = {}
        self._current_url = ""
        self._function_table = {}
        self._description_table = {}

    def _parse_properties(self, root):
        pass

    def _parse_function_table(self, root, function_type):
        if root is None:
            return
        table_data_list = []
        children = root.getchildren()
        idx = 0
        table_xml = None
        for child in children:
            if child.tag == 'h2' and child.attrib['id'] == function_type:
                table_xml = children[idx+1]
                break
            idx += 1
        if table_xml is not None:
            rows = table_xml.findall('./table/tr')
            for row in rows:
                columns = row.findall('./td')
                if columns:
                    function_data = {self.RETURN: columns[0].text, self.NAME: ''.join(columns[1].itertext())}
                    link = columns[1].find('.//a')
                    if link is not None:
                        function_data[self.DESCRIPTION] = self._get_function_description(link.attrib['href'].split('#')[1])
                    table_data_list.append(function_data)
        self._function_table[function_type] = table_data_list

    def _parse_function_descriptions(self, root):
        function_xml = self._get_element(root, './/*[@class="func"]')
        if function_xml is not None:
            self._parse_function_descriptions_inner(function_xml.getchildren())
        prop_xml = self._get_element(root, './/*[@class="prop"]')
        if prop_xml is not None:
            self._parse_function_descriptions_inner(prop_xml.getchildren())

    def _parse_function_descriptions_inner(self, items):
        current_data = {}
        current_text = ""
        current_parsed_name = ""
        for item in items:
            # Found function tag
            if item.tag == 'h3' and item.attrib['class'] == 'fn':
                self._parse_function_description_add(current_parsed_name, current_text, current_data)
                current_parsed_name = item.attrib['id']
                current_text = ""
                current_data = {self.TITLE: {self.TEXT: ''.join(item.itertext())}}
                # Updating links to types
                self._find_and_add_links(current_data[self.TITLE], item)
                if self.LINKS in current_data[self.TITLE]:
                    # Link to currently parsed property has no text
                    title_links = current_data[self.TITLE][self.LINKS]
                    if None in title_links:
                        title_links[self.ACCESS_LINK] = title_links[None]
                        del title_links[None]
            elif len(current_parsed_name) > 0:
                # Parsing function description
                if item.tag == 'p':
                    current_text += ''.join(item.itertext()) + "\n\n"
                    # Updating links to other properties
                    self._find_and_add_links(current_data, item)
                # Parsing tables
                elif item.tag == 'div' and item.attrib['class'] == 'table':
                    current_text += ''.join(item.itertext())
        self._parse_function_description_add(current_parsed_name, current_text, current_data)

    def _parse_function_description_add(self, name, text, data):
        if len(name) > 0:
            data[self.TEXT] = text
            is_property = name.endswith("-prop")
            if is_property:
                name = name[0:-5]
            data[self.IS_PROPERTY] = is_property
            self._function_descriptions[name] = data

    def _parse_description_table(self, root):
        table_data = {}
        table_xml = self._get_element(root, './/*[@class="table"]')
        if table_xml:
            rows = table_xml.findall('./table/tr')
            for row in rows:
                columns = row.findall('./td')
                if len(columns) > 0:
                    left_column_text = columns[0].text
                    right_column = columns[1]
                    right_column_children = right_column.getchildren()
                    if len(right_column_children) > 0:
                        column_content_xml = right_column_children[0]
                        if column_content_xml.tag == "p":
                            item_list = []
                            for link in column_content_xml.getchildren():
                                item_list.append(self._format_element_text(link))
                            right_column_text = ", ".join(item_list)
                        else:
                            right_column_text = self._format_element_text(column_content_xml)
                    else:
                        right_column_text = right_column.text
                    table_data[left_column_text] = right_column_text
        self._description_table = table_data

    def _parse_description(self, root):
        description_paragraphs = [self._get_element_text(root, './/p')]
        advanced_description_xml = self._get_element(root, './/*[@class="descr"]')
        if advanced_description_xml is not None:
            # TODO parse extended description, e.g. https://doc.qt.io/qt-5/qabstractitemmodel.html
            self._description[self.EXTENDED] = {}
            self._find_and_add_links(self._description[self.EXTENDED], advanced_description_xml, True)
        self._description[self.SIMPLE] = "\n".join(description_paragraphs)

    def _find_and_add_links(self, data, item, skip_none=False):
        if self.LINKS not in data:
            data[self.LINKS] = {}
        for child in item.iter("a"):
            if child.text is None and skip_none:
                continue
            if 'href' in child.attrib:
                link = child.attrib['href']
                if link.startswith('#'):
                    data[self.LINKS][child.text] = self._current_url + link
                else:
                    data[self.LINKS][child.text] = QT_BASE_URL + link

    def _get_function_description(self, name):
        if name in self._function_descriptions:
            return self._function_descriptions[name]
        else:
            return ""

    def _remove_from_string(self, rem, my_string):
        return re.sub(".*" + rem + ".*\n?", "", my_string)

    def _get_element(self, root, query):
        result = root.findall(query)
        if len(result) > 0:
            return result[0]
        else:
            return None

    def _format_element_text(self, element):
        if element is None:
            return ""
        if element.tag == "a":
            # TODO handle base url
            return "(" + element.text + ")[" + element.attrib['href'] + "]"
        else:
            return element.text

    def _get_element_text(self, root, query):
        element = self._get_element(root, query)
        if element is not None:
            return element.text
        else:
            return ""
