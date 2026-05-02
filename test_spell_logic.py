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
# S1-T01
class TestFreezeOpponent:
    def test_white_casts_freeze_opponent_is_black(self):
        """When White casts Freeze the frozen color must be BLACK."""
        game = SpellChessGame()
        assert game.current_turn() == chess.WHITE
        result = game.cast_freeze(chess.E5)

        # ensuring casting spell does not switch turn
        assert game.current_turn() == chess.WHITE

        assert result is True
        assert game.freeze_effect_color == chess.BLACK

    def test_black_casts_freeze_opponent_is_white(self):
        """When Black casts Freeze the frozen color must be WHITE."""
        game = SpellChessGame()
        assert game.current_turn() == chess.WHITE
        game.make_move(chess.E2, chess.E4)

        # ensuring turn switches after WHITE's move
        assert game.current_turn() == chess.BLACK

        result = game.cast_freeze(chess.E4)
        assert game.current_turn() == chess.BLACK
        assert result is True
        assert game.freeze_effect_color == chess.WHITE

# S1-T02
class TestFreezeSelf:
    def test_freeze_effect_color_is_not_caster_white(self):
        """After White casts, the frozen color must NOT equal WHITE (the caster)."""
        game = SpellChessGame()
        assert game.current_turn() == chess.WHITE
        game.cast_freeze(chess.D4)
        assert game.freeze_effect_color != chess.WHITE

    def test_freeze_effect_color_is_not_caster_black(self):
        """After Black casts, the frozen color must NOT equal BLACK (the caster)."""
        game = SpellChessGame()
        game.make_move(chess.D2, chess.D4)
        assert game.current_turn() == chess.BLACK
        game.cast_freeze(chess.D5)
        assert game.freeze_effect_color != chess.BLACK
    
    def test_freeze_on_self_does_not_affect_self(self):
        game = SpellChessGame()
        assert game.current_turn() == chess.WHITE

        # list of legal moves before freezing
        options_before_cast = game.get_legal_moves()
        result = game.cast_freeze(chess.E2)
        assert result is True

        # list of legal moves after freezing
        options_after_cast = game.get_legal_moves()
        assert options_before_cast == options_after_cast
        assert game.freeze_effect_color != chess.WHITE

# S1-T03
class TestCenterSquareIncluded:
        """The center square itself must always be in the result."""

        def test_center_included_for_every_square(self):
            failures = [
                chess.square_name(sq)
                for sq in chess.SQUARES
                if sq not in squares_in_3x3(sq)
            ]
            assert failures == [], f"Center missing for: {failures}"

        # checking every location on the board for casting freeze spell
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

    # testing if the number of squares are correct for casting freeze spell
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

# S1-T04
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

#  S1-T05
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



# S1-T06
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

# S1-T07
class TestJumpValid:
    """A correctly formed Jump cast must succeed and relocate the piece."""

    def test_valid_jump_returns_true(self):
        """cast_jump should return True for a legal jump."""
        game = SpellChessGame()
        # White knight on g1 to e3 (Chebyshev distance 2, empty square)
        assert game.cast_jump(chess.G1, chess.E3) is True

    def test_valid_jump_moves_piece_to_destination(self):
        """After a successful jump the piece must appear on the destination square."""
        game = SpellChessGame()
        piece_before = game.board.piece_at(chess.G1)
        game.cast_jump(chess.G1, chess.E3)
        assert game.board.piece_at(chess.E3) == piece_before

    def test_valid_jump_clears_origin_square(self):
        """After a successful jump the origin square must be empty."""
        game = SpellChessGame()
        game.cast_jump(chess.G1, chess.E3)
        assert game.board.piece_at(chess.G1) is None

    def test_jump_ignores_pieces_in_between(self):
        """Jump teleports over blocking pieces — the path must not matter."""
        game = SpellChessGame()
        assert game.cast_jump(chess.C1, chess.E3) is True


class TestJumpOwnPiece:
    """Jump must only be usable on the caster's own pieces."""

    def test_jump_rejects_empty_source_square(self):
        """cast_jump must return False when there is no piece on the source square."""
        game = SpellChessGame()
        assert game.cast_jump(chess.E4, chess.E6) is False

    def test_jump_rejects_opponent_piece(self):
        """White may not jump a Black piece."""
        game = SpellChessGame()
        # Black pawn on e7 — White tries to jump it.
        assert game.cast_jump(chess.E7, chess.E5) is False


class TestJumpKingRestriction:
    """The King may not be selected as the jumping piece."""

    def test_jump_rejects_own_king(self):
        """cast_jump must return False when the selected piece is the King."""
        game = SpellChessGame()
        # White king starts on e1.
        assert game.cast_jump(chess.E1, chess.E3) is False


class TestJumpEmptyDestination:
    """The destination square must be empty — Jump may not capture."""

    def test_jump_rejects_occupied_destination_own_piece(self):
        """cast_jump must return False when the destination holds a friendly piece."""
        game = SpellChessGame()
        # White knight g1 to g2 (White pawn is on g2).
        assert game.cast_jump(chess.G1, chess.G2) is False

    def test_jump_rejects_occupied_destination_opponent_piece(self):
        """cast_jump must return False when the destination holds an opponent piece."""
        game = SpellChessGame()
        game.make_move(chess.E2, chess.E4)      # moving white pawn
        game.make_move(chess.E7, chess.E5)      # moving black pawn
        assert game.cast_jump(chess.E4, chess.E5) is False     # trying to jump black pawn with white pawn

# S1-T08
class TestJumpRange:
    """Jump is limited to Chebyshev distance ≤ 2."""
    def test_jump_spell_jump_to_same_square(self):
        """A player should not be able to cast a Jump spell to the same square."""
        game = SpellChessGame()
        #  Try to jump to the same square
        result = game.cast_jump(chess.E2, chess.E2)  
        assert result is False

    def test_jump_accepts_distance_1(self):
        """A jump of Chebyshev distance 1 is within range and must succeed."""
        game = SpellChessGame()
        # Place a White Pawn on e3, destination e4 is at distance 1.
        assert game.cast_jump(chess.E2, chess.E3) is True

    def test_jump_accepts_distance_2(self):
        """A jump of Chebyshev distance 2 is within range and must succeed."""
        game = SpellChessGame()
        assert game.cast_jump(chess.G1, chess.E3) is True

    def test_jump_rejects_distance_3(self):
        """A jump of Chebyshev distance 3 exceeds the rule limit and must be rejected."""
        game = SpellChessGame()
        # Place a White Pawn on e2; e5 is distance 3.
        assert game.cast_jump(chess.E2, chess.E5) is False

    def test_jump_rejects_distance_beyond_board(self):
        """A jump to a square more than 2 away in any direction must be rejected."""
        game = SpellChessGame()
        # White knight b1; destination b8 is 7 ranks away.
        assert game.cast_jump(chess.B1, chess.B8) is False

##########
# S2-T01
class TestFreezeCharges:
    """Freeze starts with 5 charges; each cast costs 1; 0 charges blocks casting."""

    def test_freeze_charges_start_at_five_for_both_sides(self):
        """Both sides must begin with exactly 5 Freeze charges."""
        game = SpellChessGame()
        assert game.freeze_remaining[chess.WHITE] == 5
        assert game.freeze_remaining[chess.BLACK] == 5

    def test_freeze_charge_decrements_after_successful_cast(self):
        """White's Freeze charge must drop from 5 to 4 after one cast."""
        game = SpellChessGame()
        assert game.cast_freeze(chess.E5) is True
        assert game.freeze_remaining[chess.WHITE] == 4

    def test_freeze_charge_decrements_for_black_after_successful_cast(self):
        """Black's Freeze charge must drop from 5 to 4 after one cast."""
        game = SpellChessGame()
        game.make_move(chess.E2, chess.E4)          
        assert game.cast_freeze(chess.E4) is True
        assert game.freeze_remaining[chess.BLACK] == 4

    def test_freeze_blocked_when_charges_are_zero(self):
        """cast_freeze must return False when the caster has 0 charges."""
        game = SpellChessGame()
        game.freeze_remaining[chess.WHITE] = 0
        assert game.cast_freeze(chess.E5) is False

    def test_freeze_charge_cannot_go_below_zero(self):
        """After all 5 Freeze charges are used, the charge counter must be 0, not negative."""
        game = SpellChessGame()
        game.freeze_remaining[chess.WHITE] = 1
        game.cast_freeze(chess.E5)
        assert game.freeze_remaining[chess.WHITE] == 0

class TestFreezePerTurnLimit:
    """Only one Freeze cast is allowed per turn; it must happen before the move."""

    def test_freeze_cannot_be_cast_twice_in_same_turn(self):
        """A second cast_freeze() call in the same turn must return False."""
        game = SpellChessGame()
        assert game.cast_freeze(chess.E5) is True
        assert game.cast_freeze(chess.D4) is False

    def test_freeze_cast_limit_resets_next_turn(self):
        """After the caster's turn ends, the per-turn limit resets so the next
        player (or the same player on their next turn) can cast again."""
        game = SpellChessGame()
        # White casts Freeze, then moves.
        assert game.cast_freeze(chess.E5) is True
        game.make_move(chess.E2, chess.E4)
        # It is now Black's turn; Black has had no cast yet this turn.
        assert game.spell_casted_this_turn is False
        # Black should be able to cast on their own turn.
        assert game.cast_freeze(chess.E4) is True

    def test_freeze_charge_does_not_decrement_on_failed_cast(self):
        """A failed cast (duplicate in same turn) must not consume a charge."""
        game = SpellChessGame()
        game.cast_freeze(chess.E5)          # succeeds, charge 5 to 4
        charges_before = game.freeze_remaining[chess.WHITE]
        game.cast_freeze(chess.D4)          # fails (same-turn duplicate)
        assert game.freeze_remaining[chess.WHITE] == charges_before

class TestJumpCharges:
    """Jump starts with 3 charges; each cast costs 1; 0 charges blocks casting."""

    def test_jump_charges_start_at_three_for_both_sides(self):
        """Both sides must begin with exactly 3 Jump charges."""
        game = SpellChessGame()
        assert game.jump_remaining[chess.WHITE] == 3
        assert game.jump_remaining[chess.BLACK] == 3

    def test_jump_charge_decrements_after_successful_cast(self):
        """White's Jump charge must drop from 3 to 2 after one cast."""
        game = SpellChessGame()
        assert game.cast_jump(chess.G1, chess.E3) is True
        assert game.jump_remaining[chess.WHITE] == 2

    def test_jump_charge_decrements_for_black_after_successful_cast(self):
        """Black's Jump charge must drop from 3 to 2 after one cast."""
        game = SpellChessGame()
        game.make_move(chess.E2, chess.E4)          
        assert game.cast_jump(chess.G8, chess.E6) is True
        assert game.jump_remaining[chess.BLACK] == 2

    def test_jump_blocked_when_charges_are_zero(self):
        """cast_jump must return False when the caster has 0 charges."""
        game = SpellChessGame()
        game.jump_remaining[chess.WHITE] = 0
        assert game.cast_jump(chess.G1, chess.E3) is False

    def test_jump_charge_cannot_go_below_zero(self):
        """After all 3 Jump charges are used, the charge counter must be 0, not negative."""
        game = SpellChessGame()
        game.jump_remaining[chess.WHITE] = 1
        game.cast_jump(chess.G1, chess.E3)
        assert game.jump_remaining[chess.WHITE] == 0

class TestJumpPerTurnLimit:
    """Only one Jump cast is allowed per turn; it must happen before the move."""

    def test_jump_cannot_be_cast_twice_in_same_turn(self):
        """A second cast_jump() call in the same turn must return False."""
        game = SpellChessGame()
        assert game.cast_jump(chess.G1, chess.E3) is True
        # Try to jump a different piece in the same turn.
        result = game.cast_jump(chess.B1, chess.C3)
        assert result is False

    def test_jump_cast_limit_resets_next_turn(self):
        """After the caster's turn ends, jump_casted_this_turn must reset so the
        next player can cast Jump on their turn."""
        game = SpellChessGame()
        assert game.cast_jump(chess.G1, chess.E3) is True
        game.make_move(chess.E3, chess.F5)         # White moves the jumped piece
        # It is now Black's turn.
        assert game.jump_casted_this_turn is False
        assert game.cast_jump(chess.G8, chess.E6) is True

    def test_jump_charge_does_not_decrement_on_failed_cast(self):
        """A failed cast (duplicate in same turn) must not consume a charge."""
        game = SpellChessGame()
        game.cast_jump(chess.G1, chess.E3)          # succeeds, charge 3 to 2
        charges_before = game.jump_remaining[chess.WHITE]
        game.cast_jump(chess.B1, chess.C3)          # fails (same-turn duplicate)
        assert game.jump_remaining[chess.WHITE] == charges_before

class TestSpellsAreIndependent:
    """Casting one spell must not affect the other spell's charges or limits."""

    def test_casting_freeze_does_not_block_jump_in_same_turn(self):
        """After casting Freeze, the player should still be able to cast Jump
        (spells have independent per-turn limits per the spec)."""
        game = SpellChessGame()
        assert game.cast_freeze(chess.E5) is True
        assert game.cast_jump(chess.G1, chess.E3) is True

    def test_casting_jump_does_not_block_freeze_in_same_turn(self):
        """After casting Jump, the player should still be able to cast Freeze."""
        game = SpellChessGame()
        assert game.cast_jump(chess.G1, chess.E3) is True
        assert game.cast_freeze(chess.E5) is True

    def test_freeze_charges_unaffected_by_jump_cast(self):
        """Casting Jump must not change the Freeze charge count."""
        game = SpellChessGame()
        freeze_before = game.freeze_remaining[chess.WHITE]
        game.cast_jump(chess.G1, chess.E3)
        assert game.freeze_remaining[chess.WHITE] == freeze_before

    def test_jump_charges_unaffected_by_freeze_cast(self):
        """Casting Freeze must not change the Jump charge count."""
        game = SpellChessGame()
        jump_before = game.jump_remaining[chess.WHITE]
        game.cast_freeze(chess.E5)
        assert game.jump_remaining[chess.WHITE] == jump_before

# S2-T02
class TestJumpChargesAndCooldown:
    """Jump has 3 charges and a cooldown after use."""

    def test_jump_charges_start_at_three(self):
        """Both sides must start with exactly 3 Jump charges."""
        game = SpellChessGame()
        assert game.jump_remaining[chess.WHITE] == 3
        assert game.jump_remaining[chess.BLACK] == 3

    def test_jump_charge_decrements_on_success(self):
        """A successful jump must reduce the caster's charge count by 1."""
        game = SpellChessGame()
        assert game.cast_jump(chess.G1, chess.E3) is True
        assert game.jump_remaining[chess.WHITE] == 2

    def test_jump_cooldown_set_after_cast(self):
        """After a successful jump the caster's cooldown must be > 0."""
        game = SpellChessGame()
        game.cast_jump(chess.G1, chess.E3)
        assert game.jump_cooldown[chess.WHITE] > 0

    def test_jump_rejected_when_no_charges_remain(self):
        """cast_jump must return False once all 3 charges are spent."""
        game = SpellChessGame()
        game.jump_remaining[chess.WHITE] = 0
        assert game.cast_jump(chess.G1, chess.E3) is False

    def test_jump_rejected_while_on_cooldown(self):
        """cast_jump must return False while the caster is on cooldown."""
        game = SpellChessGame()
        game.jump_cooldown[chess.WHITE] = 2
        assert game.cast_jump(chess.G1, chess.E3) is False

    def test_jump_cooldown_counts_down_on_casters_turn_starts(self):
        game = SpellChessGame()

        assert game.cast_jump(chess.H1, chess.H3) is True
        assert game.jump_cooldown[chess.WHITE] == 2
        assert game.current_turn() == chess.WHITE
        assert game.make_move(chess.G1, chess.F3) is True

        # Moving to Black's turn should not reduce White's cooldown yet.
        assert game.current_turn() == chess.BLACK
        assert game.jump_cooldown[chess.WHITE] == 2
        assert game.make_move(chess.A7, chess.A6) is True

        # At the start of White's next turn, cooldown drops from 2 to 1.
        assert game.current_turn() == chess.WHITE
        assert game.jump_cooldown[chess.WHITE] == 1
        assert game.cast_jump(chess.A1, chess.A3) is False

        # The following White turns continue the countdown: 1 -> 0.
        assert game.make_move(chess.B1, chess.C3) is True
        assert game.make_move(chess.B7, chess.B6) is True
        assert game.current_turn() == chess.WHITE
        assert game.jump_cooldown[chess.WHITE] == 0
        assert game.cast_jump(chess.A1, chess.A3) is True

    def test_double_jump_in_second_turn(self):
        game = SpellChessGame()
        game.cast_jump(chess.G1, chess.E3)
        game.make_move(chess.E3, chess.F5)         # White moves the jumped piece
        assert game.current_turn() == chess.BLACK
        game.make_move(chess.E7, chess.E5)         # Black moves
        assert game.current_turn() == chess.WHITE
        assert game.cast_jump(chess.B1, chess.C3) is False
        assert game.current_turn() == chess.WHITE
        assert game.cast_jump(chess.B1, chess.C3) is False
  
# S2-T03 to S2-T04
class TestGameResets:
    def test_new_game_resets_board(self):
        """Calling new_game() should reset the board to the starting position."""
        game = SpellChessGame()
        game.board.push_san("e4")
        game.new_game()
        assert game.board.fen() == chess.STARTING_FEN

    def test_new_game_resets_freeze_effect_color(self):
        """Calling new_game() should clear any active freeze effects."""
        game = SpellChessGame()

        status_before_freeze = game.freeze_effect_color
        game.cast_freeze(chess.E5)
        assert game.freeze_effect_color != status_before_freeze
        game.new_game()
        assert game.freeze_effect_color == status_before_freeze

    def test_new_game_resets_freeze_effect_squares(self):
        """Calling new_game() should clear any active freeze effects."""
        game = SpellChessGame()

        status_before_freeze = game.freeze_effect_squares
        game.cast_freeze(chess.E5)
        assert game.freeze_effect_squares != status_before_freeze
        game.new_game()
        assert game.freeze_effect_squares == status_before_freeze

    def test_new_game_resets_freeze_effect_plies_left(self):
        """Calling new_game() should clear any active freeze effects."""
        game = SpellChessGame()

        status_before_freeze = game.freeze_effect_plies_left
        game.cast_freeze(chess.E5)
        assert game.freeze_effect_plies_left != status_before_freeze
        game.new_game()
        assert game.freeze_effect_plies_left == status_before_freeze

    def test_new_game_resets_freeze_cooldown_white(self):
        """Calling new_game() should reset freeze cooldowns for both players."""
        game = SpellChessGame()

        game.cast_freeze(chess.E5)
        assert game.freeze_cooldown[chess.WHITE] != 0
        game.new_game()
        assert game.freeze_cooldown[chess.WHITE] == 0

    def test_new_game_resets_freeze_cooldown_black(self):
        """Calling new_game() should reset freeze cooldowns for both players."""
        game = SpellChessGame()

        game.cast_freeze(chess.E5)
        game.new_game()
        assert game.freeze_cooldown[chess.BLACK] == 0

    def test_new_game_resets_freeze_remaining_white(self):
        """Calling new_game() should reset freeze cooldowns for both players."""
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        game.new_game()
        assert game.freeze_remaining[chess.WHITE] == 5

    def test_new_game_resets_freeze_remaining_black(self):
        """Calling new_game() should reset freeze cooldowns for both players."""
        game = SpellChessGame()

        game.cast_freeze(chess.E5)
        game.new_game()
        assert game.freeze_remaining[chess.BLACK] == 5
    
    def test_new_game_resets_spell_casted_this_turn(self):
        """Calling new_game() should reset spell_casted_this_turn for both players."""
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        game.new_game()
        assert  game.spell_casted_this_turn == False

    def test_new_game_resets_get_legal_moves(self):
        """Calling new_game() should reset the board to the starting position, which has a specific set of legal moves."""
        game = SpellChessGame()

        game.cast_freeze(chess.F6)
        assert game.is_frozen(chess.F6, chess.BLACK)
        game.make_move(chess.E2, chess.E3)

        # legal moves available to black player after opponent cast freeze spell
        legal_moves_after_freeze = game.get_legal_moves()
        assert game.current_turn() == chess.BLACK
        game.new_game()
        game.make_move(chess.E2, chess.E3)

        # legal moves available to black player when opponent has not casted freeze spell
        # this checks if freeze spell affects the available legal moves for the black player
        assert game.get_legal_moves() != legal_moves_after_freeze

    def test_new_game_resets_jumps_remaining(self):
        """Calling new_game() should reset the jumps_remaining for both players."""
        game = SpellChessGame()
        game.cast_jump(chess.E2, chess.E4)
        game.new_game()
        assert game.jump_remaining[chess.WHITE] == 3

    def test_new_game_resets_jump_cooldown(self):
        """Calling new_game() should reset the jump_cooldown for both players."""
        game = SpellChessGame()
        game.cast_jump(chess.E2, chess.E4)
        game.new_game()
        assert game.jump_cooldown[chess.WHITE] == 0

    def test_new_game_resets_jump_casted_this_turn(self):
        """Calling new_game() should reset the jump_casted_this_turn for both players."""
        game = SpellChessGame()
        game.cast_jump(chess.E2, chess.E4)
        game.new_game()
        assert game.jump_casted_this_turn == False

# S2T05
def game_with_black_e_pawn_frozen() -> SpellChessGame:
    """Create a focused S2 fixture with Black to move and e7 frozen."""
    game = SpellChessGame()
    game.board.turn = chess.BLACK
    game.freeze_effect_color = chess.BLACK
    game.freeze_effect_squares = {chess.E7}
    game.freeze_effect_plies_left = 1
    return game

class TestFrozenOriginMoveRestriction:
    """Frozen-origin moves must be rejected and filtered from legal moves."""

    def test_make_move_rejects_move_from_frozen_origin(self):
        game = game_with_black_e_pawn_frozen()

        assert game.is_frozen(chess.E7, chess.BLACK) is True

        # black pawn on e7 is frozen, so it cannot move
        assert game.make_move(chess.E7, chess.E5) is False
        assert game.board.piece_at(chess.E7) == chess.Piece(chess.PAWN, chess.BLACK)
        assert game.board.piece_at(chess.E5) is None

    def test_get_legal_moves_excludes_moves_from_frozen_origin(self):
        game = game_with_black_e_pawn_frozen()

        legal_moves = set(game.get_legal_moves())

        assert chess.Move(chess.E7, chess.E5) not in legal_moves
        assert chess.Move(chess.E7, chess.E6) not in legal_moves
        assert chess.Move(chess.G8, chess.F6) in legal_moves

# S2T06
class TestFrozenOriginUiFeedback:
    """UI-facing helpers should support blocking and explaining frozen moves."""

    def test_current_player_can_be_identified_as_frozen_for_ui_blocking(self):
        game = game_with_black_e_pawn_frozen()

        assert game.current_turn() == chess.BLACK
        assert game.is_frozen(chess.E7, game.current_turn()) is True
        assert game.is_frozen(chess.G8, game.current_turn()) is False

    def test_freeze_info_text_mentions_frozen_pieces_for_current_player(self):
        game = game_with_black_e_pawn_frozen()

        freeze_text = game.freeze_info_text().lower()
        assert "frozen" in freeze_text


#######################
# S3T01
class TestGameStateDisplayTraceability:
    """Every accepted game-state display rule should have test coverage."""

    def test_status_text_shows_current_player_turn(self):
        game = SpellChessGame()

        assert game.status_text() == "Turn: White."
        game.board.turn = chess.BLACK
        assert game.status_text() == "Turn: Black."

    def test_status_text_marks_check(self):
        game = SpellChessGame()

        # making moves to put black king in check
        assert game.make_move(chess.E2, chess.E4) is True
        assert game.make_move(chess.D7, chess.D6) is True
        assert game.make_move(chess.F1, chess.B5) is True

        status = game.status_text()

        assert "Turn: Black" in status
        assert "check" in status.lower()


    def test_freeze_info_text_shows_current_player_charges_and_cooldown(self):
        game = SpellChessGame()
        game.cast_freeze(chess.E5)  # This will set White's charges to 4 and cooldown to 3

        text = game.freeze_info_text()

        assert "Freeze: 4" in text
        assert "cooldown 3" in text
        assert "Freeze: 2" not in text
        game.make_move(chess.E2, chess.E4)  # End White's turn to show Black

        text = game.freeze_info_text()

        assert "Freeze: 5" in text
        assert "cooldown 0" not in text

    def test_jump_info_text_shows_current_player_charges_and_cooldown(self):
        game = SpellChessGame()
        game.cast_jump(chess.E2, chess.E4)
        text = game.jump_info_text()

        assert "Jump: 2" in text
        assert "cooldown 2" in text
        assert "Jump: 1" not in text
        game.make_move(chess.E4, chess.E5)  # End White's turn to show Black
        text = game.jump_info_text()

        assert "Jump: 3" in text
        assert "cooldown 0" not in text

    
# S3T02
class TestCloseDisplayGaps:
    """Close remaining display and state-reporting test gaps."""

    def test_freeze_info_text_mentions_when_current_player_is_frozen(self):
        game = SpellChessGame()
        game.board.turn = chess.BLACK
        game.freeze_effect_color = chess.BLACK
        game.freeze_effect_squares = {chess.E7}
        game.freeze_effect_plies_left = 1

        assert "frozen" in game.freeze_info_text().lower()

    def test_game_over_status_text_reports_checkmate_winner(self):
        game = SpellChessGame()
        game.board.push_san("f3")
        game.board.push_san("e5")
        game.board.push_san("g4")
        game.board.push_san("Qh4#")

        status = game.status_text()

        assert status.startswith("Game over:")
        assert "Black wins" in status

# S3-T03
class TestFrozenAreaCaptureAndCheck:
    """Frozen pieces are movement-restricted, but can still be captured or checked."""
    def test_white_can_capture_black_piece_inside_frozen_area(self):
        game = SpellChessGame()

        # opening moves
        assert game.make_move(chess.E2, chess.E4) is True
        assert game.make_move(chess.G8, chess.F6) is True
        assert game.make_move(chess.G1, chess.F3) is True
        assert game.make_move(chess.D7, chess.D5) is True

        # white player casts freeze spell
        game.freeze_effect_color = chess.BLACK
        game.freeze_effect_squares = {
            chess.D4, chess.E4, chess.F4,
            chess.D5, chess.E5, chess.F5,
            chess.D6, chess.E6, chess.F6,
        }
        game.freeze_effect_plies_left = 1
        assert game.current_turn() == chess.WHITE

        # check if black pawn on d5 is frozen
        assert game.is_frozen(chess.D5, chess.BLACK) is True
        assert game.is_frozen(chess.F6, chess.BLACK) is True

        # check if white pawn on e4 can move to d5
        assert game.make_move(chess.E4, chess.D5) is True

        # check if black pawn on d5 is captured
        assert game.board.piece_at(chess.D5) == chess.Piece(chess.PAWN, chess.WHITE)
        assert game.board.piece_at(chess.E4) is None
    
    def test_white_can_give_check_when_black_king_is_in_frozen_area(self):
        game = SpellChessGame()

        # opening moves
        assert game.make_move(chess.E2, chess.E4) is True
        assert game.make_move(chess.E7, chess.E5) is True
        assert game.make_move(chess.D1, chess.H5) is True
        assert game.make_move(chess.B8, chess.C6) is True
        assert game.make_move(chess.F1, chess.C4) is True
        assert game.make_move(chess.G8, chess.F6) is True

        # white player casts freeze spell
        game.freeze_effect_color = chess.BLACK
        game.freeze_effect_squares = {
            chess.D7, chess.E7, chess.F7,
            chess.D8, chess.E8, chess.F8,
        }
        game.freeze_effect_plies_left = 1
        assert game.current_turn() == chess.WHITE

        # check if black king on e8 is frozen
        assert game.is_frozen(chess.E8, chess.BLACK) is True

        # white queen check the black king on e8
        assert game.make_move(chess.H5, chess.F7) is True

        # check if white queen on f7 check the black king on e8
        assert game.board.piece_at(chess.F7) == chess.Piece(chess.QUEEN, chess.WHITE)
        assert game.board.is_check() is True
        assert "check" in game.status_text().lower()
