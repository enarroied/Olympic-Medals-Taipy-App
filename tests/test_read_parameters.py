"""Tests for src/algorithms/read_parameters.py"""

import pytest
import yaml

from algorithms.read_parameters import yaml_to_list

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestYamlToList:
    """Unit tests for yaml_to_list."""

    def test_returns_list_for_valid_yaml(self, tmp_path):
        yaml_file = tmp_path / "valid.yaml"
        yaml_file.write_text("- alpha\n- beta\n- gamma\n")
        result = yaml_to_list(yaml_file)
        assert result == ["alpha", "beta", "gamma"]

    def test_accepts_path_object(self, tmp_path):
        yaml_file = tmp_path / "path_obj.yaml"
        yaml_file.write_text("- 1\n- 2\n- 3\n")
        result = yaml_to_list(yaml_file)
        assert isinstance(result, list)
        assert result == [1, 2, 3]

    def test_accepts_string_path(self, tmp_path):
        yaml_file = tmp_path / "str_path.yaml"
        yaml_file.write_text("- x\n- y\n")
        result = yaml_to_list(str(yaml_file))
        assert result == ["x", "y"]

    def test_raises_file_not_found(self, tmp_path):
        missing = tmp_path / "does_not_exist.yaml"
        with pytest.raises(FileNotFoundError, match="was not found"):
            yaml_to_list(missing)

    def test_raises_type_error_for_dict_content(self, tmp_path):
        # yaml_to_list wraps TypeError inside a bare `except Exception`, so the
        # caller receives an Exception whose message contains the original reason.
        yaml_file = tmp_path / "dict.yaml"
        yaml_file.write_text("key: value\n")
        with pytest.raises(Exception, match="not a plain list"):
            yaml_to_list(yaml_file)

    def test_raises_type_error_for_scalar_content(self, tmp_path):
        yaml_file = tmp_path / "scalar.yaml"
        yaml_file.write_text("just_a_string\n")
        with pytest.raises(Exception, match="not a plain list"):
            yaml_to_list(yaml_file)

    def test_raises_yaml_error_for_malformed_content(self, tmp_path):
        yaml_file = tmp_path / "bad.yaml"
        yaml_file.write_text("key: [unclosed bracket\n")
        with pytest.raises(yaml.YAMLError):
            yaml_to_list(yaml_file)

    def test_empty_list_is_valid(self, tmp_path):
        yaml_file = tmp_path / "empty.yaml"
        yaml_file.write_text("[]\n")
        result = yaml_to_list(yaml_file)
        assert result == []

    def test_list_with_mixed_types(self, tmp_path):
        yaml_file = tmp_path / "mixed.yaml"
        yaml_file.write_text("- one\n- 2\n- 3.14\n")
        result = yaml_to_list(yaml_file)
        assert result == ["one", 2, 3.14]
