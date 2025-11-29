from subprocess import (
    run as sp_run,
    Popen as sp_Popen
)
from os import (
    startfile as os_startfile
)
from typing import Callable

class VMControl:

    paths: dict[str, str] = {
        "powershell": "C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
        "vmconnect": "C:/Windows/System32/vmconnect.exe",
        "hyperv_manager": "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Administrative Tools/Hyper-V Manager.lnk"
    }

    @staticmethod
    def start(vm_name: str) -> None:
        sp_run([
            VMControl.paths["powershell"],
            "-Command",
            f"Start-VM -Name '{vm_name}'"
        ])

    @staticmethod
    def stop(vm_name: str) -> None:
        sp_run([
            VMControl.paths["powershell"],
            "-Command",
            f"Stop-VM -Name '{vm_name}' -TurnOff:$false"
        ])

    @staticmethod
    def kill(vm_name: str) -> None:
        sp_run([
            VMControl.paths["powershell"],
            "-Command",
            f"Stop-VM -Name '{vm_name}' -TurnOff:$true"
        ])

    @staticmethod
    def manage() -> None:
        os_startfile(VMControl.paths["hyperv_manager"])

    @staticmethod
    def open(vm_name: str) -> None:
        sp_Popen([
            VMControl.paths["vmconnect"],
            "localhost",
            vm_name
        ])

    @staticmethod
    def status(vm_name: str) -> str:
        result = sp_run(
            [
                VMControl.paths["powershell"],
                "-Command",
                f"Get-VM -Name '{vm_name}' | Select-Object -ExpandProperty State"
            ],
            capture_output=True,
            text=True
        )
        result_text_raw: str = result.stdout
        result_text: str = result_text_raw.strip()
        return result_text

commands: dict[str, Callable] = {
    "start": lambda vm_name: VMControl.start(vm_name),
    "stop": lambda vm_name: VMControl.stop(vm_name),
    "kill": lambda vm_name: VMControl.kill(vm_name),
    "manage": lambda vm_name: VMControl.manage(),
    "open": lambda vm_name: VMControl.open(vm_name),
    "status": lambda vm_name: print(VMControl.status(vm_name))
}

def main(vm_name: str) -> None:

    print(f"Hyper-V control ({vm_name})")

    while True:

        user_input_raw: str = input(">>> ")
        user_input_commands: list[str] = [i.strip() for i in user_input_raw.strip().split(" ")]

        for command in user_input_commands:

            match command:

                case "quit":
                    return

                case "switch":
                    vm_name = input("new vm name: ")
                    continue

                case _:
                    if not command in commands.keys():
                        print(f"Invalid command: \"{command}\"")
                        continue
                    commands[command](vm_name)

if __name__ == "__main__":
    main("ArchLinux")
