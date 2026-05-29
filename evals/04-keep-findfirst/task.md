# Review route lookup

Use `$java-optionals` to review whether this Optional-returning lookup should change. Answer with a
short review comment.

```java
import java.util.List;
import java.util.Optional;

final class RouteSelector {
    Optional<Route> firstEnabledRoute(List<Route> routes) {
        return routes.stream()
                .filter(Route::enabled)
                .findFirst();
    }

    record Route(String name, boolean enabled) {}
}
```
