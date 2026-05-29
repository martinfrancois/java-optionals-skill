# Review proposed Optional cleanup

Use `$java-optionals` to review this proposed cleanup. Should it be accepted?

Before:

```java
import java.util.Optional;

final class UserService {
    String displayName(Optional<User> user) {
        if (user.isPresent()) {
            return user.get().displayName();
        }
        return "Anonymous";
    }

    record User(String displayName) {}
}
```

Proposed:

```java
import java.util.Optional;

final class UserService {
    String displayName(Optional<User> user) {
        User value = user.orElse(null);
        if (value != null) {
            return value.displayName();
        }
        return "Anonymous";
    }

    record User(String displayName) {}
}
```
