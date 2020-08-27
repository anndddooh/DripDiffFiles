# -*- coding: UTF-8 -*-

import PySimpleGUI as sg
import os, git, re, shutil


def drip_diff_files(repo_path, sha1, pattern, output_folder):
    try:
        repo = git.Repo(repo_path)

        # 差分のあるファイルを抽出
        diff_files = repo.git.diff('--name-only', sha1).split('\n')
        print(diff_files)

        # パターンにマッチするファイル名のファイルに絞る
        re_pattern = re.compile(pattern)
        diff_files_include_pattern = [file for file in diff_files if re_pattern.search(file)]
        print(diff_files_include_pattern)

        # 該当ファイルを指定フォルダにコピー
        for file in diff_files_include_pattern:
            src_path = os.path.join(repo_path, file)
            dst_path = os.path.join(output_folder, os.path.basename(file))
            if os.path.exists(src_path):
                shutil.copyfile(src_path, dst_path)

        return True

    except:
        return False


def gui():
    TEXT_WIDTH = 20
    TEXT_HEIGHT = 1

    VALUE_IDX_REPOSITORY_PATH = 0
    VALUE_IDX_SHA1_TO_COMPARE = 1
    VALUE_IDX_FILE_NAME_PATTERN = 2
    VALUE_IDX_OUTPUT_FOLDER = 3

    SUBMIT_TEXT = 'Go'

    layout = [
        [sg.Text('Repository path', size=(TEXT_WIDTH, TEXT_HEIGHT)),
            sg.InputText('')
        ],
        [sg.Text('First SHA-1', size=(TEXT_WIDTH, TEXT_HEIGHT)),
            sg.InputText('')
        ],
        [sg.Text('Pattern included in file name', size=(TEXT_WIDTH, TEXT_HEIGHT)),
            sg.InputText('\\.[cC]$')
        ],
        [sg.Text('Output folder', size=(TEXT_WIDTH, TEXT_HEIGHT)),
            sg.InputText('')
        ],
        [sg.Submit(button_text=SUBMIT_TEXT)]
    ]

    window = sg.Window('DripDiffFiles', layout)

    while True:
        event, values = window.read()

        if event is None:
            break

        if event == SUBMIT_TEXT:
            succeed = drip_diff_files(
                values[VALUE_IDX_REPOSITORY_PATH],
                values[VALUE_IDX_SHA1_TO_COMPARE],
                values[VALUE_IDX_FILE_NAME_PATTERN],
                values[VALUE_IDX_OUTPUT_FOLDER]
            )

            if succeed:
                sg.popup('Succeed.')
            else:
                sg.popup('Failed.')

    window.close()


if __name__ == '__main__':
    gui()