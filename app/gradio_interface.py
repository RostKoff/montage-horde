import gradio as gr
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import process_request

def gradio_app():
    with gr.Blocks() as app:
        with gr.Group(visible=True) as form_section:
            gr.Markdown("## Upload Files and Enter a Prompt")
            with gr.Row():
                file_input = gr.File(
                    label="Upload Video/Audio Files",
                    file_types=["video", "audio"],
                    file_count="multiple",
                )
                prompt_input = gr.Textbox(
                    label="Enter Prompt",
                    placeholder="What would you like to do?",
                )
            submit_button = gr.Button("Submit")
        
        with gr.Group(visible=False) as results_section:
            gr.Markdown("## Results and Feedback")
            result_output = gr.Textbox(
                label="Results", interactive=False
            )
            download_file = gr.File(
                label="Download Processed Files",
                interactive=True
            )
            feedback_prompt = gr.Textbox(
                label="Refine Prompt",
                placeholder="If not satisfied, provide additional instructions here.",
            )
            refine_button = gr.Button("Refine Request")
            back_button = gr.Button("Start New Request")

        def process_and_update(files, prompt):
            (result, zipped_file) = asyncio.run(process_request(files, prompt))
            output = result.messages[-1].content
            return (
                gr.update(visible=False),
                gr.update(value=zipped_file, visible=True),
                gr.update(visible=True),
                gr.update(value=result.messages[-1].content) 
            )

        def refine_request(new_prompt):
            output_files = asyncio.run(process_request([], new_prompt))

            if output_files is None:
                output_files = []

            if isinstance(output_files, str):
                output_files = [output_files]

            zip_file_path = os.path.abspath('app/work_dir/output/generate_test.zip')
            output_files.append(zip_file_path)

            return gr.update(value=zip_file_path)  

        submit_button.click(
            process_and_update,
            inputs=[file_input, prompt_input],
            outputs=[form_section, download_file, results_section, result_output],
        )

        refine_button.click(
            refine_request,
            inputs=feedback_prompt,
            outputs=download_file,
        )

        def go_back_to_form():
            return (
                gr.update(visible=True),
                gr.update(visible=False),
            )

        back_button.click(
            go_back_to_form,
            inputs=[],
            outputs=[form_section, results_section],
        )

    return app

if __name__ == "__main__":
    gradio_app().launch()


