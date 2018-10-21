import sys

def run() -> None:
    if len(sys.argv) < 2:
        print('No entry point specified.')
        sys.exit(1)

    if 'create_legal_card_list' in sys.argv:
        from database.legality_list_creator import update_legal_cards
        update_legal_cards()
    if 'decksite' in sys.argv:
        from website.main import app
        app.run()

run()
