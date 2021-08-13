def test_find_card(client):
    response = client.get("/find-card?name=Stasis")

    # confirm response
    assert response.status_code == 200

    # confirm stasis was found
    assert response.json()["result"][0]["name"] == "Stasis"


def test_create_executable(client):
    commander = "Orcus, Prince of Undeath"
    total_lands = 0
    total_creatures = 0
    total_artifacts = 0
    total_sorcery = 0
    total_enchantments = 0
    total_walkers = 1
    total_instants = 0
    response = client.get(
        f"/build-deck?commander={commander}&total_lands={total_lands}&total_creatures={total_creatures}&total_artifacts={total_artifacts}&total_sorcery={total_sorcery}&total_walkers={total_walkers}&total_enchantments={total_enchantments}&total_instants={total_instants}"
    )
    assert response.json()["result"][0] == "Orcus, Prince of Undeath"
    assert response.json()["result"][1] == "Ob Nixilis of the Black Oath"
