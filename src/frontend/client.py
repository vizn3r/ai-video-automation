import gradio as gr
from string import Template

a = "asdflkasjdflj"

def greet(name, intensity):
    temp = Template("Hello there" + name)
    return temp.substitute(a=a)

demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
)

demo.launch()