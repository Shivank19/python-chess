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

class TestCenterSquareIncluded:
        """The center square itself must always be in the result."""

        def test_center_included_for_every_square(self):
            failures = [
                chess.square_name(sq)
                for sq in chess.SQUARES
                if sq not in squares_in_3x3(sq)
            ]
            assert failures == [], f"Center missing for: {failures}"

        def test_center_corner_a1(self):
            assert chess.A1 in squares_in_3x3(chess.A1)

        def test_center_corner_h1(self):
            assert chess.H1 in squares_in_3x3(chess.H1)

        def test_center_corner_a8(self):
            assert chess.A8 in squares_in_3x3(chess.A8)

        def test_center_corner_h8(self):
            assert chess.H8 in squares_in_3x3(chess.H8)

        def test_center_left_edge(self):
            assert chess.A4 in squares_in_3x3(chess.A4)

        def test_center_right_edge(self):
            assert chess.H5 in squares_in_3x3(chess.H5)

        def test_center_bottom_edge(self):
            assert chess.E1 in squares_in_3x3(chess.E1)

        def test_center_top_edge(self):
            assert chess.E8 in squares_in_3x3(chess.E8)


class TestSquareCount:
    """Mid-board → 9, edge → 6, corner → 4."""

    def test_midboard_e4(self):
        assert len(squares_in_3x3(chess.E4)) == 9

    def test_midboard_d5(self):
        assert len(squares_in_3x3(chess.D5)) == 9

    def test_left_edge_a4(self):
        assert len(squares_in_3x3(chess.A4)) == 6

    def test_right_edge_h5(self):
        assert len(squares_in_3x3(chess.H5)) == 6

    def test_bottom_edge_e1(self):
        assert len(squares_in_3x3(chess.E1)) == 6

    def test_top_edge_e8(self):
        assert len(squares_in_3x3(chess.E8)) == 6

    def test_corner_a1(self):
        assert len(squares_in_3x3(chess.A1)) == 4

    def test_corner_h1(self):
        assert len(squares_in_3x3(chess.H1)) == 4

    def test_corner_a8(self):
        assert len(squares_in_3x3(chess.A8)) == 4

    def test_corner_h8(self):
        assert len(squares_in_3x3(chess.H8)) == 4


class TestExactMembership:
    """Exact set checks — no missing squares, no extra squares."""

    def test_a1_exact(self):
        assert squares_in_3x3(chess.A1) == {chess.A1, chess.B1, chess.A2, chess.B2}

    def test_h1_exact(self):
        assert squares_in_3x3(chess.H1) == {chess.G1, chess.H1, chess.G2, chess.H2}

    def test_a8_exact(self):
        assert squares_in_3x3(chess.A8) == {chess.A7, chess.B7, chess.A8, chess.B8}

    def test_h8_exact(self):
        assert squares_in_3x3(chess.H8) == {chess.G7, chess.H7, chess.G8, chess.H8}

    def test_a4_exact(self):
        assert squares_in_3x3(chess.A4) == {
            chess.A3, chess.B3, chess.A4, chess.B4, chess.A5, chess.B5
        }

    def test_e1_exact(self):
        assert squares_in_3x3(chess.E1) == {
            chess.D1, chess.E1, chess.F1, chess.D2, chess.E2, chess.F2
        }

    def test_e8_exact(self):
        assert squares_in_3x3(chess.E8) == {
            chess.D7, chess.E7, chess.F7, chess.D8, chess.E8, chess.F8
        }

    def test_exact_match_all_64_squares(self):
        def expected(sq):
            cf, cr = chess.square_file(sq), chess.square_rank(sq)
            return {
                chess.square(cf + df, cr + dr)
                for df in (-1, 0, 1) for dr in (-1, 0, 1)
                if 0 <= cf + df < 8 and 0 <= cr + dr < 8
            }
        failures = []
        for sq in chess.SQUARES:
            got, want = squares_in_3x3(sq), expected(sq)
            if got != want:
                failures.append(
                    f"{chess.square_name(sq)}: missing={[chess.square_name(s) for s in want - got]}"
                )
        assert failures == [], "Mismatches:\n" + "\n".join(failures)

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


#  S1-T05: Tests for Freeze duration and Cooldown conditions


class TestFreezeDuration:
    # Freeze should last for exactly one opponent turn.

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


class TestJumpSpellValidity:

    def test_jump_spell_initial_charges(self):
        """At the start of the game, both players should have 3 Jump charges."""
        game = SpellChessGame()
        assert game.jump_remaining[chess.WHITE] == 3, "BUG: White should start with 3 Jump charges"
        assert game.jump_remaining[chess.BLACK] == 3, "BUG: Black should start with 3 Jump charges"

    def test_jump_spells_after_1_use(self):
        """After using a Jump spell, a player should have 2 Jump charges remaining."""
        game = SpellChessGame()
        ok = game.cast_jump(chess.E2, chess.E3)
        assert ok is True
        assert game.jump_remaining[chess.WHITE] == 2, "BUG: White should have 2 Jump charges after using one"
    
    def test_jump_spells_after_2_uses(self):
        """After using a Jump spell twice, a player should have 1 Jump charge remaining."""
        game = SpellChessGame()
        if game.cast_jump(chess.E2, chess.F5):
            if game.cast_jump(chess.E4, chess.F4):
                assert game.jump_remaining[chess.WHITE] == 1, "BUG: White should have 1 Jump charge after using two"

    def test_jump_spells_after_3_uses(self):
        """After using a Jump spell three times, a player should have 0 Jump charges remaining."""
        game = SpellChessGame()
        if game.cast_jump(chess.E2, chess.F5):
            if game.cast_jump(chess.E4, chess.F4):
                if game.cast_jump(chess.D5, chess.C5):
                    assert game.jump_remaining[chess.WHITE] == 0, "BUG: White should have 0 Jump charges after using three"

    def test_jump_spell_no_charges_left(self):
        """If a player has no Jump charges left, cast_jump should return False."""
        game = SpellChessGame()
        # Use all 3 Jump charges
        game.cast_jump(chess.E2, chess.E4)
        game.cast_jump(chess.A2, chess.A4)
        game.cast_jump(chess.D2, chess.D4)
        # Try to use a 4th Jump spell
        result = game.cast_jump(chess.C2, chess.C4)
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
        ok = game.make_move(chess.A1, chess.A3)  # Make a normal move after casting the Jump spell
        assert ok is True, "BUG: Normal move should succeed after casting a Jump spell"

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


class TestGameResets:

    def test_new_game_resets_board(self):
        """Calling new_game() should reset the board to the starting position."""
        game = SpellChessGame()
        game.board.push_san("e4")
        game.new_game()
        assert game.board.fen() == chess.STARTING_FEN, "BUG: Board should be reset to starting position after calling new_game()"

    def test_new_game_resets_freeze_effect_color(self):
        """Calling new_game() should clear any active freeze effects."""
        game = SpellChessGame()

        status_before_freeze = game.freeze_effect_color
        game.cast_freeze(chess.E5)
        assert game.freeze_effect_color != status_before_freeze, "BUG: freeze_effect_color should change after casting freeze"
        game.new_game()
        assert game.freeze_effect_color == status_before_freeze, "BUG: freeze effect should be cleared after calling new_game()"

    def test_new_game_resets_freeze_effect_squares(self):
        """Calling new_game() should clear any active freeze effects."""
        game = SpellChessGame()

        status_before_freeze = game.freeze_effect_squares
        game.cast_freeze(chess.E5)
        assert game.freeze_effect_squares != status_before_freeze, "BUG: freeze_effect_squares should change after casting freeze"
        game.new_game()
        assert game.freeze_effect_squares == status_before_freeze, "BUG: freeze effect should be cleared after calling new_game()"

    def test_new_game_resets_freeze_effect_plies_left(self):
        """Calling new_game() should clear any active freeze effects."""
        game = SpellChessGame()

        status_before_freeze = game.freeze_effect_plies_left
        game.cast_freeze(chess.E5)
        assert game.freeze_effect_plies_left != status_before_freeze, "BUG: freeze_effect_plies_left should change after casting freeze"
        game.new_game()
        assert game.freeze_effect_plies_left == status_before_freeze, "BUG: freeze effect should be cleared after calling new_game()"

    def test_new_game_resets_freeze_cooldown_white(self):
        """Calling new_game() should reset freeze cooldowns for both players."""
        game = SpellChessGame()

        game.cast_freeze(chess.E5)
        assert game.freeze_cooldown[chess.WHITE] != 0, "BUG: freeze_cooldown should change after casting freeze"
        game.new_game()
        assert game.freeze_cooldown[chess.WHITE] == 0, "BUG: freeze cooldowns should be reset after calling new_game()"

    def test_new_game_resets_freeze_cooldown_black(self):
        """Calling new_game() should reset freeze cooldowns for both players."""
        game = SpellChessGame()

        game.cast_freeze(chess.E5)
        game.new_game()
        assert game.freeze_cooldown[chess.BLACK] == 0, "BUG: freeze cooldowns should be reset after calling new_game()"

    def test_new_game_resets_freeze_remaining_white(self):
        """Calling new_game() should reset freeze cooldowns for both players."""
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        game.new_game()
        assert game.freeze_remaining[chess.WHITE] == 5, "BUG: freeze remaining should be reset after calling new_game()"

    def test_new_game_resets_freeze_remaining_black(self):
        """Calling new_game() should reset freeze cooldowns for both players."""
        game = SpellChessGame()

        game.cast_freeze(chess.E5)
        game.new_game()
        assert game.freeze_remaining[chess.BLACK] == 5, "BUG: freeze remaining should be reset after calling new_game()"
    
    def test_new_game_resets_spell_casted_this_turn(self):
        """Calling new_game() should reset spell_casted_this_turn for both players."""
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        game.new_game()
        assert  game.spell_casted_this_turn == False, "BUG: spell_casted_this_turn should be reset after calling new_game()"

    def test_new_game_resets_get_legal_moves(self):
        """Calling new_game() should reset the board to the starting position, which has a specific set of legal moves."""
        game = SpellChessGame()

        game.cast_freeze(chess.F6)
        assert game.is_frozen(chess.F6, chess.BLACK), "BUG: Square F6 should be frozen after casting freeze on it"
        game.make_move(chess.E2, chess.E3)
        legal_moves_after_freeze = game.get_legal_moves()
        assert game.current_turn() == chess.BLACK, "It should be black's turn after White's move"
        game.new_game()
        
        assert game.get_legal_moves() != legal_moves_after_freeze, "BUG: get_legal_moves should return a different set of moves after resetting the game"

    def test_new_game_resets_jumps_remaining(self):
        """Calling new_game() should reset the jumps_remaining for both players."""
        game = SpellChessGame()
        game.cast_jump(chess.E2, chess.E4)
        game.new_game()
        assert game.jump_remaining[chess.WHITE] == 3, "BUG: jumps_remaining should be reset after calling new_game()"

    def test_new_game_resets_jump_cooldown(self):
        """Calling new_game() should reset the jump_cooldown for both players."""
        game = SpellChessGame()
        game.cast_jump(chess.E2, chess.E4)
        game.new_game()
        assert game.jump_cooldown[chess.WHITE] == 0, "BUG: jump_cooldown should be reset after calling new_game()"

    def test_new_game_resets_jump_casted_this_turn(self):
        """Calling new_game() should reset the jump_casted_this_turn for both players."""
        game = SpellChessGame()
        game.cast_jump(chess.E2, chess.E4)
        game.new_game()
        assert game.jump_casted_this_turn == False, "BUG: jump_casted_this_turn should be reset after calling new_game()"
# ------------------------------------------------------------------ #
#  CHARGES AND LIMITS — Freeze Spell                                  #
# ------------------------------------------------------------------ #

class TestFreezeChargeDecrement:
    """Each successful Freeze cast must deduct exactly 1 charge."""

    def test_white_freeze_charge_drops_by_1_after_cast(self):
        """TC-FC-02a: freeze_remaining[WHITE] must go from 5 to 4 after one cast."""
        game = SpellChessGame()
        result = game.cast_freeze(chess.E5)
        assert result is True, "cast_freeze should succeed on a fresh game"
        assert game.freeze_remaining[chess.WHITE] == 4, (
            f"BUG: White Freeze charges should be 4 after one cast, "
            f"got {game.freeze_remaining[chess.WHITE]}"
        )

    def test_freeze_cast_does_not_affect_opponent_charges(self):
        """TC-FC-02b: White casting Freeze must not change Black's charge count."""
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        assert game.freeze_remaining[chess.BLACK] == 5, (
            "BUG: White's Freeze cast must not reduce Black's charges"
        )


class TestFreezeChargeEnforcement:
    """When Freeze charges reach 0, casting must be blocked."""

    def test_cast_freeze_blocked_at_zero_charges(self):
        """TC-FC-03a: cast_freeze must return False when freeze_remaining == 0."""
        game = SpellChessGame()
        game.freeze_remaining[chess.WHITE] = 0
        result = game.cast_freeze(chess.E5)
        assert result is False, (
            "BUG: cast_freeze must return False when White has 0 charges"
        )

    def test_freeze_charges_do_not_go_below_zero(self):
        """TC-FC-03b: freeze_remaining must stay at 0 after a blocked cast."""
        game = SpellChessGame()
        game.freeze_remaining[chess.WHITE] = 0
        game.cast_freeze(chess.E5)
        assert game.freeze_remaining[chess.WHITE] == 0, (
            "BUG: freeze_remaining must not go below 0"
        )

    def test_one_freeze_charge_left_then_blocked(self):
        """TC-FC-03c: With 1 charge, cast succeeds; next cast (cooldown reset) is blocked."""
        game = SpellChessGame()
        game.freeze_remaining[chess.WHITE] = 1
        first = game.cast_freeze(chess.E5)
        assert first is True, "Cast with 1 charge remaining must succeed"
        # Reset per-turn flag and cooldown to isolate the charge check
        game.spell_casted_this_turn = False
        game.freeze_cooldown[chess.WHITE] = 0
        second = game.cast_freeze(chess.D4)
        assert second is False, (
            "BUG: cast_freeze must be blocked once charges drop to 0"
        )


# ------------------------------------------------------------------ #
#  CHARGES AND LIMITS — Jump Spell Cooldown                           #
# ------------------------------------------------------------------ #

class TestJumpCooldownSetAfterCast:
    """Casting Jump must set the cooldown to exactly 2, not 1."""

    def test_white_jump_cooldown_is_2_after_cast(self):
        """TC-JCD-01a: jump_cooldown[WHITE] must equal 2 right after casting."""
        game = SpellChessGame()
        game.cast_jump(chess.A1, chess.A3)
        assert game.jump_cooldown[chess.WHITE] == 2, (
            f"BUG: Jump cooldown must be 2 after casting (spec: 2-turn cooldown), "
            f"got {game.jump_cooldown[chess.WHITE]}"
        )

    def test_jump_cast_does_not_set_opponents_cooldown(self):
        """TC-JCD-01b: White casting Jump must not set Black's cooldown."""
        game = SpellChessGame()
        game.cast_jump(chess.A1, chess.A3)
        assert game.jump_cooldown[chess.BLACK] == 0, (
            "BUG: White casting Jump must not set Black's jump cooldown"
        )


class TestJumpCooldownDecrement:
    """Jump cooldown must decrement by 1 at the start of each of the caster's turns."""

    def test_jump_cooldown_does_not_drop_during_black_turn(self):
        """TC-JCD-03a: White's Jump cooldown must not drop while it is Black's turn."""
        game = SpellChessGame()
        game.cast_jump(chess.A1, chess.A3)
        game.make_move(chess.G1, chess.F3)    # White ends turn; now Black's turn
        assert game.jump_cooldown[chess.WHITE] == 2, (
            "BUG: White's Jump cooldown must not decrement during Black's turn"
        )

    def test_jump_cooldown_drops_to_1_after_one_white_turn(self):
        """TC-JCD-03b: After one full round (White + Black move), cooldown drops 2→1."""
        game = SpellChessGame()
        game.cast_jump(chess.A1, chess.A3)
        game.make_move(chess.G1, chess.F3)
        game.make_move(chess.B8, chess.C6)    # Black done; White's new turn starts
        assert game.jump_cooldown[chess.WHITE] == 1, (
            f"BUG: Jump cooldown should be 1 after one White turn has passed, "
            f"got {game.jump_cooldown[chess.WHITE]}"
        )

    def test_jump_cooldown_reaches_zero_after_two_white_turns(self):
        """TC-JCD-03c: After two full rounds, cooldown drops 2→0."""
        game = SpellChessGame()
        game.cast_jump(chess.A1, chess.A3)
        game.make_move(chess.G1, chess.F3)
        game.make_move(chess.B8, chess.C6)
        game.make_move(chess.B1, chess.C3)
        game.make_move(chess.G8, chess.F6)
        assert game.jump_cooldown[chess.WHITE] == 0, (
            f"BUG: Jump cooldown should be 0 after two White turns, "
            f"got {game.jump_cooldown[chess.WHITE]}"
        )

    def test_can_cast_jump_again_after_cooldown_expires(self):
        """TC-JCD-03d: cast_jump must succeed once the 2-turn cooldown has expired."""
        game = SpellChessGame()
        game.cast_jump(chess.A1, chess.A3)
        game.make_move(chess.G1, chess.F3)
        game.make_move(chess.B8, chess.C6)
        game.make_move(chess.B1, chess.C3)
        game.make_move(chess.G8, chess.F6)
        assert game.jump_cooldown[chess.WHITE] == 0, (
            "Precondition failed: cooldown must be 0 before testing re-cast."
        )
        result = game.cast_jump(chess.H1, chess.H3)
        assert result is True, (
            "BUG: cast_jump must succeed once the 2-turn cooldown has expired."
        )


# ------------------------------------------------------------------ #
#  CHARGES AND LIMITS — new_game() resets                             #
# ------------------------------------------------------------------ #

class TestNewGameResetsChargesAndCooldowns:
    """new_game() must restore all charges and clear all cooldowns."""

    def test_new_game_resets_freeze_charges_to_5(self):
        """TC-NG-01: Both sides get 5 Freeze charges after new_game()."""
        game = SpellChessGame()
        game.freeze_remaining[chess.WHITE] = 2
        game.freeze_remaining[chess.BLACK] = 0
        game.new_game()
        assert game.freeze_remaining[chess.WHITE] == 5, (
            f"BUG: White Freeze charges should be 5 after new_game(), "
            f"got {game.freeze_remaining[chess.WHITE]}"
        )
        assert game.freeze_remaining[chess.BLACK] == 5, (
            f"BUG: Black Freeze charges should be 5 after new_game(), "
            f"got {game.freeze_remaining[chess.BLACK]}"
        )

    def test_new_game_resets_jump_charges_to_3(self):
        """TC-NG-02: Both sides get 3 Jump charges after new_game()."""
        game = SpellChessGame()
        game.jump_remaining[chess.WHITE] = 0
        game.jump_remaining[chess.BLACK] = 1
        game.new_game()
        assert game.jump_remaining[chess.WHITE] == 3, (
            f"BUG: White Jump charges should be 3 after new_game(), "
            f"got {game.jump_remaining[chess.WHITE]}"
        )
        assert game.jump_remaining[chess.BLACK] == 3, (
            f"BUG: Black Jump charges should be 3 after new_game(), "
            f"got {game.jump_remaining[chess.BLACK]}"
        )

    def test_new_game_resets_freeze_cooldown_to_0(self):
        """TC-NG-03: Both Freeze cooldowns must be 0 after new_game()."""
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        game.new_game()
        assert game.freeze_cooldown[chess.WHITE] == 0, (
            f"BUG: White Freeze cooldown should be 0 after new_game(), "
            f"got {game.freeze_cooldown[chess.WHITE]}"
        )
        assert game.freeze_cooldown[chess.BLACK] == 0, (
            f"BUG: Black Freeze cooldown should be 0 after new_game(), "
            f"got {game.freeze_cooldown[chess.BLACK]}"
        )

    def test_new_game_resets_jump_cooldown_to_0(self):
        """TC-NG-04: Both Jump cooldowns must be 0 after new_game()."""
        game = SpellChessGame()
        game.cast_jump(chess.A1, chess.A3)
        game.new_game()
        assert game.jump_cooldown[chess.WHITE] == 0, (
            f"BUG: White Jump cooldown should be 0 after new_game(), "
            f"got {game.jump_cooldown[chess.WHITE]}"
        )
        assert game.jump_cooldown[chess.BLACK] == 0, (
            f"BUG: Black Jump cooldown should be 0 after new_game(), "
            f"got {game.jump_cooldown[chess.BLACK]}"
        )

    def test_cast_jump_succeeds_after_new_game(self):
        """TC-NG-05: cast_jump must succeed immediately after new_game() restores charges."""
        game = SpellChessGame()
        game.jump_remaining[chess.WHITE] = 0
        game.jump_cooldown[chess.WHITE] = 2
        game.new_game()
        result = game.cast_jump(chess.A1, chess.A3)
        assert result is True, (
            "BUG: cast_jump must succeed right after new_game() — "
            "Charges and cooldown must both be reset."
        )
