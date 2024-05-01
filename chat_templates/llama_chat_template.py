def get_llama_chat_template():
    return (
        "<s>"
        "{%- for message in messages -%}"
        "{%- if message.role == 'system' -%}"
        "<<SYS>>{{message.content}}<</SYS>>"
        "{%- elif message.role == 'user' -%}"
        "[INST]{{message.content}}[/INST]"
        "{%- elif message.role == 'assistant' -%}"
        "{{message.content}}"
        "{%- endif -%}"
        "{%- endfor -%}"
        "</s>"
    )

def get_llama3_chat_template():
    return (
        "<|begin_of_text|>"
        "{% for message in messages %}"
            "{% if message.role == 'system' %}"
                "<|start_header_id|>system<|end_header_id|>"
                "{{message.content}}"
                "<|eot_id|>"
            "{% endif %}"
            "{% if message.role == 'user' %}"
                "<|start_header_id|>user<|end_header_id|>"
                "{{message.content}}"
                "<|eot_id|>"
            "{% endif %}"
            "{% if message.role == 'assistant' %}"
                "<|start_header_id|>assistant<|end_header_id|>"
                "{{message.content}}"
                "<|eot_id|>"
            "{% endif %}"
        "{% endfor %}"
        "<|end_of_text|>"
    )