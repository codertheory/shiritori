import pytest
from django.core.exceptions import ValidationError

from shiritori.game.models import Game, GameStatus, GameWord, Word

pytestmark = pytest.mark.django_db


def test_create_game(un_saved_game):
    assert un_saved_game.settings is None
    un_saved_game.save()
    assert un_saved_game.id is not None
    assert un_saved_game.settings is not None


def test_join_game(game, player):
    game.join(player)
    assert game.player_count == 1
    assert game.players.count() == 1
    assert game.host == player
    assert game.players.first() == player


def test_join_game_with_str(game):
    player = game.join("John")
    assert game.player_count == 1
    assert game.players.count() == 1
    assert game.host == player
    assert game.players.first() == player
    assert player.name == "John"


def test_join_started_game(started_game):
    with pytest.raises(ValidationError):
        started_game.join("John")


def test_leave_game(game, player):
    game.join(player)
    game.leave(player)
    assert game.id is None  # Instance is deleted


def test_leave_game_by_session_key(game, player):
    game.join(player)
    game.leave(player.session_key)
    assert game.id is None  # Instance is deleted


def test_host_leaving_properly_deletes_and_recalculates(started_game):
    player = started_game.players.first()
    player2 = started_game.players.last()
    player.delete()
    started_game.leave(player)
    assert started_game.host == player2
    assert started_game.player_count == 1
    assert started_game.players.first() == player2
    started_game.leave(player2)
    assert started_game.id is None


def test_start_game_with_one_player(game, player):
    game.join(player)
    with pytest.raises(ValidationError):
        game.prepare_start()


def test_start_game_with_two_players(game, player, human_player_2):
    game.join(player)
    game.join(human_player_2)
    game.prepare_start()
    game.start()
    assert game.status == GameStatus.PLAYING
    assert game.current_player == player
    assert game.current_turn == 0
    assert game.last_word is not None


def test_start_started_game(started_game):
    with pytest.raises(ValidationError):
        started_game.prepare_start()


def test_calculate_current_player(game, player, human_player_2):
    game.join(player)
    game.join(human_player_2)
    game.prepare_start()
    setup_and_assert_current_player(1, game, human_player_2)
    setup_and_assert_current_player(2, game, player)


def setup_and_assert_current_player(current_turn, game, expected_player):
    game.current_turn = current_turn
    game.calculate_current_player()
    assert game.current_player == expected_player


def test_recalculate_host_is_called_when_leaves_game(game, player, human_player_2):
    game.join(player)
    game.join(human_player_2)
    assert game.host == player
    game.leave(player)
    assert game.host == human_player_2


def test_recalculate_host_called_when_nothing_changes(game, player, human_player_2):
    game.join(player)
    assert game.host == player
    game.join(human_player_2)
    assert game.host == player
    game.recalculate_host()
    assert game.host == player
    game.recalculate_host()
    assert game.host == player


def test_recalculate_host_with_no_players(game):
    with pytest.raises(ValidationError):
        game.recalculate_host()


def test_can_current_player_take_turn(game, player, human_player_2):
    game.join(player)
    game.join(human_player_2)
    game.prepare_start()
    game.start()
    game.current_player = human_player_2
    game.turn_time_left = 10
    pytest.raises(ValidationError, game.can_take_turn, player.session_key)
    game.can_take_turn(human_player_2.session_key)


def test_can_current_player_take_turn_with_no_time_left(game, player, human_player_2):
    game.join(player)
    game.join(human_player_2)
    game.prepare_start()
    game.current_player = human_player_2
    game.turn_time_left = 0
    pytest.raises(ValidationError, game.can_take_turn, human_player_2.session_key)


def test_can_current_player_take_turn_when_game_status_is_not_playing(game, player, human_player_2):
    game.join(player)
    game.join(human_player_2)
    game.prepare_start()
    game.current_player = human_player_2
    game.turn_time_left = 10
    game.status = GameStatus.WAITING
    pytest.raises(ValidationError, game.can_take_turn, human_player_2.session_key)


def test_take_turn_with_word_non_existent_word(started_game: Game, sample_words: list[str]):
    with pytest.raises(ValidationError) as exec_info:
        started_game.turn_time_left = 10
        session_key = started_game.current_player.session_key
        started_game.take_turn(session_key, "invalid")
    assert exec_info.value.message == "Word not found in dictionary."


def test_take_turn_with_word_already_used(started_game: Game, sample_words: list[str]):
    with pytest.raises(ValidationError) as exec_info:
        started_game.turn_time_left = 10
        GameWord.objects.create(word=sample_words[0], game=started_game)
        session_key = started_game.current_player.session_key
        started_game.take_turn(session_key, sample_words[0])
    assert exec_info.value.message == "Word already used."


def test_take_turn_with_word_not_starting_with_last_word(started_game: Game, sample_words: list[str]):
    with pytest.raises(ValidationError) as exec_info:
        started_game.turn_time_left = 10
        session_key = started_game.current_player.session_key
        started_game.take_turn(session_key, sample_words[2])
    assert exec_info.value.message == "Word must start with the last letter of the previous word."


def test_take_turn_with_word_not_long_enough(started_game: Game, sample_words: list[str]):
    with pytest.raises(ValidationError) as exec_info:
        started_game.turn_time_left = 10
        session_key = started_game.current_player.session_key
        Word.objects.create(word="to")
        started_game.take_turn(session_key, "to")
    assert exec_info.value.message == "Word must be at least 3 characters long."


def test_take_turn_increments_current_round_when_last_player_takes_turn(started_game: Game, sample_words: list[str]):
    started_game.turn_time_left = 10
    first_player, next_player = started_game.players
    started_game.take_turn(first_player.session_key, sample_words[0])
    assert started_game.current_round == 0
    started_game.take_turn(next_player.session_key, sample_words[1])
    assert started_game.current_round == 1


def test_word_case_insensitive(started_game: Game, sample_words: list[str]):
    started_game.turn_time_left = 10
    session_key = started_game.current_player.session_key
    started_game.take_turn(session_key, sample_words[0].upper())
    assert started_game.last_word == sample_words[0]


def test_end_turn_updates_current_player_and_turn(started_game):
    first_player, next_player = started_game.players
    started_game.end_turn()
    assert first_player.score == -15
    assert started_game.current_player == next_player
    assert started_game.current_turn == 1


def test_finished_game_longest_word(finished_game):
    assert finished_game.longest_word.word == "toothbrush"


def test_skip_turn_updates_current_player_and_turn(started_game):
    first_player, next_player = started_game.players
    started_game.skip_turn()
    assert started_game.current_player == next_player
    started_game.skip_turn()
    assert started_game.current_player == first_player
    started_game.skip_turn()
    assert started_game.current_player == next_player


def test_restart_game(started_game):
    started_game.restart()
    assert started_game.status == GameStatus.WAITING
    assert started_game.current_turn == 0
    assert started_game.current_player is None
    assert started_game.last_word != "toothbrush"
    assert started_game.turn_time_left == 0
    assert started_game.longest_word is None
    assert started_game.players.count() == 2
    assert started_game.players.first().score == 0
    assert started_game.players.last().score == 0


def test_max_turns_calculation(started_game, player_factory):
    assert started_game.max_turns == 20
    started_game.player_set.add(player_factory())
    assert started_game.max_turns == 30
    started_game.player_set.add(player_factory())
    assert started_game.max_turns == 40
    started_game.player_set.add(player_factory())
    assert started_game.max_turns == 50


@pytest.mark.real_shuffle
def test_shuffle_player_order(started_game):
    started_game.status = GameStatus.WAITING
    first_player, next_player = started_game.players
    started_game.shuffle_player_order()
    started_game.status = GameStatus.PLAYING
    assert started_game.players.first() == next_player
    assert started_game.players.last() == first_player


@pytest.mark.real_shuffle
def test_shuffle_player_order_on_started_game_raises_validation_error(started_game):
    started_game.status = GameStatus.PLAYING
    with pytest.raises(ValidationError):
        started_game.shuffle_player_order()


@pytest.mark.real_shuffle
def test_shuffle_player_order_on_finished_game_raises_validation_error(finished_game):
    finished_game.status = GameStatus.FINISHED
    with pytest.raises(ValidationError):
        finished_game.shuffle_player_order()


@pytest.mark.real_shuffle
def test_shuffle_player_order_with_less_than_two_players(game_factory, player_factory):
    game = game_factory()
    game.player_set.add(player_factory())
    with pytest.raises(ValidationError):
        game.shuffle_player_order()


def test_player_delete_updates_current_player(started_game):
    first_player, next_player = started_game.players
    started_game.current_player = next_player
    started_game.leave(first_player)
    assert started_game.current_player == next_player
    assert started_game.players.count() == 1
    assert started_game.players.first() == next_player


def test_used_letters_returns_empty_list_when_no_words(started_game):
    # assert an empty queryset is returned
    assert started_game.used_letters.exists() is False


def test_used_letters_returns_list_of_used_letters(started_game, sample_words):
    started_game.turn_time_left = 10
    session_key = started_game.current_player.session_key
    started_game.take_turn(session_key, sample_words[0])
    assert "t" in started_game.used_letters
    assert list(started_game.used_letters) == ["t"]
