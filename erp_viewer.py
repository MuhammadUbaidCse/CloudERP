import sys
from pathlib import Path

import webview


def main():
    if len(sys.argv) < 2:
        print('Usage: erp_viewer.py <path to html file>')
        sys.exit(1)

    html_path = Path(sys.argv[1])
    if not html_path.exists():
        raise FileNotFoundError(f'ERP HTML file not found: {html_path}')

    url = html_path.absolute().as_uri()
    window = webview.create_window('CloudBase ERP Page', url, width=1200, height=800, resizable=True)
    webview.start()


if __name__ == '__main__':
    main()
