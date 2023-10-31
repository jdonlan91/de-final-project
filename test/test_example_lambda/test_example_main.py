from src.example_lambda.example_main import example_function


def test_example_function_returns_hello_world():
    assert example_function() == "Hello World"
