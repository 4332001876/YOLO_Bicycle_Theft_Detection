from server.server_pipeline import ServerPipeline
from server.config import TOP_K

import gradio as gr
import pandas as pd


class QuerySystemBackend:
    def __init__(self, server_pipeline: ServerPipeline):
        self.server_pipeline = server_pipeline
        self.top_k = TOP_K
        self.page = self.build_page()

    def build_page(self):
        
        with gr.Blocks() as page:
            gr.Markdown("# Bicycle Re-ID")
            gr.Markdown("Input a picture of your bicycle to find its recent location.")
            
            # self.top_k = gr.Slider(5, 50, value=TOP_K, step=1, label="Number of query results")

            
            with gr.Row():
                image_input = gr.Image()
            
            image_button = gr.Button("Query")

            ui_content=[]
            for _ in range(self.top_k):
                with gr.Row():
                    image_output = gr.Image(type="filepath", label=None)
                    ui_content.append(image_output)
                    table_output = gr.DataFrame(type="pandas", label=None)
                    ui_content.append(table_output)



            #with gr.Accordion("See Details"):
                #gr.Markdown("lorem ipsum")
                
            
            image_button.click(fn=self.server_pipeline.query_img, inputs=image_input, outputs=ui_content, api_name="greet")

            
        return page

    def launch(self):
        self.page.launch()

    
    
