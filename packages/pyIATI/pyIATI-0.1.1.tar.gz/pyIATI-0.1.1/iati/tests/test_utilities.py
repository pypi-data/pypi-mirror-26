"""A module containing tests for the library implementation of accessing utilities."""
from lxml import etree
import pytest
import iati.resources
import iati.tests.utilities
import iati.utilities


class TestUtilities(object):
    """A container for tests relating to utilities."""

    @pytest.fixture
    def schema_base_tree(self):
        """Return schema_base_tree."""
        activity_schema_path = iati.resources.get_schema_path(
            iati.tests.utilities.SCHEMA_ACTIVITY_NAME_VALID
        )
        return iati.ActivitySchema(activity_schema_path)._schema_base_tree  # pylint: disable=protected-access

    def test_add_namespace_schema_new(self, schema_base_tree):
        """Check that an additional namespace can be added to a Schema.

        Todo:
            Deal with required changes to iati.constants.NSMAP.

            Add a similar test for Datasets.

        """
        initial_nsmap = schema_base_tree.getroot().nsmap
        ns_name = 'xi'
        ns_uri = 'http://www.w3.org/2001/XInclude'

        tree = iati.utilities.add_namespace(schema_base_tree, ns_name, ns_uri)
        new_nsmap = tree.getroot().nsmap

        assert len(new_nsmap) == len(initial_nsmap) + 1
        assert ns_name not in initial_nsmap
        assert ns_name in new_nsmap
        assert new_nsmap[ns_name] == ns_uri

    def test_add_namespace_schema_already_present(self, schema_base_tree):
        """Check that attempting to add a namespace that already exists changes nothing if the new URI is the same.

        Todo:
            Add a similar test for Datasets.

        """
        initial_nsmap = schema_base_tree.getroot().nsmap
        ns_name = 'xsd'
        ns_uri = 'http://www.w3.org/2001/XMLSchema'

        tree = iati.utilities.add_namespace(schema_base_tree, ns_name, ns_uri)
        new_nsmap = tree.getroot().nsmap

        assert len(new_nsmap) == len(initial_nsmap)
        assert ns_name in initial_nsmap
        assert ns_name in new_nsmap
        assert initial_nsmap[ns_name] == ns_uri
        assert new_nsmap[ns_name] == ns_uri

    def test_add_namespace_schema_already_present_diff_value(self, schema_base_tree):
        """Check that attempting to add a namespace that already exists to a Schema raises an error rather than leading to modification.

        Todo:
            Add a similar test for Datasets.

        """
        ns_name = 'xsd'
        ns_uri = 'http://www.w3.org/2001/XMLSchema-different'

        with pytest.raises(ValueError) as excinfo:
            iati.utilities.add_namespace(schema_base_tree, ns_name, ns_uri)

        assert 'There is already a namespace called' in str(excinfo.value)

    @pytest.mark.parametrize("not_a_tree", iati.tests.utilities.generate_test_types([], True))
    def test_add_namespace_no_schema(self, not_a_tree):
        """Check that attempting to add a namespace to something that isn't a Schema raises an error."""
        ns_name = 'xsd'
        ns_uri = 'http://www.w3.org/2001/XMLSchema'

        with pytest.raises(TypeError) as excinfo:
            iati.utilities.add_namespace(not_a_tree, ns_name, ns_uri)

        assert 'The `tree` parameter must be of type `etree._ElementTree` - it was of type' in str(excinfo.value)

    @pytest.mark.parametrize("ns_name", iati.tests.utilities.generate_test_types(['str'], True))
    def test_add_namespace_nsname_non_str(self, ns_name):
        """Check that attempting to add a namespace with a name that is not a string acts correctly.

        Todo:
            Determine whether to attempt cast to string or raise an error.

        """
        pass

    @pytest.mark.parametrize("ns_name", [''])
    def test_add_namespace_nsname_invalid_str(self, ns_name, schema_base_tree):
        """Check that attempting to add a namespace with a name that is an invalid string raises an appropriate error.

        Todo:
            Add more tests - for syntax, see:
                https://www.w3.org/TR/REC-xml-names/#NT-NSAttName

        """
        ns_uri = 'http://www.w3.org/2001/XMLSchema'

        with pytest.raises(ValueError) as excinfo:
            iati.utilities.add_namespace(schema_base_tree, ns_name, ns_uri)

        assert 'The `new_ns_name` parameter must be a non-empty string.' in str(excinfo.value)

    @pytest.mark.parametrize("ns_uri", iati.tests.utilities.generate_test_types(['str'], True))
    def test_add_namespace_nsuri_non_str(self, ns_uri):
        """Check that attempting to add a namespace uri that is not a string acts correctly.

        Todo:
            Determine whether to attempt cast to string or raise an error.
        """
        pass

    @pytest.mark.parametrize("ns_uri", [''])
    def test_add_namespace_nsuri_invalid_str(self, ns_uri, schema_base_tree):
        """Check that attempting to add a namespace that is an invalid string raises an appropriate error.

        Note:
            While a valid URI, an empty string is not a valid namespace - https://www.w3.org/TR/REC-xml-names/#iri-use https://www.ietf.org/rfc/rfc2396.txt

        Todo:

        """
        ns_name = 'testname'

        with pytest.raises(ValueError) as excinfo:
            iati.utilities.add_namespace(schema_base_tree, ns_name, ns_uri)

        assert 'The `new_ns_uri` parameter must be a valid URI.' in str(excinfo.value)

    def test_convert_tree_to_schema(self):
        """Check that an etree can be converted to a schema."""
        path = iati.resources.get_schema_path('iati-activities-schema')

        tree = iati.resources.load_as_tree(path)
        if not tree:  # pragma: no cover
            assert False
        schema = iati.utilities.convert_tree_to_schema(tree)

        assert isinstance(schema, etree.XMLSchema)

    def test_convert_xml_to_tree(self):
        """Check that a valid XML string can be converted to an etree."""
        xml = '<parent><child /></parent>'

        tree = iati.utilities.convert_xml_to_tree(xml)

        assert isinstance(tree, etree._Element)  # pylint: disable=protected-access
        assert tree.tag == 'parent'
        assert len(tree.getchildren()) == 1
        assert tree.getchildren()[0].tag == 'child'
        assert not tree.getchildren()[0].getchildren()

    def test_convert_xml_to_tree_invalid_str(self):
        """Check that an invalid string raises an error when an attempt is made to convert it to an etree."""
        not_xml = "this is not XML"

        with pytest.raises(etree.XMLSyntaxError) as excinfo:
            iati.utilities.convert_xml_to_tree(not_xml)

        assert excinfo.typename == 'XMLSyntaxError'

    @pytest.mark.parametrize("not_xml", iati.tests.utilities.generate_test_types(['str'], True))
    def test_convert_xml_to_tree_not_str(self, not_xml):
        """Check that an invalid string raises an error when an attempt is made to convert it to an etree."""
        with pytest.raises(ValueError) as excinfo:
            iati.utilities.convert_xml_to_tree(not_xml)

        assert 'To parse XML into a tree, the XML must be a string, not a' in str(excinfo.value)

    def test_log(self):
        """TODO: Implement testing for logging."""
        pass

    def test_log_error(self):
        """TODO: Implement testing for logging."""
        pass

    def test_log_exception(self):
        """TODO: Implement testing for logging."""
        pass

    def test_log_warning(self):
        """TODO: Implement testing for logging."""
        pass


class TestDefaultVersions(object):
    """A container for tests relating to default versions."""

    @pytest.mark.parametrize("major_version", iati.constants.STANDARD_VERSIONS_MAJOR)
    def test_versions_for_integer(self, major_version):
        """Check that the each of the decimal versions returned by versions_for_integer starts with the input major version."""
        result = iati.utilities.versions_for_integer(major_version)

        for version in result:
            assert version.startswith(str(major_version))
