from PyFiTransfer.appevents.events import Events, exprogram, logger
from PyFiTransfer.appgui.gui import sg, window


def GUI_loop() -> None:
    while True:
        event, vals = window.read()

        logger.info(f'{event} : {vals}')

        if event in [sg.WIN_X_EVENT, sg.WIN_CLOSED, 'Exit']:
            break

        if event == '-Transfer-':
            if len(vals['-SourceFolderInput-']) < 1:
                sg.Popup('Make sure all fields are filled out!')
                continue
            if len(vals['-TargetFolderInput-']) < 1:
                sg.Popup('Make sure all fields are filled out!')
                continue
            if len(vals['-FileExtensionInput-']) < 1:
                sg.Popup('Make sure all fields are filled out!')
                continue
            Events.transfer(vals['-SourceFolderInput-'],
                            vals['-TargetFolderInput-'],
                            vals['-FileExtensionInput-'])

    window.close()

    return exprogram.success()
