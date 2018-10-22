import sys

def run() -> None:

    if len(sys.argv) < 2:
        print('No entry point specified.')
        sys.exit(1)

    if 'update' in sys.argv:
        import database.helper
        database.helper.update_database()
    if 'update_prices' in sys.argv:
        from database.price_grabber import make_all_cards_list
        make_all_cards_list()
    if 'update_legality' in sys.argv:
        from database.legality_list_creator import update_legal_cards
        update_legal_cards()
    if 'website' in sys.argv:
        from website.main import app
        app.run(debug=True)

run()
