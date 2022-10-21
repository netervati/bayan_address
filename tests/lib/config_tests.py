# import pytest
# from bayan_address.lib.config import Immutable


# class ImmutableTesterClass(Immutable):
#     def __init__(self) -> None:
#         self.test_key = "Sample Value"
#         super().__init__()


# def test_immutable():
#     subject = ImmutableTesterClass()

#     with pytest.raises(AttributeError):
#         subject.test_key = True

#     with pytest.raises(AttributeError):
#         del subject.test_key
