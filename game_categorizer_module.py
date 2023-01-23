import os
import openai

###########################################################
# REPLACE THIS WITH YOUR API KEY
openai.api_key = "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"
###########################################################


model: str = "text-davinci-003"  # text-ada-001     text-babbage-001      text-curie-001      text-davinci-003


def categorize_games(games, categories, guiscreen, progressbar, event, queue):
    """
    Categorize games based on the provided parameters.
    :param queue:
    :param event:
    :param progressbar:
    :param guiscreen:
    :param games:
    :param categorizedgames:
    :param categories: A list of categories to search for.
    """

    # Start the task
    totaltasks = len(categories) * len(games)
    progressbar['maximum'] = totaltasks
    progressbar['value'] = 0
    progressbar.start
    categorized_games = {}
    for category in categories:
        # check for stop
        if event.is_set():
            break

        current_category_games = []
        for game in games:
            # check for stop
            if event.is_set():
                break

            query: str = f"If this video game [{game}] " \
                         f"can fit into the [{category}] video game category" \
                         f" return 'y', else return 'n'"

            # Use API to retrieve game information
            response = openai.Completion.create(
                model=model,
                prompt=query,
                temperature=0.1,
                max_tokens=10
            )

            progressbar['value'] += 1
            guiscreen.update()

            answer: str = response['choices'][0]['text']
            answer = answer.strip()
            print("completed task " + str(progressbar['value']) + " out of " + str(totaltasks))

            if answer is str("y"):
                # print("yes")
                current_category_games.append(game)
            else:
                pass
                # print("no")

        current_category_games = {f"{category}": current_category_games}
        print(current_category_games)
        categorized_games.update(current_category_games)

    print("local: ")
    print(categorized_games)
    queue.put(categorized_games)
    print("queue: ")
    print(queue)
    return categorized_games
