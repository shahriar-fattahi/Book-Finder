# API Style

In the **Book Finder** project, I adhere to the [Django-Styleguide by HackSoftware](https://github.com/HackSoftware/Django-Styleguide) for structuring my API, particularly when it comes to handling data serialization. The styleguide provides clear, well-defined patterns for using Django Rest Framework serializers to ensure consistency, readability, and maintainability.

## Why I Follow the Serializer Guidelines

### 1. **Explicit and Readable Serializer Logic**

According to the styleguide, I aim to keep my serializers as simple and declarative as possible. This means avoiding complex logic within serializers and focusing purely on validation and transforming data. By following this principle:

- **Clear Validation**: Validation logic is kept explicit within the serializer, allowing us to quickly see how incoming data is being validated.
- **Reduced Complexity**: Instead of mixing logic across layers, the serializer focuses solely on structuring and validating input/output data, making it easier to debug or modify.

### 2. **Use of Separate Input and Output Serializers**

A key principle in the styleguide is the use of **separate serializers for input and output**. This improves clarity by ensuring:

- **Input Serializer**: Handles incoming data validation (e.g., user-submitted reviews).
- **Output Serializer**: Formats data for API responses (e.g., displaying book details and user reviews).

By keeping these serializers separate, I maintain flexibility and clarity between what is received from users and what is returned to them. For example:

- When creating a book, an input serializer focuses only on fields needed for creation, whereas the output serializer adds additional computed fields (like the average review score).

## Serializer Practices Adopted in Book Finder

- All API views inherit from `APIView`.
- For listing or updating data, we implement custom business logic through the `get_queryset()` and `get_object()` methods.
- Since we are using Pydantic's `BaseModel` for data validation, we do not require separate output serializers (except for authentication-related APIs).
- We Have 1 API per operation. This means, for CRUD on a model, having 4 APIs. So, each API endpoint supports only one HTTP method: `GET`, `POST`, `PUT`, or `DELETE`.

## Full Example

```python
class SomeApi(APIView):
    class InputSerializer(serializers.Serializer):
        ...
    class OutputSerializer(serializers.Serializer):
        ...

    def get_queryset(self):
        ...
    def get_object(self):
        ...

    def post(self, request: Request) -> Response:
        ...
    def get(self, request: Request) -> Response:
        ...
    def put(self, request: Request) -> Response:
        ...
```
