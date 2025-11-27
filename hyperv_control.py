from subprocess import (
    run as sp_run,
    Popen as sp_Popen
)

def main(vm_name: str) -> None:

    powershell_path: str = "C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
    vmconnect_path: str = "C:/Windows/System32/vmconnect.exe"

    print(f"Hyper-V control ({vm_name})")

    while True:

        for user_input in [i.strip() for i in input(">>> ").strip().split(" ")]:

            match user_input:

                case "quit":
                    return

                case "switch":
                    vm_name = input("new vm name: ")
                    continue

                case "start":
                    sp_run(
                        [
                            powershell_path,
                            "-Command",
                            f"Start-VM -Name '{vm_name}'"
                        ]
                    )

                case "status":
                    print(
                        sp_run(
                            [
                                powershell_path,
                                "-Command",
                                f"Get-VM -Name '{vm_name}' | Select-Object -ExpandProperty State"
                            ],
                            capture_output=True,
                            text=True
                        ).stdout.strip()
                    )

                case "open":
                    sp_Popen(
                        [
                            vmconnect_path,
                            "localhost",
                            vm_name
                        ]
                    )

                case "stop":
                    sp_run(
                        [
                            powershell_path,
                            "-Command",
                            f"Stop-VM -Name '{vm_name}' -TurnOff:$false"
                        ]
                    )

                case "kill":
                    sp_run(
                        [
                            powershell_path,
                            "-Command",
                            f"Stop-VM -Name '{vm_name}' -TurnOff:$true"
                        ]
                    )

                case _:
                    print(f"Invalid input: \"{user_input}\"")

if __name__ == "__main__":
    main("ArchLinux")
