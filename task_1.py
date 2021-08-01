import os
from shutil import copy
from shutil import SameFileError, SpecialFileError, ExecError
from xmltodict import parse
from lxml import etree


def validate(xml_path: str, xsd_path: str) -> bool:
    xsd_file_name = xsd_path
    schema_root = etree.parse(xsd_file_name)
    schema = etree.XMLSchema(schema_root)

    xml_filename = xml_path
    xml = etree.parse(xml_filename)

    return schema.validate(xml)


if __name__ == "__main__":
    path = os.curdir + "/config.xml"

    try:
        with open(os.curdir + "/config.xml", "r") as xml_obj:
            xml_dict = parse(xml_obj.read())
            xml_obj.close()
    except FileNotFoundError:
        print('File is not present')
    except PermissionError:
        print('Permission denied')
    except Exception as exc:
        print(f'Error happened: {exc}')

    if any(xml_dict) and validate(path, "schema.xsd"):
        dict_config = xml_dict['config']['file']

        for d in dict_config:
            src, dst, fname = d['@sourse_path'], d['@destination_path'], d['@file_name']
            try:
                copy(src + fname, dst + fname, follow_symlinks=True)
            except SameFileError:
                print('{} and {} is the same directories'.format(src, dst))
            except SpecialFileError:
                print('Trying to do a operation which is not supported on a special file ')
            except ExecError:
                print('Command could not be executed')
            except Exception as exc:
                print(f'Error happened: {exc}')
    else:
        print('data from xml invalid')
