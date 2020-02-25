#! /usr/bin/python3
# Author: machunning
# Email: mcnwork2018@163.com | mcnwork2018@gmail.com


import os
import shutil
import argparse
from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED

"""
    mark_sur function
    @param { string } command_path
    @param { string } input_path
    @param { string } filename
    @param { string } output_path
    @return { number } 0: success -1: fail
"""


def mark_sur(command_path, input_path, filename, output_path):
    if not os.path.exists("%s/%s_m.pdb" % (output_path, filename[0:-4])):
        try:
            shutil.copy("%s/%s" % (input_path, filename), command_path)
            os.system("cd %s && mark_sur %s %s_m.pdb" %
                      (command_path, filename, filename[0:-4]))
            os.remove("%s/%s" % (command_path, filename))
            shutil.move("%s/%s_m.pdb" %
                        (command_path, filename[0:-4]), output_path)
            mark_sur_error(output_path, "%s_m.pdb" % filename[0:-4])
        except BaseException as e:
            f = open("error.log", "a+")
            f.write("%s\n" % e)
            f.close()
        return 0
    else:
        return -1


#
"""
    mark_sur function 
    执行部分pdb不会报错但生成了一个81字节的文件, 文件会影响zdock的运行
    function_name: mark_sur_error
    @param { string } output_path
    @param { string } filename
"""


def mark_sur_error(output_path, filename):
    if os.path.getsize("%s/%s" % (output_path, filename)) == 81:
        f = open("error.log", "a+")
        f.write("[error] %s is an empty file.\n" % filename)
        f.close()
        os.remove("%s/%s" % (output_path, filename))


"""
    zdock function
    @param { string } command_path
    @param { string } input_path
    @param { string } filename
    @param { string } ligand_path
    @param { string } ligand_name
    @param { string } output_path
"""


def zdock(command_path, input_path, filename,  ligand_path, ligand_name, output_path):
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    if not os.path.exists("%s/%s_%s.out" % (output_path, filename[0:-4], ligand_name[0:-6])):
        try:
            print("%s & %s start" % (ligand_name, filename))
            os.system("%s/zdock -R %s/%s -L %s/%s -o %s/%s_%s.out"
                      % (command_path, input_path, filename, ligand_path,
                         ligand_name, output_path, filename[0:-4], ligand_name[0:-6]))
        except BaseException as e:
            f = open("error.log", "a+")
            f.write('%s\n' % e)
            f.close()
    else:
        print("%s_%s.out was created" % (filename[0:-4], ligand_name[0:-6]))


"""
    create_pl function
    @param { string } command_path
    @param { string } input_path  input file path + pdb name
    @param { string } filename    pdb_m_Ag**.out
    @param { string } output_path
"""


def create_pl(command_path, input_path, filename, output_path):
    if not os.path.exists("%s/%s" % (output_path, filename[-8:-4])):
        os.mkdir("%s/%s" % (output_path, filename[-8:-4]))
    new_path = "%s/%s/%s" % (output_path, filename[-8:-4], filename[0:-11])
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    if not os.path.exists("%s/create_lig" % new_path):
        shutil.copy("%s/create_lig" % command_path, new_path)
    if not os.path.exists("%s/%s" % (new_path, filename)):
        shutil.copy("%s/%s" % (input_path, filename), new_path)
    try:
        os.system("cd %s && %s/create.pl %s 10" %
                  (new_path, command_path, filename))
        print("create_pl %s successful!" % filename)
        os.remove("%s/create_lig" % new_path)
        os.remove("%s/%s" % (new_path, filename))
    except BaseException as e:
        f = open("error.log", "a+")
        f.write('%s\n' % e)
        f.close()


if __name__ == "__main__":
    version = "v0.9.0"
    # project root dir
    project_path = os.getcwd()
    # command file path
    command_path = "%s/command" % project_path
    # create argumentParser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-version", help="zdock_script version", action="store_true")
    parser.add_argument("-mode", type=int, help="script mode", default=0)
    parser.add_argument("-input", help="pdb input file(path)")
    parser.add_argument("-output", help="pdb output file(path)")
    parser.add_argument("-ligand", help="pdb ligand file(path)")
    parser.add_argument("-multiProcessMode", type=int,
                        help="multi process mode", default=0)

    args = parser.parse_args()

    # print script version
    if args.version:
        print("zdock batch script For Linux %s" % version)
        exit()

    # Judging if input pdb is a file or a directory
    if args.input:
        if os.path.isdir(args.input):
            input_path = {
                "path": os.path.abspath(args.input),
                "isDir": True
            }
        elif os.path.isfile(args.input):
            input_path = {
                "path": os.path.abspath(args.input),
                "isDir": False
            }
        else:
            print("ERROR: input argument could not find file or directory.")
            exit()
    else:
        print("ERROR: Please enter an input argument!")
        exit()

    # Judging the output path
    if args.output:
        if os.path.exists(args.output) and os.path.isdir(args.output):
            output_path = os.path.abspath(args.output)
        else:
            os.mkdir(args.output)
            output_path = os.path.abspath(args.output)
    else:
        output_path = project_path

    # Judging the ligand path
    if args.ligand:
        if os.path.isdir(args.ligand):
            ligand_path = {
                "path": os.path.abspath(args.ligand),
                "isDir": True
            }
        elif os.path.isfile(args.ligand):
            ligand_path = {
                "path": os.path.abspath(args.ligand),
                "isDir": False
            }
        else:
            print("ERROR: ligand argument could not find file or directory.")
            exit()
    elif args.mode == 0 or args.mode == 2:
        print("ERROR: The ligand argument is required")
        exit()

    # open process pool
    if args.multiProcessMode:
        process_pool = ProcessPoolExecutor(args.multiProcessMode)

    print("input path: %s" % input_path["path"])
    print("output path: %s" % output_path)
    print("multiProcessMode: %s" % args.multiProcessMode)

    # mode1: mark_sur all pdb
    if args.mode == 1:
        # input is a directory
        if input_path["isDir"]:
            for filename in os.listdir(input_path["path"]):
                # Do not enable multiple processes mode
                if args.multiProcessMode == 0:
                    mark_sur(command_path,
                             input_path["path"], filename, output_path)
                # multiple processes mode
                else:
                    process_pool.submit(
                        mark_sur, command_path, input_path["path"], filename, output_path)
        # input is a file
        elif not input_path["isDir"]:
            mark_sur(command_path, os.path.dirname(input_path["path"]),
                     os.path.basename(input_path["path"]), output_path)

    # mode2: zdock all pdb_m
    if args.mode == 2:
        print("ligand path: %s" % ligand_path["path"])
        # input is a directory and ligand is a directory.
        if input_path["isDir"] and ligand_path["isDir"]:
            for ligand_name in os.listdir(ligand_path["path"]):
                for filename in os.listdir(input_path["path"]):
                    # Do not enable multiple processes mode
                    if args.multiProcessMode == 0:
                        zdock(command_path, input_path["path"], filename,
                              ligand_path["path"], ligand_name,
                              "%s/%s" % (output_path, filename[0:-6]))
                    # multiple processes mode
                    else:
                        process_pool.submit(zdock, command_path, input_path["path"],
                                            filename, ligand_path["path"], ligand_name,
                                            "%s/%s" % (output_path, filename[0:-6]))
        # input is a file and ligand is a directory.
        if not input_path["isDir"] and ligand_path["isDir"]:
            for ligand_name in os.listdir(ligand_path["path"]):
                # Do not enable multiple processes mode
                if args.multiProcessMode == 0:
                    zdock(command_path, os.path.dirname(input_path["path"]),
                          os.path.basename(
                        input_path["path"]), ligand_path["path"], ligand_name,
                        "%s/%s" % (output_path, os.path.basename(input_path["path"])[0:-6]))
                # multiple processes mode
                else:
                    process_pool.submit(zdock, command_path, os.path.dirname(input_path["path"]),
                                        os.path.basename(
                                            input_path["path"]), ligand_path["path"],
                                        ligand_name, "%s/%s" % (output_path, os.path.basename(input_path["path"])[0:-6]))
        # input is a directory and ligand is a file.
        if input_path["isDir"] and not ligand_path["isDir"]:
            for filename in os.listdir(input_path["path"]):
                # Do not enable multiple processes mode
                if args.multiProcessMode == 0:
                    zdock(command_path, input_path["path"], filename,
                          os.path.dirname(ligand_path["path"]),
                          os.path.basename(ligand_path["path"]),
                          "%s/%s" % (output_path, filename[0:-6]))
                # multiple processes mode
                else:
                    process_pool.submit(zdock, command_path, input_path["path"], filename,
                                        os.path.dirname(ligand_path["path"]),
                                        os.path.basename(ligand_path["path"]),
                                        "%s/%s" % (output_path, filename[0:-6]))
        # input is a file and ligand is a file.
        if not input_path["isDir"] and not ligand_path["isDir"]:
            zdock(command_path, os.path.dirname(input_path["path"]),
                  os.path.basename(input_path["path"]),
                  os.path.dirname(ligand_path["path"]),
                  os.path.basename(ligand_path["path"]),
                  "%s/%s" % (output_path, os.path.basename(input_path["path"])[0:-6]))

    # step3: create_pl all pdb_m.out
    if args.mode == 3:
        # input is a directory
        if input_path["isDir"]:
            for dirname in os.listdir(input_path["path"]):
                for filename in os.listdir("%s/%s" % (input_path["path"], dirname)):
                    if args.multiProcessMode == 0:
                        create_pl(command_path, "%s/%s" % (input_path["path"], dirname),
                                  filename, output_path)
                    else:
                        process_pool.submit(create_pl, command_path,
                                            "%s/%s" % (input_path["path"],
                                                       dirname),
                                            filename, output_path)
        # input is a file
        if not input_path["isDir"]:
            create_pl(command_path, os.path.dirname(input_path["path"]),
                      os.path.basename(input_path["path"]), output_path)

    # step0: default mode
    # Execute mark_sur, zdock, create_pl three steps on pdb
    if args.mode == 0:
        print("ligand path: %s" % ligand_path["path"])

        mark_sur_pdb_path = "%s/mark_sur_pdb" % output_path
        if not os.path.exists(mark_sur_pdb_path):
            os.mkdir(mark_sur_pdb_path)

        zdock_pdb_path = "%s/zdock_pdb" % output_path
        if not os.path.exists(zdock_pdb_path):
            os.mkdir(zdock_pdb_path)

        create_pl_pdb = "%s/create_pl_pdb" % output_path
        if not os.path.exists(create_pl_pdb):
            os.mkdir(create_pl_pdb)

        # input is a directory
        if input_path["isDir"]:
            # mark_sur pdb
            # Do not enable multiple processes mode
            if args.multiProcessMode == 0:
                for filename in os.listdir(input_path["path"]):
                    mark_sur(command_path,
                             input_path["path"], filename, mark_sur_pdb_path)
            # multiple processes mode
            else:
                all_task = [process_pool.submit(mark_sur, command_path,
                                                input_path["path"], filename, mark_sur_pdb_path)
                            for filename in os.listdir(input_path["path"])]
                wait(all_task, return_when=ALL_COMPLETED)

            # zdock pdb
            # ligand is a directory
            if ligand_path["isDir"]:
                # Do not enable multiple processes mode
                if args.multiProcessMode == 0:
                    for ligand_name in os.listdir(ligand_path["path"]):
                        for filename in os.listdir(mark_sur_pdb_path):
                            zdock(command_path, mark_sur_pdb_path, filename,
                                  ligand_path["path"], ligand_name,
                                  "%s/%s" % (zdock_pdb_path, filename[0:-6]))
                # multiple processes mode
                else:
                    all_task = [process_pool.submit(zdock, command_path, mark_sur_pdb_path, filename,
                                                    ligand_path["path"], ligand_name,
                                                    "%s/%s" % (zdock_pdb_path, filename[0:-6]))
                                for ligand_name in os.listdir(ligand_path["path"])
                                for filename in os.listdir(mark_sur_pdb_path)]
                    wait(all_task, return_when=ALL_COMPLETED)
            # ligand is a file
            if not ligand_path["isDir"]:
                # Do not enable multiple processes mode
                if args.multiProcessMode == 0:
                    for filename in os.listdir(mark_sur_pdb_path):
                        zdock(command_path, mark_sur_pdb_path, filename,
                              os.path.dirname(ligand_path["path"]),
                              os.path.basename(ligand_path["path"]),
                              "%s/%s" % (zdock_pdb_path, filename[0:-6]))
                # multiple processes mode
                else:
                    all_task = [process_pool.submit(zdock, command_path, mark_sur_pdb_path, filename,
                                                    os.path.dirname(
                                                        ligand_path["path"]),
                                                    os.path.basename(
                                                        ligand_path["path"]),
                                                    "%s/%s" % (zdock_pdb_path, filename[0:-6]))
                                for filename in os.listdir(mark_sur_pdb_path)]
                    wait(all_task, return_when=ALL_COMPLETED)

            # create_pl pdb
            for dirname in os.listdir(zdock_pdb_path):
                for filename in os.listdir("%s/%s" % (zdock_pdb_path, dirname)):
                    if args.multiProcessMode == 0:
                        create_pl(command_path, "%s/%s" % (zdock_pdb_path, dirname),
                                  filename, create_pl_pdb)
                    else:
                        process_pool.submit(create_pl, command_path,
                                            "%s/%s" % (zdock_pdb_path,
                                                       dirname),
                                            filename, create_pl_pdb)
        # input is a file
        if not input_path["isDir"]:
            # mark_sur pdb
            mark_sur(command_path, os.path.dirname(input_path["path"]),
                     os.path.basename(input_path["path"]), mark_sur_pdb_path)
            # zdock pdb
            # ligand is a directory
            if ligand_path["isDir"]:
                # Do not enable multiple processes mode
                if args.multiProcessMode == 0:
                    for ligand_name in os.listdir(ligand_path["path"]):
                        for filename in os.listdir(mark_sur_pdb_path):
                            zdock(command_path, mark_sur_pdb_path, filename,
                                  ligand_path["path"], ligand_name,
                                  "%s/%s" % (zdock_pdb_path, filename[0:-6]))
                # multiple processes mode
                else:
                    all_task = [process_pool.submit(zdock, command_path, mark_sur_pdb_path, filename,
                                                    ligand_path["path"], ligand_name,
                                                    "%s/%s" % (zdock_pdb_path, filename[0:-6]))
                                for ligand_name in os.listdir(ligand_path["path"])
                                for filename in os.listdir(mark_sur_pdb_path)]
                    wait(all_task, return_when=ALL_COMPLETED)
            # ligand is a file
            if not ligand_path["isDir"]:
                for filename in os.listdir(mark_sur_pdb_path):
                    zdock(command_path, mark_sur_pdb_path, filename,
                          os.path.dirname(ligand_path["path"]),
                          os.path.basename(ligand_path["path"]),
                          "%s/%s" % (zdock_pdb_path, filename[0:-6]))

            # create_pl pdb
            for dirname in os.listdir(zdock_pdb_path):
                for filename in os.listdir("%s/%s" % (zdock_pdb_path, dirname)):
                    if not ligand_path["isDir"]:
                        create_pl(command_path, "%s/%s" % (zdock_pdb_path, dirname),
                                  filename, create_pl_pdb)
                    if ligand_path["isDir"]:
                        # Do not enable multiple processes mode
                        if args.multiProcessMode == 0:
                            create_pl(command_path, "%s/%s" % (zdock_pdb_path, dirname),
                                      filename, create_pl_pdb)
                        # multiple processes mode
                        else:
                            process_pool.submit(create_pl, command_path,
                                                "%s/%s" % (zdock_pdb_path,
                                                           dirname),
                                                filename, create_pl_pdb)
            # Script END
