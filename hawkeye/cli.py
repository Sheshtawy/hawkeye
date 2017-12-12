import argparse
from hawkeye.server import Hawkeye

def main():
    """Run the module."""
    parser = argparse.ArgumentParser(
        description='A tool for monitoring machines in an intranet.'
    )
    parser.add_argument(
        'xml_config_path', 
        help="path to xml config file for nodes you want to monitor"
    )
    args = parser.parse_args()
    xml_config = open(args.xml_config_path, 'r').read()
    hawkeye = Hawkeye(xml_config)
    hawkeye.run()

if __name__ == '__main__':
    main()
