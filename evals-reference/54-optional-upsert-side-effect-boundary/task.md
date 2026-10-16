# Clarify Optional upsert flow

Refactor `WaitingCommentSync.java`. Assume Java 17.

Return the revised Java code only.

```java
import java.util.Optional;
import java.util.logging.Logger;

final class WaitingCommentSync {
    private static final Logger LOG = Logger.getLogger(WaitingCommentSync.class.getName());

    private void upsertPrerequisiteWaitingComment(Config config, Card card, String text) {
        try {
            Optional<Comment> existing = prerequisiteWaitingComment(config, card.id());
            if (existing.map(Comment::text).filter(text::equals).isPresent()) {
                return;
            }
            existing.filter(comment -> !blank(comment.id()))
                    .ifPresentOrElse(
                            comment -> updateComment(config, comment.id(), text),
                            () -> addComment(config, card.id(), text));
        } catch (RuntimeException e) {
            LOG.warning("card_id=" + card.id() + " prerequisite_waiting_comment=failed reason=" + e.getMessage());
        }
    }

    private Optional<Comment> prerequisiteWaitingComment(Config config, String cardId) {
        return Optional.empty();
    }

    private void updateComment(Config config, String commentId, String text) {}
    private void addComment(Config config, String cardId, String text) {}
    private static boolean blank(String value) { return value == null || value.isBlank(); }

    record Config() {}
    record Card(String id) {}
    record Comment(String id, String text) {}
}
```

Preserve these outcomes: absent comment creates one; same text does nothing; different text with a
nonblank id updates; different text with a blank id creates one; runtime exceptions are logged at
the upsert boundary.

Use one Optional present/absent side-effect boundary for the existing comment, avoid
`isPresent()`/`get()`, and put the nontrivial present-comment policy in a named helper or equally
clear method boundary.
