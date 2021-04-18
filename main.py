from configue import load_config_from_file

from xls_writer import XLSWriter


def main():
    config = load_config_from_file('config.yaml')
    writer: XLSWriter = config['writer']
    writer.create()
    writer.write()
    writer.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

