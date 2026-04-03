import importlib
import pytest


@pytest.fixture()
def vm_mod():
    mod = importlib.import_module("VendingMachine")
    return mod


@pytest.fixture()
def vm(vm_mod):
    return vm_mod.VendingMachine()


def test_getters_default_state(vm, vm_mod):
    assert vm.get_number_of_product() == 0
    assert vm.get_current_balance() == 0
    assert vm.get_current_mode() == vm_mod.VendingMachine.Mode.OPERATION
    assert vm.get_price() == 5


def test_get_current_sum_operation_is_zero(vm):
    vm._coins1 = 10
    vm._coins2 = 10
    vm._mode = 1
    s = vm.get_current_sum()
    assert s == 0


def test_get_current_sum_admin_is_coins_value(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    vm._coins1 = 3
    vm._coins2 = 4
    s = vm.get_current_sum()
    assert s == 3 * vm._coinval1 + 4 * vm._coinval2


def test_get_coins1_operation_is_zero(vm):
    vm._coins1 = 7
    vm._mode = 1
    assert vm.get_coins1() == 0


def test_get_coins1_admin_returns_coins1(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    vm._coins1 = 7
    assert vm.get_coins1() == 7


@pytest.mark.xfail(reason="get_coins2() should return 0 in OPERATION mode. \
                Meanwhile, code returns coins1", strict=False)
def test_get_coins2_operation_should_be_zero(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._coins1 = 5
    vm._coins2 = 7
    got = vm.get_coins2()
    assert got == 0


def test_get_coins2_admin_returns_coins2(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    vm._coins2 = 9
    assert vm.get_coins2() == 9


def test_fill_products_admin_mode_works(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    vm._num = 0
    r = vm.fill_products()
    assert r == vm_mod.VendingMachine.Response.OK
    assert vm._num == vm._max


@pytest.mark.xfail(reason="fill_products() should work only in ADMINISTERING. \
                Meanwhile, the code ignores the mode", strict=False)
def test_fill_products_in_operation_should_be_illegal_per_spec(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._num = 0
    r = vm.fill_products()
    assert r == vm_mod.VendingMachine.Response.ILLEGAL_OPERATION
    assert vm._num == 0


def test_fill_coins_illegal_in_operation(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    r = vm.fill_coins(1, 1)
    assert r == vm_mod.VendingMachine.Response.ILLEGAL_OPERATION


@pytest.mark.xfail(reason="If c1 > maxc1, the code must return INVALID_PARAM. Meanwhile it doesn't check c1", strict=False)
def test_fill_coins_c1_above_max_should_be_invalid(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    vm._maxc1 = 5
    vm._maxc2 = 50

    r = vm.fill_coins(6, 1)
    assert r == vm_mod.VendingMachine.Response.INVALID_PARAM


def test_fill_coins_c2_above_max_should_be_invalid(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    vm._maxc1 = 50
    vm._maxc2 = 5

    r = vm.fill_coins(1, 6)
    assert r == vm_mod.VendingMachine.Response.INVALID_PARAM


def test_fill_coins_valid_params(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    vm._maxc1 = 50
    vm._maxc2 = 50
    r = vm.fill_coins(10, 20)
    assert r == vm_mod.VendingMachine.Response.OK
    assert vm._coins1 == 10
    assert vm._coins2 == 20


@pytest.mark.xfail(reason="fill_coins() should reject c2 <= 0. Meanwhile, the code doesn't check it", strict=False)
def test_fill_coins_should_reject_c2_le_zero(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    r = vm.fill_coins(1, 0)
    assert r == vm_mod.VendingMachine.Response.INVALID_PARAM


def test_fill_coins_should_reject_c1_le_zero(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    r = vm.fill_coins(0, 1)
    assert r == vm_mod.VendingMachine.Response.INVALID_PARAM


def test_enter_admin_mode_wrong_code_invalid_param(vm, vm_mod):
    vm._balance = 0
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    r = vm.enter_admin_mode(123)
    assert r == vm_mod.VendingMachine.Response.INVALID_PARAM
    assert vm._mode == vm_mod.VendingMachine.Mode.OPERATION


def test_enter_admin_mode_ok(vm, vm_mod):
    vm._balance = 0
    r = vm.enter_admin_mode(117345294655382)
    assert r == vm_mod.VendingMachine.Response.OK
    assert vm._mode == vm_mod.VendingMachine.Mode.ADMINISTERING


@pytest.mark.xfail(reason="If balance != 0 then enter_admin_mode returns CANNOT_PERFORM. \
                          Meanwhile, the code returns UNSUITABLE_CHANGE", strict=False)
def test_enter_admin_mode_with_nonzero_balance_should_return_cannot_perform(vm, vm_mod):
    vm._balance = 1
    r = vm.enter_admin_mode(117345294655382)
    assert r == vm_mod.VendingMachine.Response.CANNOT_PERFORM


def test_exit_admin_mode_from_admin(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    vm.exit_admin_mode()
    assert vm._mode == vm_mod.VendingMachine.Mode.OPERATION


def test_exit_admin_mode_from_operation(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm.exit_admin_mode()
    assert vm._mode == vm_mod.VendingMachine.Mode.OPERATION


def test_set_prices_illegal_in_operation(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    r = vm.set_prices(10)
    assert r == vm_mod.VendingMachine.Response.ILLEGAL_OPERATION


def test_set_prices_invalid_param(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    vm_mod._price = 0
    r = vm.set_prices(0)
    assert r == vm_mod.VendingMachine.Response.INVALID_PARAM


@pytest.mark.xfail(reason="set_prices(p > 0) should return OK and set price to p. \
                    Meanwhile, the code checks global _price instead of p", strict=False)
def test_set_prices_ok(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    r = vm.set_prices(7)
    assert r == vm_mod.VendingMachine.Response.OK
    assert vm.get_price() == 7


@pytest.mark.xfail(reason="set_prices(p <= 0) should return INVALID_PARAM. \
                    Meanwhile, the code checks global _price instead of p", strict=False)
def test_set_prices_should_reject_nonpositive_p_per_spec(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    vm_mod._price = 1
    r = vm.set_prices(0)
    assert r == vm_mod.VendingMachine.Response.INVALID_PARAM


def test_put_coin1_illegal_in_admin(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    r = vm.put_coin1()
    assert r == vm_mod.VendingMachine.Response.ILLEGAL_OPERATION


def test_put_coin2_illegal_in_admin(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    r = vm.put_coin2()
    assert r == vm_mod.VendingMachine.Response.ILLEGAL_OPERATION


@pytest.mark.xfail(reason="put_coin1() should check if _coins1 is full before adding a coin. \
                    The code checks _coins2 instead and addds to _coins2", strict=False)
def test_put_coin1_cannot_perform_when_coin1_full(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._coins1 = vm._maxc1
    r = vm.put_coin1()
    assert r == vm_mod.VendingMachine.Response.CANNOT_PERFORM
    assert vm.get_coins2 == 0


@pytest.mark.xfail(reason="put_coin2() should check if _coins2 is full before adding a coin. \
                    The code checks _coins1 instead and adds to coins_1", strict=False)
def test_put_coin2_cannot_perform_when_coin2_full(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._coins2 = vm._maxc2
    r = vm.put_coin2()
    assert r == vm_mod.VendingMachine.Response.CANNOT_PERFORM
    assert vm.get_coins1 == 0


@pytest.mark.xfail(reason="put_coin1() should +1 to _coins1 and add coin1 to balance. \
                    Meanwhile, the code adds +1 to _coins2 and adds coin2 to balance", strict=False)
def test_put_coin1_when_coins1_lt_maxc1(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    r = vm.put_coin1()
    assert r == vm_mod.VendingMachine.Response.OK
    assert vm._coins1 == 1
    assert vm._balance == 1 * vm._coinval1


@pytest.mark.xfail(reason="put_coin2() should +1 to _coins2 and add coin2 to balance. \
                    Meanwhile, the code adds +1 to _coins1 and adds coin1 to balance", strict=False)
def test_put_coin2_when_coins2_lt_maxc2(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    r = vm.put_coin2()
    assert r == vm_mod.VendingMachine.Response.OK
    assert vm._coins2 == 1
    assert vm._balance == 1 * vm._coinval2


def test_return_money_illegal_in_admin(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    r = vm.return_money()
    assert r == vm_mod.VendingMachine.Response.ILLEGAL_OPERATION


def test_return_money_zero_balance_ok(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._balance = 0
    r = vm.return_money()
    assert r == vm_mod.VendingMachine.Response.OK


def test_return_money_too_big_change(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._balance = 10
    vm._coins1 = 0
    vm._coins2 = 0
    r = vm.return_money()
    assert r == vm_mod.VendingMachine.Response.TOO_BIG_CHANGE


def test_return_money_balance_gt_all_coin2_value_uses_all_coin2_then_coin1(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._coins2 = 1
    vm._coins1 = 10
    vm._balance = 4

    r = vm.return_money()

    assert r == vm_mod.VendingMachine.Response.OK
    assert vm._coins2 == 0
    assert vm._coins1 == 8
    assert vm._balance == 0


def test_return_money_even_uses_only_coin2(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._coins2 = 10
    vm._coins1 = 3
    vm._balance = 4

    r = vm.return_money()

    assert r == vm_mod.VendingMachine.Response.OK
    assert vm._coins2 == 8
    assert vm._coins1 == 3
    assert vm._balance == 0


def test_return_money_odd_no_coin1_unsuitable(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._coins2 = 10
    vm._coins1 = 0
    vm._balance = 3

    r = vm.return_money()

    assert r == vm_mod.VendingMachine.Response.UNSUITABLE_CHANGE
    assert vm._coins2 == 10
    assert vm._coins1 == 0
    assert vm._balance == 3


@pytest.mark.xfail(reason="return_money() should - _balance // _coinval2 to _coins2 and -1 to _coins1. \
                    Instead the code mixes up _coins1 and _coins2", strict=False)
def test_return_money_odd_with_coin1(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._coins2 = 10
    vm._coins1 = 5
    vm._balance = 7

    r = vm.return_money()

    assert r == vm_mod.VendingMachine.Response.OK
    assert vm._coins2 == 7
    assert vm._coins1 == 4
    assert vm._balance == 0


def test_give_product_illegal_in_admin(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.ADMINISTERING
    r = vm.give_product(1)
    assert r == vm_mod.VendingMachine.Response.ILLEGAL_OPERATION


def test_give_product_invalid_param(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    r = vm.give_product(0)
    assert r == vm_mod.VendingMachine.Response.INVALID_PARAM


def test_give_product_insufficient_product(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._num = 0
    r = vm.give_product(1)
    assert r == vm_mod.VendingMachine.Response.INSUFFICIENT_PRODUCT


def test_give_product_insufficient_money_res_negative(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._num = 10
    vm._balance = 0
    r = vm.give_product(1)
    assert r == vm_mod.VendingMachine.Response.INSUFFICIENT_MONEY


@pytest.mark.xfail(reason="If not enough change after purchase => TOO_BIG_CHANGE. \
                The code returns INSUFFICIENT_MONEY instead", strict=False)
def test_give_product_not_enough_change_should_be_too_big_change(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._num = 10
    vm._balance = 10
    vm._coins1 = 0
    vm._coins2 = 0
    r = vm.give_product(1)
    assert r == vm_mod.VendingMachine.Response.TOO_BIG_CHANGE


def test_give_product_res_gt_coin2_value_uses_all_coin2_then_coin1(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._num = 10
    vm._price = 5
    vm._balance = 8
    vm._coins2 = 1
    vm._coins1 = 10

    r = vm.give_product(1)

    assert r == vm_mod.VendingMachine.Response.OK
    assert vm._num == 9
    assert vm._coins2 == 0
    assert vm._coins1 == 9
    assert vm._balance == 0


def test_give_product_res_even_uses_only_coin2_ok(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._num = 10
    vm._price = 5
    vm._balance = 9
    vm._coins2 = 10
    vm._coins1 = 0

    r = vm.give_product(1)

    assert r == vm_mod.VendingMachine.Response.OK
    assert vm._num == 9
    assert vm._coins2 == 8
    assert vm._balance == 0


def test_give_product_odd_no_coin1_unsuitable(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._num = 10
    vm._price = 5
    vm._balance = 8
    vm._coins2 = 10
    vm._coins1 = 0

    r = vm.give_product(1)

    assert r == vm_mod.VendingMachine.Response.UNSUITABLE_CHANGE
    assert vm._balance == 8
    assert vm._num == 10


@pytest.mark.xfail(reason="give_product() should - res // _coinval2 to _coins2 and -1 to _coins1 when giving \
                    change. Instead the code mixes up _coins1 and _coins2", strict=False)
def test_give_product_odd_with_coin1_ok(vm, vm_mod):
    vm._mode = vm_mod.VendingMachine.Mode.OPERATION
    vm._num = 10
    vm._price = 3
    vm._balance = 8
    vm._coins2 = 10
    vm._coins1 = 5

    r = vm.give_product(1)

    assert r == vm_mod.VendingMachine.Response.OK
    assert vm._num == 9
    assert vm._coins2 == 8
    assert vm._coins1 == 4
    assert vm._balance == 0
