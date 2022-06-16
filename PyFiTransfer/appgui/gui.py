import PySimpleGUI as sg

layout: list = [
    [sg.Text('PyFiTransfer')], [sg.HSeparator()],
    [
        sg.Text('Source Directory:', s=(12, 1)),
        sg.VSeperator(),
        sg.Input(key='-SourceFolderInput-'),
        sg.VSeperator(),
        sg.FolderBrowse(
            key='-SourceFolder-',
            target=(sg.ThisRow, -2),
            tooltip=
            'Browse for directory containing the files you wish to transfer.')
    ],
    [
        sg.Text('Target Directory:', s=(12, 1)),
        sg.VSeperator(),
        sg.Input(key='-TargetFolderInput-'),
        sg.VSeperator(),
        sg.FolderBrowse(
            key='-TargetFolder-',
            target=(sg.ThisRow,
                    -2),
            tooltip='Browse for target directory you wish to transfer files to.'
        )
    ],
    [
        sg.Text('File Extension:', s=(12, 1)),
        sg.VSeperator(),
        sg.Input(key='-FileExtensionInput-', expand_x=True),
    ],
    [
        sg.Multiline(s=(60, 50),
                     expand_x=True,
                     expand_y=True,
                     disabled=True,
                     key='-Logger-',
                     reroute_stdout=True,
                     write_only=True,
                     auto_refresh=True,
                     autoscroll=True)
    ], [sg.Button('Start Transfer', key='-Transfer-')], [sg.Exit()]
]

window: sg.Window = sg.Window('PyFiTransfer',
                              layout,
                              auto_size_buttons=True,
                              text_justification='c',
                              element_justification='c')
