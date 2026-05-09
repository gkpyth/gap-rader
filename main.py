from gap_analyzer import *
from report_generator import generate_report


analysis = analyze(setup_client(), get_content())

generate_report(analysis)