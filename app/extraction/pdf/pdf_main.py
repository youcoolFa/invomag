from app.extraction.pdf.pdf_to_json import extract_pdf_to_json
from app.extraction.pdf.json_to_df import get_pdf_parser_for_task


def main_pdf(pdf_path, output_path, task):
    data = extract_pdf_to_json(pdf_path, output_path)
    parser = get_pdf_parser_for_task(task)
    df = parser(data)
    return df


if __name__ == "__main__":
    from app.task.task_mapping import task1_1
    task = task1_1
    pdf_path = task["pdf_path"]
    output_path = task["pdf_to_json"]
    df = main_pdf(pdf_path, output_path, task)
