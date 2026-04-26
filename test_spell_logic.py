"""
Unit tests for Spell Chess game logic.

Run with:
    pytest test_spell_logic.py -v

These tests verify the Spell Chess rules described in SPELL_CHESS_RULES.md.
Each test creates a fresh SpellChessGame, sets up a position, performs an
action, and checks that the result matches the specification.
"""

import chess
from spell_logic import SpellChessGame, squares_in_3x3, squares_in_jump_range


# ------------------------------------------------------------------ #
#  Demo tests - provided to students as examples                      #
# ------------------------------------------------------------------ #

class TestFreezeTarget:
    """Casting Freeze should mark the opponent's color as frozen."""

    def test_freeze_affects_opponent_not_caster(self):
        game = SpellChessGame()
        # White casts freeze
        game.cast_freeze(chess.E5)
        # The frozen color should be Black (the opponent), not White
        assert game.freeze_effect_color == chess.BLACK


class TestNewGameResetsBoard:
    """Calling new_game() should bring the board back to the starting position."""

    def test_board_resets_after_moves(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.new_game()
        assert game.board.fen() == chess.STARTING_FEN


# ------------------------------------------------------------------ #
#  YOUR TESTS GO BELOW                                                #
#  Write tests that check the rules from SPELL_CHESS_RULES.md.        #
#  If a test fails, you've found a bug - document it!                 #
# ------------------------------------------------------------------ #



#  S1-T05: Tests for Freeze duration and Cooldown conditions


class TestFreezeDuration:
    """Freeze should last for exactly one opponent turn."""

    def test_freeze_expires_after_frozen_player_completes_one_move(self):
        game = SpellChessGame()

        assert game.cast_freeze(chess.E6) is True
        assert game.freeze_effect_plies_left == 1

        # White's normal move hands the turn to Black; the freeze is still active.
        assert game.make_move(chess.G1, chess.F3) is True
        assert game.current_turn() == chess.BLACK
        assert game.freeze_effect_plies_left == 1

        # After Black completes one move, the one-turn freeze must be cleared.
        assert game.make_move(chess.A7, chess.A6) is True
        assert game.current_turn() == chess.WHITE
        assert game.freeze_effect_color is None
        assert game.freeze_effect_squares == set()
        assert game.freeze_effect_plies_left == 0


class TestFreezeCooldown:
    # Freeze cooldown should decrement only at the start of the caster's turns
    def test_freeze_cooldown_counts_down_on_casters_turn_starts(self):
        game = SpellChessGame()

        assert game.cast_freeze(chess.H8) is True
        assert game.freeze_cooldown[chess.WHITE] == 3

        # Switching to Black should not reduce White's cooldown count
        assert game.make_move(chess.G1, chess.F3) is True
        assert game.current_turn() == chess.BLACK
        assert game.freeze_cooldown[chess.WHITE] == 3

        # At the start of White's next turn, cooldown should drop from 3 to 2
        assert game.make_move(chess.A7, chess.A6) is True
        assert game.current_turn() == chess.WHITE
        assert game.freeze_cooldown[chess.WHITE] == 2
        assert game.cast_freeze(chess.A1) is False

        # The following White player's turns continue the countdown: 2 to 1 to 0
        assert game.make_move(chess.B1, chess.C3) is True
        assert game.make_move(chess.B7, chess.B6) is True
        assert game.current_turn() == chess.WHITE
        assert game.freeze_cooldown[chess.WHITE] == 1
        assert game.cast_freeze(chess.A1) is False

        assert game.make_move(chess.G2, chess.G3) is True
        assert game.make_move(chess.C7, chess.C6) is True
        assert game.current_turn() == chess.WHITE
        assert game.freeze_cooldown[chess.WHITE] == 0
        assert game.cast_freeze(chess.A1) is True



#  S1-T06: Regression Tests for Freeze implementation turn-order
class TestFreezeImplementationTurnOrder:
    # Implementing freeze timing should not break normal turn flow.
    def test_normal_moves_alternate_turns_without_spell_side_effects(self):
        game = SpellChessGame()

        assert game.current_turn() == chess.WHITE
        assert game.make_move(chess.E2, chess.E4) is True
        assert game.current_turn() == chess.BLACK
        assert game.make_move(chess.E7, chess.E5) is True
        assert game.current_turn() == chess.WHITE

    def test_freeze_lifecycle_preserves_turn_order(self):
        game = SpellChessGame()

        assert game.current_turn() == chess.WHITE
        assert game.cast_freeze(chess.H8) is True
        assert game.current_turn() == chess.WHITE

        assert game.make_move(chess.G1, chess.F3) is True
        assert game.current_turn() == chess.BLACK

        assert game.make_move(chess.A7, chess.A6) is True
        assert game.current_turn() == chess.WHITE
