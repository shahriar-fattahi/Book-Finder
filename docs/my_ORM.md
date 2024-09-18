# My ORM and Queries

Since we couldn't use Django's ORM in this project, I used Pydantic models to handle and validate data at the Python level. The models are defined in the `schemas.py` file within each app and use type hints to manage data effectively.

Example:

```python
class Book(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(max_length=255)
    author: str = Field(max_length=255)
    genre: str = Field(max_length=255)
    reviews: List[Review] = Field(default=[])

    objects: ClassVar["BookManager"] = BookManager(db_table_name="books")

    def __str__(self) -> str:
        return self.title
```

As shown above, each model has an `objects` property, which is a manager responsible for handling raw database queries. All CRUD operations are performed through this manager.

Each manager inherits from a base manager, which is an abstract class. This base class includes functions that every model must customize to fit its specific requirements.

in `config/database.py`:

```python
class BaseModelManager(ABC):
    """
    An interface through which database query operations are provided to Pydantic models.
    At least one Manager exists for every model.
    """

    def __init__(self, db_table_name: str) -> None:
        self.table = db_table_name

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def all(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass
```
