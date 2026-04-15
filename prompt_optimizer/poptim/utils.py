from typing import Any, Callable, List, Tuple
class DotDict(dict):
    def __getattr__(self, attr: str) -> Any:
        if attr in self:
            return self[attr]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{attr}'"
        )
    def __setattr__(self, attr: str, value: Any) -> None:
        self[attr] = value
class ParseError(Exception):
    def __init__(self, message: str, prompt: str) -> None:
        super().__init__(message)
        self.prompt = prompt
    def __str__(self) -> str:
        return f"ParseError: {self.args[0]} in `Prompt`: {self.prompt}"
def parse_protect_tags(prompt: str, protect_tag: str) -> Tuple[List[str], List[str]]:
    protect_start_tag = f"<{protect_tag}>"
    protect_end_tag = f"</{protect_tag}>"
    chunks = []
    protected_chunks = []
    stack = []
    start_idx = 0
    for i in range(len(prompt)):
        if prompt[i : i + len(protect_start_tag)] == protect_start_tag:
            if len(stack) != 0:
                raise ParseError("Nested ignore tags not allowed", prompt)
            stack.append(i)
            chunks.append(prompt[start_idx:i])
        elif prompt[i : i + len(protect_end_tag)] == protect_end_tag:
            start_idx = i + len(protect_end_tag)
            if len(stack) == 0:
                raise ParseError(
                    f"Invalid protect tag sequence. {protect_end_tag} must follow an unclosed {protect_start_tag}",
                    prompt,
                )
            protect_start_index = stack.pop()
            protect_content = prompt[protect_start_index + len(protect_start_tag) : i]
            protected_chunks.append(protect_content)
            if protect_content.startswith(
                protect_start_tag
            ) or protect_content.endswith(protect_end_tag):
                raise ParseError("Invalid protect tag sequence.", prompt)
    if len(stack) > 0:
        raise ParseError(
            f"All {protect_start_tag} must be followed by a corresponding {protect_end_tag}",
            prompt,
        )
    chunks.append(prompt[start_idx:])
    assert (
        len(chunks) == len(protected_chunks) + 1
    ), f"Invalid tag parsing for string: {prompt}"
    return chunks, protected_chunks
def protected_runner(run: Callable) -> Callable:
    def run_in_chunks(obj: object, prompt: str, *args, **kwargs) -> str:
        protect_tag = obj.protect_tag
        opti_prompt = ""
        if protect_tag is not None:
            chunks, protected_chunks = parse_protect_tags(prompt, protect_tag)
            protected_chunks.append("")
            for i, chunk in enumerate(chunks):
                if len(chunk):
                    opti_chunk = run(obj, chunk, *args, **kwargs)
                else:
                    opti_chunk = ""
                opti_prompt += opti_chunk + protected_chunks[i]
        elif len(prompt):
            opti_prompt = run(obj, prompt, *args, **kwargs)
        else:
            opti_prompt = prompt
        return opti_prompt
    return run_in_chunks