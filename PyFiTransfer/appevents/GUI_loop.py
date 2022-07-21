from random import uniform
from time import sleep

from PyFiTransfer.appevents.events import events, exit_program, logger
from PyFiTransfer.appgui.gui import sg, window


def GUI_loop() -> None:
    """Main GUI loop.

    - Starts processing of window events.

    ---

    :return: program window
    :rtype: None
    """

    while True:
        event, vals = window.read()  # Get events from GUI window

        logger.info(f'{event} : {vals}')  # Log events

        if event in [sg.WIN_CLOSED, 'Exit']:  # Exit events
            break

        if event == '-Transfer-':  # Process Transfer button event

            # No source directory entered
            if len(vals['-SourceFolderInput-']) < 1:
                sg.Popup('Make sure all fields are filled out!')
                continue

            # No target directory entered
            if len(vals['-TargetFolderInput-']) < 1:
                sg.Popup('Make sure all fields are filled out!')
                continue

            # No file extension entered
            if len(vals['-FileExtensionInput-']) < 1:
                sg.Popup('Make sure all fields are filled out!')
                continue

            # Start Transfer
            transfer: int = events.transfer(vals['-SourceFolderInput-'],
                                            vals['-TargetFolderInput-'],
                                            vals['-FileExtensionInput-'],
                                            gui=True)
            # Progress bar
            if transfer > 0:
                # Update current progress bar value
                for _ in range(transfer):
                    sleep(uniform(0.01, 0.1))
                    window['-ProgressBar-'].update(_ + 1, transfer)
                    window.refresh()  # Update changes in window

                print(f'Successfully transferred {transfer} files!\n'
                      )  # Output success message

            window['-ProgressBar-'].update(0)  # Reset progress bar

    window.close()  # Close window and return system resources

    return exit_program.success()  # Return successful exit status
