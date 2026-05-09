from config import REPORT_OUTPUT

def generate_report(analysis):
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gap Analysis Results</title>
    </head>
    <body>
        <h1>Gap Analysis Results</h1>
        <p>Data:</p>
        <pre>{analysis}</pre>
    </body>
    </html>
    '''

    with open(REPORT_OUTPUT, "w") as file:
        file.write(html_content)
