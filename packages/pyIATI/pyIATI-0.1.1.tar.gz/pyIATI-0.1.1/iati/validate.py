"""A module containing validation functionality.

Warning:
    It is planned to change from Schema-based to Data-based Codelist validation. As such, this module will change significantly.
"""
# pylint: disable=unused-argument


def is_valid(dataset, schema):
    """Determine whether a given Dataset is valid against the specified Schema.

    Args:
        dataset (iati.Dataset): The Dataset to check validity of.
        schema (iati.Schema): The Schema to validate the Dataset against.

    Warning:
        Parameters are likely to change in some manner.

    Todo:
        Consider if functionality should take account of differences between iati.Schema, iati.ActivtySchema and iati.OrganisationSchema

    """
    raise NotImplementedError
