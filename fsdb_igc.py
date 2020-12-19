# !/usr/bin/env python
#
import lxml.etree as ET
import os, argparse
import shutil


def main(args):

    if not os.path.isfile(args.file):
        print("fsdb file does not exist")
        exit()

    path = os.path.dirname(args.file)

    try:
        tree = ET.parse(args.file)
    except TypeError:
        tree = ET.parse(args.file.as_posix())
    except ET.Error:
        print("FSDB Read Error.")
        return None
    finally:
        root = tree.getroot()

    participants = root.xpath('FsCompetition/FsParticipants')
    tasks = root.xpath('FsCompetition/FsTasks')
    pilots = {}
    for participant in participants[0]:
        pilots[participant.attrib.get('id')] = participant.attrib.get('name')
    print(pilots)

    destination = os.path.join(path, "output")
    if not os.path.exists(destination):
        os.makedirs(destination)

    for task in tasks[0]:
        source_dir = task.get('tracklog_folder')
        print(task.get('name'))
        task_destination = os.path.join(destination, source_dir)
        if not os.path.exists(task_destination):
            os.makedirs(task_destination)
        source = None
        if dir:
            source = os.path.join(path, source_dir)
        if not os.path.isdir(source):
            print(f"{source} does not exist. Skipping")
            continue
        task_participants = task.xpath('FsParticipants')

        for participant in task_participants[0]:
            pil_id = participant.get('id')
            name = pilots[str(pil_id)].replace(" ", "_") + "_" + str(pil_id)
            if participant.xpath('FsFlightData'):
                tracklog = participant.xpath('FsFlightData')[0].get('tracklog_filename')
                if tracklog:
                    print(f'pil_id={pil_id} name={name} tracklog={tracklog}')
                    if len(tracklog) > 5:
                        _, extension = os.path.splitext(tracklog)
                        out = os.path.join(task_destination, name + extension)
                        if not os.path.isfile(os.path.join(source, tracklog)):
                            print(f"{tracklog} does not exist. Skipping")
                            continue
                        shutil.copy2(os.path.join(source, tracklog), out)
                else:
                    print(f"{name} does not have a tracklog in fsdb file.")
        shutil.make_archive(os.path.join(destination, source_dir), 'zip', task_destination)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Reads a fsdb file and copies the igc files that have been used in the file to a new folder"
                    " renaming them firstname_lastname.igc where the name is the name of the pilot."
                    "The source igc files should be located in sub dirs to the location of the fsdb. The dirs should "
                    "be named as they are in the fsdb",)

    parser.add_argument(
        # "-f"
        "file",
        help="The fsdb file to process.",
    )
    args = parser.parse_args()
    main(args)
