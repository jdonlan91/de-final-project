from src.ingester.utils.convert_to_csv import convert_to_csv


def test_return_a_string():
    input = [{"staff_id": 1, "first_name": "Jeremie"}]
    expected = True
    assert isinstance(convert_to_csv(input), str) == expected


def test_returns_an_empty_string_when_empty_list_passed():
    assert convert_to_csv([]) == ""


def test_does_not_mutate_passed_list():
    input = [{"staff_id": 1, "first_name": "Jeremie"}]
    convert_to_csv(input)
    assert input == [{"staff_id": 1, "first_name": "Jeremie"}]


def test_converts_list_of_one_dictionary_to_csv_string():
    input = [{"staff_id": 1, "first_name": "Jeremie"}]
    expected = "staff_id,first_name\n1,Jeremie\n"
    assert convert_to_csv(input) == expected


def test_conver_list_of_mult_dictionaries_with_2_columns_to_csv_string():
    input = [
        {"staff_id": 1, "first_name": "Jeremie"},
        {"staff_id": 2, "first_name": "Peter"},
        {"staff_id": 3, "first_name": "Steve"},
        {"staff_id": 4, "first_name": "Mary"},
    ]
    expected = "staff_id,first_name\n1,Jeremie\n2,Peter\n3,Steve\n4,Mary\n"
    assert convert_to_csv(input) == expected


def test_conver_list_of_mult_dictionaries_with_mult_columns_to_csv_string():
    input = [
        {
            "staff_id": 1,
            "first_name": "Jeremie",
            "last_name": "Franey",
            "dep_id": 2,
            "email_address": "jeremie.franey@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 2,
            "first_name": "Deron",
            "last_name": "Beier",
            "dep_id": 6,
            "email_address": "deron.beier@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 3,
            "first_name": "Jeanette",
            "last_name": "Erdman",
            "dep_id": 6,
            "email_address": "jeanette.erdman@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 4,
            "first_name": "Ana",
            "last_name": "Glover",
            "dep_id": 3,
            "email_address": "ana.glover@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 5,
            "first_name": "Magdalena",
            "last_name": "Zieme",
            "dep_id": 8,
            "email_address": "magdalena.zieme@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 6,
            "first_name": "Korey",
            "last_name": "Kreiger",
            "dep_id": 3,
            "email_address": "korey.kreiger@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 7,
            "first_name": "Raphael",
            "last_name": "Rippin",
            "dep_id": 2,
            "email_address": "raphael.rippin@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 8,
            "first_name": "Oswaldo",
            "last_name": "Berg",
            "dep_id": 7,
            "email_address": "oswaldo.berg@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 9,
            "first_name": "Brody",
            "last_name": "Ratke",
            "dep_id": 2,
            "email_address": "brody.ratke@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 10,
            "first_name": "Jazmin",
            "last_name": "Kuhn",
            "dep_id": 2,
            "email_address": "jazmyn.kuhn@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 11,
            "first_name": "Meda",
            "last_name": "Cremin",
            "dep_id": 5,
            "email_address": "meda.cremin@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 12,
            "first_name": "Imani",
            "last_name": "Walker",
            "dep_id": 5,
            "email_address": "imani.walker@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 13,
            "first_name": "Stan",
            "last_name": "Lehner",
            "dep_id": 4,
            "email_address": "stan.lehner@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 14,
            "first_name": "Rob",
            "last_name": "VonRueden",
            "dep_id": 7,
            "email_address": "rob.vonrueden@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 15,
            "first_name": "Tom",
            "last_name": "Gutkowski",
            "dep_id": 3,
            "email_address": "tom.gutkowski@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 16,
            "first_name": "Jett",
            "last_name": "Parisian",
            "dep_id": 6,
            "email_address": "jett.parisian@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 17,
            "first_name": "Irving",
            "last_name": "O''Keefe",
            "dep_id": 3,
            "email_address": "irving.o''keefe@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 18,
            "first_name": "Tomasa",
            "last_name": "Moore",
            "dep_id": 8,
            "email_address": "tomasa.moore@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 19,
            "first_name": "Pierre",
            "last_name": "Sauer",
            "dep_id": 2,
            "email_address": "pierre.sauer@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
        {
            "staff_id": 20,
            "first_name": "Flavio",
            "last_name": "Kulas",
            "dep_id": 3,
            "email_address": "flavio.kulas@terrifictotes.com",
            "created_at": "2022-11-03 14:20:51.563",
        },
    ]
    expected = """staff_id,first_name,last_name,dep_id,email_address,created_at
1,Jeremie,Franey,2,jeremie.franey@terrifictotes.com,2022-11-03 14:20:51.563
2,Deron,Beier,6,deron.beier@terrifictotes.com,2022-11-03 14:20:51.563
3,Jeanette,Erdman,6,jeanette.erdman@terrifictotes.com,2022-11-03 14:20:51.563
4,Ana,Glover,3,ana.glover@terrifictotes.com,2022-11-03 14:20:51.563
5,Magdalena,Zieme,8,magdalena.zieme@terrifictotes.com,2022-11-03 14:20:51.563
6,Korey,Kreiger,3,korey.kreiger@terrifictotes.com,2022-11-03 14:20:51.563
7,Raphael,Rippin,2,raphael.rippin@terrifictotes.com,2022-11-03 14:20:51.563
8,Oswaldo,Berg,7,oswaldo.berg@terrifictotes.com,2022-11-03 14:20:51.563
9,Brody,Ratke,2,brody.ratke@terrifictotes.com,2022-11-03 14:20:51.563
10,Jazmin,Kuhn,2,jazmyn.kuhn@terrifictotes.com,2022-11-03 14:20:51.563
11,Meda,Cremin,5,meda.cremin@terrifictotes.com,2022-11-03 14:20:51.563
12,Imani,Walker,5,imani.walker@terrifictotes.com,2022-11-03 14:20:51.563
13,Stan,Lehner,4,stan.lehner@terrifictotes.com,2022-11-03 14:20:51.563
14,Rob,VonRueden,7,rob.vonrueden@terrifictotes.com,2022-11-03 14:20:51.563
15,Tom,Gutkowski,3,tom.gutkowski@terrifictotes.com,2022-11-03 14:20:51.563
16,Jett,Parisian,6,jett.parisian@terrifictotes.com,2022-11-03 14:20:51.563
17,Irving,O''Keefe,3,irving.o''keefe@terrifictotes.com,2022-11-03 14:20:51.563
18,Tomasa,Moore,8,tomasa.moore@terrifictotes.com,2022-11-03 14:20:51.563
19,Pierre,Sauer,2,pierre.sauer@terrifictotes.com,2022-11-03 14:20:51.563
20,Flavio,Kulas,3,flavio.kulas@terrifictotes.com,2022-11-03 14:20:51.563
"""
    assert convert_to_csv(input) == expected
