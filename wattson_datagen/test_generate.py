from wattson_datagen.generate import generate_data_py


def test_generate_data() -> None:
    # Generate code...
    code = generate_data_py()
    # ... and check that it's valid Python.
    assert compile(code, "test_generate_data.py", "exec")
