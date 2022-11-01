def main():
    all_ids = []
    with open("./USC_outs/USC_out_ALL.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line and line != "":
                all_ids.append(set(list(map(int, line.split("{")[1][:-1].split(", ")))))

    print(all_ids)
    for index, i in enumerate(all_ids):
        with open(f"./USC_outs/USC_out_PARSED_{index}.txt", "w") as file:
            for j in i:
                file.write(f"https://en.wikipedia.org/?curid={j}\n")
if __name__ == "__main__":
    main()