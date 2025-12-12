import gradio as gr
from transformers import pipeline
import html
import json
import re

MODEL_NAME = "Darebal/vacancies_ner"

RAW_CLASSES = [
    'SKILL_HARD', 'SKILL_SOFT', 'ENGLISH_LEVEL', 'DEGREE',
    'EXPERIENCE_LEVEL', 'EXPERIENCE_YEARS', 'BENEFIT',
    'LOCATION', 'COMPANY_NAME', 'ROLE'
]

COLORS = [
    "#ff4b4b", "#4bff62", "#ffd84b", "#4b7bff",
    "#d94bff", "#4bfff0", "#ff3333", "#33cc33",
    "#ff9933", "#3366ff", "#cc33ff", "#33ffff"
]


def merge_bio_annotations(bio_annotations):
    merged = []
    current = None

    bio_annotations = sorted(bio_annotations, key=lambda x: x["start"])

    for ann in bio_annotations:
        raw_label = ann["entity"]

        if raw_label == "O":
            if current:
                merged.append(current)
                current = None
            continue

        prefix, cls = raw_label.split("-", 1)

        if prefix == "B":
            if current:
                merged.append(current)
            current = {"start": ann["start"], "end": ann["end"], "label": cls}

        elif prefix == "I":
            if current and current["label"] == cls:
                current["end"] = ann["end"]
            else:
                current = {"start": ann["start"], "end": ann["end"], "label": cls}

    if current:
        merged.append(current)

    return merged


def colorize_html(text, entities):
    label_colors = {lbl: COLORS[i % len(COLORS)] for i, lbl in enumerate(RAW_CLASSES)}

    out = text
    for ent in sorted(entities, key=lambda x: x["start"], reverse=True):
        color = label_colors.get(ent["label"], "#ffffff")
        start, end = ent["start"], ent["end"]

        out = (
            out[:start]
            + f'<span style="background-color:{color}; padding:2px; border-radius:3px;">'
            + out[start:end]
            + "</span>"
            + out[end:]
        )

    # escape HTML except spans
    out = html.escape(out, quote=False)
    out = out.replace("&lt;span", "<span").replace("&lt;/span&gt;", "</span>").replace("&gt;", ">")

    out = out.replace("  ", "&nbsp;&nbsp;")
    out = out.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
    out = out.replace("\n", "<br>")

    return out


def legend_html():
    html_code = "<h4>Legend</h4><div style='line-height:1.6;'>"
    for label, color in zip(RAW_CLASSES, COLORS):
        html_code += (
            f"<div>"
            f"<span style='display:inline-block; width:15px; height:15px; background:{color}; "
            f"border-radius:3px; margin-right:6px;'></span>"
            f"{label}"
            f"</div>"
        )
    html_code += "</div>"
    return html_code


def clean_markdown(text: str) -> str:
    text = re.sub(r'^\s*#{1,6}\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*{3,}', '', text)          
    text = re.sub(r'\*{2}([^*]+)\*{2}', r'\1', text)  
    text = re.sub(r'\*([^*]+)\*', r'\1', text)        
    text = re.sub(r'_([^_]+)_', r'\1', text)          
    text = re.sub(r'^[\t ]*[\*\-•—]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    lines = [line.strip() for line in text.splitlines()]
    cleaned = []
    prev_blank = False
    for line in lines:
        if line == "":
            if not prev_blank:
                cleaned.append("")
            prev_blank = True
        else:
            cleaned.append(line)
            prev_blank = False
    return "\n".join(cleaned).strip()


def process_text(text):
    cleaned_text = clean_markdown(text)
    if not cleaned_text.strip():
        return "", "", None
    raw = token_classifier(cleaned_text)
    merged = merge_bio_annotations(raw)
    html_out = colorize_html(cleaned_text, merged)

    data = {
        "text": cleaned_text,
        "entities": merged
    }

    return html_out, legend_html(), data


def save_labeled(data):
    if data is None:
        return None

    file_path = "labeled_output.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return file_path


def clear_all():
    return "", "", "", None


with gr.Blocks(title="Vacancies NER") as interface:

    gr.Markdown("### Paste vacancy text below")

    text_input = gr.Textbox(lines=15, label="Vacancy text")
    submit_btn = gr.Button("Submit")
    clear_btn = gr.Button("Clear All")

    with gr.Row():
        legend_box = gr.HTML()
        output_box = gr.HTML(label="NER Output")

    save_btn = gr.Button("Save Labeled Data")
    download_file = gr.File(label="Download labeled JSON")

    hidden_data = gr.State()

    submit_btn.click(
        fn=process_text,
        inputs=text_input,
        outputs=[output_box, legend_box, hidden_data]
    )

    clear_btn.click(
        fn=clear_all,
        inputs=None,
        outputs=[text_input, output_box, legend_box, hidden_data]
    )

    save_btn.click(
        fn=save_labeled,
        inputs=hidden_data,
        outputs=download_file
    )


if __name__ == '__main__':
    token_classifier = pipeline(
        "token-classification",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME
    )
    interface.launch()
