from stargazeutils.common import print_table


def test_print_table(capsys):
    table = [
        ["Number", "Type1", "Type2"],
        [1, "Grass", "Electric"],
        [2, "Fire", ""],
        [3, "Electric", "Flying"],
    ]

    print_table(table)
    captured = capsys.readouterr()
    lines = captured.out.split("\n")

    assert len(lines) == 5
    assert lines[0] == " | Number | Type1    | Type2   "
    assert lines[1] == " | 1      | Grass    | Electric"
    assert lines[2] == " | 2      | Fire     |         "
    assert lines[3] == " | 3      | Electric | Flying  "
    assert lines[4] == ""


def test_print_table_should_allow_custom_delimiter(capsys):
    table = [
        ["Number", "Type1", "Type2"],
        [1, "Grass", "Electric"],
    ]

    print_table(table, delimiter="")
    captured = capsys.readouterr()
    lines = captured.out.split("\n")

    assert len(lines) == 3
    assert lines[0] == "  Number  Type1  Type2   "
    assert lines[1] == "  1       Grass  Electric"
    assert lines[2] == ""


def test_print_table_should_allow_header_footer(capsys):
    table = [
        ["Number", "Type1", "Type2"],
        [1, "Grass", "Electric"],
    ]

    print_table(table, header="Hello", footer="Goodbye")
    captured = capsys.readouterr()
    lines = captured.out.split("\n")

    assert len(lines) == 5
    assert lines[0] == "Hello"
    assert lines[1] == " | Number | Type1 | Type2   "
    assert lines[2] == " | 1      | Grass | Electric"
    assert lines[3] == "Goodbye"
