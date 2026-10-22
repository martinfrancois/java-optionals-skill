# Refactor display name

Assume Java 17.

Improve this Java code without changing behavior. Create `UserService.java` with the revised class:

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
