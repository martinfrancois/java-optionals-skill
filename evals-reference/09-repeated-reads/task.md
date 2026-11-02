# Refactor card move

Assume Java 17.

Improve this method without changing behavior. Create `CardMover.java` with the revised class:

```java
import java.util.Optional;

final class CardMover {
    Card moveIfNeeded(Optional<ListRef> target, Card card) {
        if (target.isEmpty()) {
            return card;
        }
        if (card.listId().equals(target.get().id())) {
            return card;
        }
        return new Card(card.id(), target.get().id());
    }

    record Card(String id, String listId) {}
    record ListRef(String id) {}
}
```
