# import pytest
# from bayan_address.lib.utils import clean_str, concat_str, is_valid_str, replace_str


# @pytest.mark.parametrize(
#     ["arg", "result"],
#     [
#         ("Bayan", "bayan"),
#         ("BAYAN", "bayan"),
#         ("Bayan Address", "bayan address"),
#         (" Bayan Address ", "bayan address"),
#         (" Bayan  Address ", "bayan  address"),
#     ],
# )
# def test_clear_str(arg, result):
#     assert clean_str(arg) == result


# @pytest.mark.parametrize(
#     ["arg1", "arg2", "result"],
#     [
#         ("Sta.", "Anna", "Sta. Anna"),
#         (" Brgy.", "barrio ", "Brgy. barrio"),
#     ],
# )
# def test_concat_str(arg1, arg2, result):
#     assert concat_str(arg1, arg2) == result


# @pytest.mark.parametrize(
#     ["arg", "result"],
#     [
#         (True, False),
#         (1, False),
#         ({}, False),
#         ("", False),
#         ("Valid String", True),
#     ],
# )
# def test_is_valid_str(arg, result):
#     assert is_valid_str(arg) == result


# @pytest.mark.parametrize(
#     ["arg1", "arg2", "result"],
#     [
#         (",", "Test, with comma", "Test with comma"),
#         ("mid", "Sample Mid City", "Sample  City"),
#     ],
# )
# def test_is_replace_str(arg1, arg2, result):
#     assert replace_str(arg1, arg2) == result
