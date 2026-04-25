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
#  Demo tests — provided to students as examples                      #
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
#  If a test fails, you've found a bug — document it!                 #
# ------------------------------------------------------------------ #
class TestFreezeOpponent:
    def test_white_casts_freeze_opponent_is_black(self):
        """When White casts Freeze the frozen color must be BLACK."""
        game = SpellChessGame()
        assert game.current_turn() == chess.WHITE, "It should be white's turn"
        result = game.cast_freeze(chess.E5)
        assert game.current_turn() == chess.WHITE, "It should be white's turn even after casting spell"
        assert result is True, "cast_freeze should succeed on a fresh game"
        assert game.freeze_effect_color == chess.BLACK, (
            "BUG: freeze_effect_color should be BLACK (opponent) after White casts; "
            f"got {game.freeze_effect_color}"
        )

    def test_black_casts_freeze_opponent_is_white(self):
        """When Black casts Freeze the frozen color must be WHITE."""
        game = SpellChessGame()
        assert game.current_turn() == chess.WHITE, "It should be white's turn"  
        game.make_move(chess.E2, chess.E4)
        assert game.current_turn() == chess.BLACK, "It should be black's turn"
        result = game.cast_freeze(chess.E4)
        assert game.current_turn() == chess.BLACK, "It should be black's turn even after casting spell"
        assert result is True, "cast_freeze should succeed for Black on their first turn"
        assert game.freeze_effect_color == chess.WHITE, (
            "BUG: freeze_effect_color should be WHITE (opponent) after Black casts; "
            f"got {game.freeze_effect_color}"
        )

class TestFreezeSelf:
    def test_freeze_effect_color_is_not_caster_white(self):
        """After White casts, the frozen color must NOT equal WHITE (the caster)."""
        game = SpellChessGame()
        assert game.current_turn() == chess.WHITE, "It should be white's turn"
        game.cast_freeze(chess.D4)
        assert game.freeze_effect_color != chess.WHITE, (
            "BUG: freeze_effect_color must not equal the caster's color (WHITE)"
        )

    def test_freeze_effect_color_is_not_caster_black(self):
        """After Black casts, the frozen color must NOT equal BLACK (the caster)."""
        game = SpellChessGame()
        game.make_move(chess.D2, chess.D4)
        assert game.current_turn() == chess.BLACK, "It should be black's turn"
        game.cast_freeze(chess.D5)
        assert game.freeze_effect_color != chess.BLACK, (
            "BUG: freeze_effect_color must not equal the caster's color (BLACK)"
        )

class TestFreezeAreaCoversCenter:
    def test_frozen_squares_include_center(self):
        """The center square passed to cast_freeze must be in freeze_effect_squares."""
        game = SpellChessGame()
        center = chess.E5
        result = game.cast_freeze(center)
        assert result is True, "cast_freeze should succeed"
        assert center in game.freeze_effect_squares, (
            f"BUG: center square {chess.square_name(center)} should be inside "
            f"freeze_effect_squares but it is missing. "
            f"Squares found: {[chess.square_name(s) for s in game.freeze_effect_squares]}"
        )

    def test_frozen_squares_count_at_corner(self):
        """Center square on a board corner must have 4 squares in freeze_effect_squares."""
        game = SpellChessGame()
        center = chess.A1
        result = game.cast_freeze(center)
        assert result is True, "cast_freeze should succeed"
        assert len(game.freeze_effect_squares) == 4, (
            f"BUG: corner center {chess.square_name(center)} missing from freeze_effect_squares"
        )
    
    def test_frozen_squares_set_at_corner(self):
        """Center square on a board corner must have the correct 4 squares in freeze_effect_squares."""
        game = SpellChessGame()
        center = chess.A1
        expected_squares = {chess.square_name(square) for square in [chess.A1, chess.A2, chess.B1, chess.B2]}
        result = game.cast_freeze(center)
        affected_squares = {chess.square_name(s) for s in game.freeze_effect_squares}
        assert result is True, "cast_freeze should succeed"
        assert affected_squares == expected_squares, (
            f"BUG: frozen squares, {expected_squares - affected_squares} are missing from freeze_effect_squares"
        )
    
    def test_frozen_squares_count_at_edge(self):
        """Center square on a board edge must have 6 squares in freeze_effect_squares."""
        game = SpellChessGame()
        center = chess.A5
        result = game.cast_freeze(center)
        assert result is True, "cast_freeze should succeed"
        assert len(game.freeze_effect_squares) == 6, (
            f"BUG: edge center {chess.square_name(center)} missing from freeze_effect_squares"
        )
    
    def test_frozen_squares_set_at_edge(self):
        """Center square on a board edge must have the correct 6 squares in freeze_effect_squares."""
        game = SpellChessGame()
        center = chess.A5
        expected_squares = {chess.square_name(square) for square in [chess.A5, chess.A6, chess.B5, chess.B6, chess.A4, chess.B4]}
        result = game.cast_freeze(center)
        affected_squares = {chess.square_name(s) for s in game.freeze_effect_squares}
        assert result is True, "cast_freeze should succeed"
        assert affected_squares == expected_squares, (
            f"BUG: frozen squares, {expected_squares - affected_squares} are missing from freeze_effect_squares"
        )
    
    def test_frozen_squares_count_at_middle(self):
        """Center square on middle of the board must have 9 squares in freeze_effect_squares."""
        game = SpellChessGame()
        center = chess.E5
        result = game.cast_freeze(center)
        assert result is True, "cast_freeze should succeed"
        assert len(game.freeze_effect_squares) == 9, (
            f"BUG: center {chess.square_name(center)} missing from freeze_effect_squares"
        )
    
    def test_frozen_squares_set_at_middle(self):
        """Center square on a board edge must have the correct 6 squares in freeze_effect_squares."""
        game = SpellChessGame()
        center = chess.E5
        expected_squares = {chess.square_name(square) for square in [chess.E5, chess.E4, chess.F5, chess.F4, chess.D5, chess.D4, chess.E6, chess.F6, chess.D6]}
        result = game.cast_freeze(center)
        affected_squares = {chess.square_name(s) for s in game.freeze_effect_squares}
        assert result is True, "cast_freeze should succeed"
        assert affected_squares == expected_squares, (
            f"BUG: frozen squares, {expected_squares - affected_squares} are missing from freeze_effect_squares"
        )
