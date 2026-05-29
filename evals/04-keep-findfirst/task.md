# Review order-dependent findFirst

Use `$java-optionals` to review this method. Should `findFirst()` become `findAny()`? Answer with a
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
