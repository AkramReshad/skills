from pathlib import Path

INSTRUCTIONS = (
    "After writing the notes, run Prettier with --write on the note files you created or updated, "
    "using the workspace's Prettier configuration."
)


def speaker(message):
    role = message["role"].upper()
    author = message.get("author")
    return f"{role} ({author})" if author else role


def conversation_text(conversation):
    return "\n\n".join(f"{speaker(message)}:\n{message['text']}" for message in conversation)


class NoteChanges:
    def __init__(self, cwd, activity, count_source):
        self.cwd = Path(cwd)
        self.notes_dir = self.cwd / "notes"
        self.activity = activity
        self.paths = {"add": set(), "update": set(), "delete": set()}
        activity.update(phase="writing_notes", count_source=count_source, created_count=0,
                        created_notes=[], modified_notes=[], deleted_notes=[])

    def record(self, kind, path):
        path = (self.cwd / path).resolve()
        if path.suffix != ".md" or not path.is_relative_to(self.notes_dir):
            return
        self.paths[kind].add(str(path))
        self.activity.update(created_count=len(self.paths["add"]), created_notes=sorted(self.paths["add"]),
                             modified_notes=sorted(self.paths["update"]), deleted_notes=sorted(self.paths["delete"]))

    @property
    def created_count(self):
        return len(self.paths["add"])
