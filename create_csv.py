def main(file_path: str) -> None:

    # define and apply optimizations
    optimizations: list[tuple[str, str]] = [
        ("\"", ""), # remove "
        ("\\", "/") # change \ to /
    ]

    for old, new in optimizations:
        file_path = file_path.replace(old, new)

    # file config
    encoding: str = "utf-8-sig" # leaves a signature for utf-8 encoding
    sep: str = ";"

    # create file
    with open(file_path, "w", encoding=encoding) as file:
        file.write(f"sep={sep}")

if __name__ == "__main__":
    main(input("file path: "))
