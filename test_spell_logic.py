"""
Unit tests for Spell Chess game logic.

Run with:
    pytest test_spell_logic.py -v

These tests verify the Spell Chess rules described in SPELL_CHESS_RULES.md.
Each test creates a fresh SpellChessGame, sets up a position, performs an
action, and checks that the result matches the specification.
"""

from pyclbr import Class

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

class TestFreezeArea:
    def test_frozen_squares_count_at_corner(self):
        """Center square on a board corner must have 4 squares in freeze_effect_squares."""
        game = SpellChessGame()
        center = chess.A1
        result = game.cast_freeze(center)
        assert result is True, "cast_freeze should succeed"
        assert len(game.freeze_effect_squares) == 4, (
            f"BUG: corner center {chess.square_name(center)} missing from freeze_effect_squares"
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
    
    def test_frozen_squares_count_at_middle(self):
        """Center square on middle of the board must have 9 squares in freeze_effect_squares."""
        game = SpellChessGame()
        center = chess.E5
        result = game.cast_freeze(center)
        assert result is True, "cast_freeze should succeed"
        assert len(game.freeze_effect_squares) == 9, (
            f"BUG: center {chess.square_name(center)} missing from freeze_effect_squares"
        )

class TestFreezeValidSquares:
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

class TestJumpSpellValidity:

    def test_jump_spell_initial_charges(self):
        """At the start of the game, both players should have 3 Jump charges."""
        game = SpellChessGame()
        assert game.jump_remaining[chess.WHITE] == 3, "BUG: White should start with 3 Jump charges"
        assert game.jump_remaining[chess.BLACK] == 3, "BUG: Black should start with 3 Jump charges"

    def test_jump_spells_after_1_use(self):
        """After using a Jump spell, a player should have 2 Jump charges remaining."""
        game = SpellChessGame()
        if game.cast_jump(chess.E5, chess.F5):
            assert game.jump_remaining[chess.WHITE] == 2, "BUG: White should have 2 Jump charges after using one"
    
    def test_jump_spells_after_2_uses(self):
        """After using a Jump spell twice, a player should have 1 Jump charge remaining."""
        game = SpellChessGame()
        if game.cast_jump(chess.E5, chess.F5):
            if game.cast_jump(chess.E4, chess.F4):
                assert game.jump_remaining[chess.WHITE] == 1, "BUG: White should have 1 Jump charge after using two"

    def test_jump_spells_after_3_uses(self):
        """After using a Jump spell three times, a player should have 0 Jump charges remaining."""
        game = SpellChessGame()
        if game.cast_jump(chess.E5, chess.F5):
            if game.cast_jump(chess.E4, chess.F4):
                if game.cast_jump(chess.D5, chess.C5):
                    assert game.jump_remaining[chess.WHITE] == 0, "BUG: White should have 0 Jump charges after using three"

    def test_jump_spell_no_charges_left(self):
        """If a player has no Jump charges left, cast_jump should return False."""
        game = SpellChessGame()
        # Use all 3 Jump charges
        game.cast_jump(chess.E5, chess.F5)
        game.cast_jump(chess.E4, chess.F4)
        game.cast_jump(chess.D5, chess.C5)
        # Try to use a 4th Jump spell
        result = game.cast_jump(chess.D4, chess.C4)
        assert result is False, "BUG: cast_jump should return False when no Jump charges are left"

    def test_jump_spell_once_per_turn(self):
        """A player should only be able to cast one Jump spell per turn."""
        game = SpellChessGame()
        # Try to cast a Jump spell
        result1 = game.cast_jump(chess.D1, chess.D3)
        assert result1 is True, "BUG: First cast_jump should succeed"
        # Try to cast a second Jump spell in the same turn
        result2 = game.cast_jump(chess.H1, chess.H3)
        assert result2 is False, "BUG: Second cast_jump in the same turn should fail"

    def test_jump_spell_after_move(self):
        """After making a normal move, a player should not be able to cast a Jump spell."""
        game = SpellChessGame()
        # initial_turn = game.current_turn()
        game.make_move(chess.E2, chess.E4)
        assert game.cast_jump(chess.E2, chess.E4) is False, "BUG: Spell should not be castable after a player has made a normal move"

    def test_jump_spell_after_different_move(self):
        """After making a normal move, a player should not be able to cast a Jump spell, even if the move is different."""
        game = SpellChessGame()
        game.make_move(chess.E2, chess.E4)
        assert game.cast_jump(chess.D1, chess.D3) is False, "BUG: Spell should not be castable after a player has made a normal move, even if the move is different"

    def test_jump_spell_before_move(self):
        """Before making a normal move, a player should be able to cast a Jump spell."""
        game = SpellChessGame()
        # Try to cast a Jump spell before making a normal move
        result = game.cast_jump(chess.A1, chess.A3)
        assert result is True, "BUG: cast_jump should succeed before making a normal move"

    def test_jump_spell_player_piece_only(self):
        """A player should only be able to cast a Jump spell on their own pieces."""
        game = SpellChessGame()
        # Try to jump an opponent's piece
        result = game.cast_jump(chess.E7, chess.E5)  
        assert result is False, "BUG: cast_jump should fail when trying to jump an opponent's piece"
    
    def test_jump_spell_jump_from_empty_square(self):
        """A player should not be able to cast a Jump spell from an empty square."""
        game = SpellChessGame()
        # Try to jump from an empty square
        result = game.cast_jump(chess.D4, chess.D6)
        assert result is False, "BUG: cast_jump should fail when trying to jump from an empty square"

    def test_jump_spell_jump_to_same_square(self):
        """A player should not be able to cast a Jump spell to the same square."""
        game = SpellChessGame()
        # Try to jump to the same square
        result = game.cast_jump(chess.E2, chess.E2)  
        assert result is False, "BUG: cast_jump should fail when trying to jump to the same square"

    def test_jump_spell_jump_king(self):
        """A player should not be able to cast a Jump spell on their own king."""
        game = SpellChessGame()
        # Try to jump the player's own king
        result = game.cast_jump(chess.E1, chess.E3)  
        assert result is False, "BUG: cast_jump should fail when trying to jump the player's own king"
    
    def test_jump_spell_jump_to_occupied_square(self):
        """A player should not be able to cast a Jump spell to a square that is already occupied."""
        game = SpellChessGame()
        # Try to jump to an occupied square
        result = game.cast_jump(chess.D1, chess.B1)  
        assert result is False, "BUG: cast_jump should fail when trying to jump to an occupied square"

    def test_jump_spell_2_squares_away(self):
        """A player should only be able to cast a Jump spell to a square that is within Chebyshev distance 2 away in any direction."""
        game = SpellChessGame()
        # Try to jump to a square that is not 2 squares away
        result = game.cast_jump(chess.C1, chess.F4)  
        assert result is False, "BUG: cast_jump should fail when trying to jump to a square that is not within Chebyshev distance 2 away"
    
    def test_jump_spell_upper_bound(self):
        """A player should only be able to cast a Jump spell to a square that is within Chebyshev distance 2 away in any direction."""
        game = SpellChessGame()
        # Try to jump to a square that is within Chebyshev distance 2 away
        result = game.cast_jump(chess.A1, chess.A5)
        assert result is False, "BUG: cast_jump should fail when trying to jump to a square that is not within Chebyshev distance 2 away"
        
        
        # Allows jumps to squares that are exactly 3 squares away but does not allow jumps to squares that are 4 or more squares away.