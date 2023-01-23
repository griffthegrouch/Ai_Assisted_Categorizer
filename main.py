import game_categorizer_module as game_categorizer
import game_categorizer_UI as ui

# Intial Commit 23/01/2023
# Griffin Atkinson

###########################################################
# git repo does NOT include a working OpenAI API key"
# to use the program yourself, go into "game_categorizer_module.py"
# and replace the API key at the top of the page with your own
# the program will then use that key for requests
# API keys are available for free on OpenAI's website, and you can get free credits when you first open an account
###########################################################

# TODO

def main():
    # Initialize the UI
    root = ui.GameCategorizerUI()
    # Start the UI event loop
    root.root.mainloop()

if __name__ == "__main__":
    main()
