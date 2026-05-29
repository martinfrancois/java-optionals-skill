# Refactor lazy Optional upsert

Use `$java-optionals` to refactor this upsert method while preserving laziness:

```java
import java.util.Optional;

final class WorkpadService {
    Result upsert(Optional<Comment> existing, String text) {
        if (existing.isPresent()) {
            return update(existing.get(), text);
        }
        return create(text);
    }

    Result update(Comment comment, String text) { return new Result("updated"); }
    Result create(String text) { return new Result("created"); }

    record Comment(String id) {}
    record Result(String status) {}
}
```
