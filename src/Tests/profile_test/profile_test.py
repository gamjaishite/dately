import os

import Controllers
import Models
import Utils

connections = Utils.ConnectDBTest()
profile_controller = Controllers.ProfileController(
    engine=connections.engine)

partner_id = ""


def test_add_profile_failed_empty_name():
    result = profile_controller.add_profile({
        "name": "",
        "role": Models.RoleEnum.main.value,
    })
    assert result.is_success == False
    assert result.message == "Name is required 📛"


def test_add_profile_failed_name_too_long():
    result = profile_controller.add_profile({
        "name": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a bibendum nibh finibus sit amet. Nunc in tortor sit amet velit fringilla dignissim eget in dui. Ut ut neque elit. Nunc interdum, lacus vel ultrices malesuada, lacus quam volutpat dui, ac gravida sem lectus ac velit. Nullam suscipit nisl vitae urna egestas maximus. Nullam interdum nulla fringilla, ",
        "role": Models.RoleEnum.partner.value,
    })
    assert result.is_success == False
    assert result.message == "Name maximum 50 characters 📛"


def test_add_profile_failed_mbti_not_valid():
    result = profile_controller.add_profile({
        "name": "Kazuha",
        "role": Models.RoleEnum.partner.value,
        "mbti": "Not valid mbti",
    })
    assert result.is_success == False
    assert result.message == "MBTI is not valid 📛"


def test_add_profile_failed_hobbies_not_valid():
    result = profile_controller.add_profile({
        "name": "Kazuha",
        "role": Models.RoleEnum.partner.value,
        "hobbies": "Not valid hobies,,",
    })
    assert result.is_success == False
    assert result.message == "Hobbies is not valid 📛"


def test_add_profile_failed_hobbies_too_long():
    result = profile_controller.add_profile({
        "name": "Kazuha",
        "role": Models.RoleEnum.partner.value,
        "hobbies": "Too long hobbies Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a",
    })
    assert result.is_success == False
    assert result.message == "Hobbies maximum 100 characters 📛"


def test_add_profile_failed_social_media_too_long():
    result = profile_controller.add_profile({
        "name": "Kazuha",
        "role": Models.RoleEnum.partner.value,
        "social_media": "Too long social media Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a",
    })
    assert result.is_success == False
    assert result.message == "Instagram username maximum 30 characters 📛"


def test_add_profile_user_success():
    result = profile_controller.add_profile({
        "name": "test1",
        "role": Models.RoleEnum.main.value,
    })
    assert result.is_success
    assert result.message == "User test1 created successfuly 👍🎉"


def test_add_profile_partner_success():
    result = profile_controller.add_profile({
        "name": "Kazuha",
        "role": Models.RoleEnum.partner.value,
        "mbti": "ENFP",
        "hobbies": "dancing,balet,singing",
        "social_media": "k_a_z_u_h_a__",
    })
    assert result.is_success
    assert result.message == "Partner Kazuha created successfuly 👍🎉"


def test_get_partners_success():
    result = profile_controller.get_partners()
    assert result.is_success == True
    assert result.data[0].name == 'Kazuha'
    global partner_id
    partner_id = result.data[0].id


def test_edit_profile_failed_empty_name():
    result = profile_controller.edit_profile({
        "name": "",
        "role": Models.RoleEnum.partner.value,
        "id": partner_id,
    })
    assert result.is_success == False
    assert result.message == "Name is required 📛"


def test_edit_profile_failed_name_too_long():
    result = profile_controller.add_profile({
        "name": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a bibendum nibh finibus sit amet. Nunc in tortor sit amet velit fringilla dignissim eget in dui. Ut ut neque elit. Nunc interdum, lacus vel ultrices malesuada, lacus quam volutpat dui, ac gravida sem lectus ac velit. Nullam suscipit nisl vitae urna egestas maximus. Nullam interdum nulla fringilla, ",
        "role": Models.RoleEnum.partner.value,
        "id": partner_id,
    })
    assert result.is_success == False
    assert result.message == "Name maximum 50 characters 📛"


def test_edit_profile_failed_mbti_not_valid():
    result = profile_controller.add_profile({
        "name": "Kazuha",
        "role": Models.RoleEnum.partner.value,
        "mbti": "Not valid mbti",
        "id": partner_id,
    })
    assert result.is_success == False
    assert result.message == "MBTI is not valid 📛"


def test_edit_profile_failed_hobbies_not_valid():
    result = profile_controller.add_profile({
        "name": "Kazuha",
        "role": Models.RoleEnum.partner.value,
        "hobbies": "Not valid hobies,,",
        "id": partner_id,
    })
    assert result.is_success == False
    assert result.message == "Hobbies is not valid 📛"


def test_edit_profile_failed_hobbies_too_long():
    result = profile_controller.add_profile({
        "name": "Kazuha",
        "role": Models.RoleEnum.partner.value,
        "hobbies": "Too long hobbies Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a",
        "id": partner_id,
    })
    assert result.is_success == False
    assert result.message == "Hobbies maximum 100 characters 📛"


def test_edit_profile_failed_social_media_too_long():
    result = profile_controller.add_profile({
        "name": "Kazuha",
        "role": Models.RoleEnum.partner.value,
        "social_media": "Too long social media Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a",
        "id": partner_id,
    })
    assert result.is_success == False
    assert result.message == "Instagram username maximum 30 characters 📛"


def test_edit_profile_success():
    result = profile_controller.edit_profile({
        "name": "Kazuha Edited",
        "role": Models.RoleEnum.partner.value,
        "mbti": "istp",
        "hobbies": "dancing,balet,singing,edited",
        "social_media": "k_a_z_u_h_a__",
        "id": partner_id,
    })
    assert result.is_success
    assert result.message == "Profile updated successfuly 👍🎉"

    result = profile_controller.get_partner_by_id(partner_id)

    assert result.data.name == 'Kazuha Edited'
    assert result.data.hobbies == "dancing,balet,singing,edited"
    assert result.data.mbti == "ISTP"


# TODO: Delete Partner
def test_delete_profile_partner_success():
    result = profile_controller.delete_partner(partner_id)

    assert result.is_success


def test_remove_db():
    os.remove("testing.db")
