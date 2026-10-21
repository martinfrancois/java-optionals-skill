# Honor the gateway's retry hint

Create `WebhookRedelivery.java`. Assume Java 21.

A payment gateway answers a failed webhook delivery with HTTP 429 or 503 and may add a `Retry-In`
header, a whole number of seconds. The redelivery loop sleeps with `Thread.sleep(Duration)` and
then tries again. Implement:

```java
Duration pauseBefore(RetryPolicy policy, int attempt, HttpResponse<?> response)
```

Rules:

- When the response carries a `Retry-In` hint the loop can use, sleep for that long.
- Otherwise sleep for the policy's exponential backoff:
  `policy.baseDelay().multipliedBy(1L << Math.min(attempt - 1, 6))`.
- `response` may be null, for a transport failure with no response at all.
- Keep `Optional<Duration> parseRetryIn(String value)` as the place that turns the header text
  into a duration, and keep this nested record:

```java
record RetryPolicy(Duration baseDelay) {}
```
