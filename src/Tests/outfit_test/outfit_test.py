import os

import Controllers
import Models
import Utils

connections = Utils.ConnectDBTest()
outfit_controller = Controllers.OutfitController(
    engine=connections.engine)
outfit_category_controller = Controllers.OutfitCategoryController(
    engine=connections.engine)

outfit_id = ""
categ_id = ""


def get_default_outfit_blob():
    image_path = "Assets/Images/OutfitDefault.png"
    with open(image_path, 'rb') as f:
        blob = f.read()

    return blob


def test_add_outfit_failed_empty_name():
    result = outfit_controller.create({
        "name": "",
        "description": "This is Description",
        "picture": get_default_outfit_blob(),
    })
    assert result.is_success == False
    assert result.message == "Name is required 📛"


def test_add_outfit_failed_name_too_long():
    result = outfit_controller.create({
        "name": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a bibendum nibh finibus sit amet. Nunc in tortor sit amet velit fringilla dignissim eget in dui. Ut ut neque elit. Nunc interdum, lacus vel ultrices malesuada, lacus quam volutpat dui, ac gravida sem lectus ac velit. Nullam suscipit nisl vitae urna egestas maximus. Nullam interdum nulla fringilla, ",
        "description": "This is Description",
        "picture": get_default_outfit_blob(),
    })
    assert result.is_success == False
    assert result.message == "Name maximum 40 characters 📛"


def test_add_outfit_failed_description_too_long():
    result = outfit_controller.create({
        "name": "This is Name",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a bibendum nibh finibus sit amet. Nunc in tortor sit amet velit fringilla dignissim eget in dui. Ut ut neque elit. Nunc interdum, lacus vel ultrices malesuada, lacus quam volutpat dui, ac gravida sem lectus ac velit. Nullam suscipit nisl vitae urna egestas maximus. Nullam interdum nulla fringilla, ",
        "picture": get_default_outfit_blob(),
    })
    assert result.is_success == False
    assert result.message == "Description maximum 255 characters 📛"


def test_add_outfit_failed_empty_picture():
    result = outfit_controller.create({
        "name": "This is Name",
        "description": "This is Description",
        "picture": None,
    })
    assert result.is_success == False
    assert result.message == "Picture is required 📛"


def test_add_outfit_failed_picture_too_big():
    result = outfit_controller.create({
        "name": "This is Name",
        "description": "This is Description",
        "picture": bytes(3 * 1024 * 1024),  # 3 MB
    })
    assert result.is_success == False
    assert result.message == "Picture is over 2 MB 📛"


def test_add_outfit_success():
    global outfit_id

    result = outfit_controller.create({
        "name": "This is Name",
        "description": "This is Description",
        "picture": get_default_outfit_blob(),
    })
    assert result.is_success == True
    assert result.message == "Outfit successfully added 👍"

    outfit_id = outfit_controller.get_one_by_index(result.data).data.id


def test_get_outfit_success():
    global outfit_id

    result = outfit_controller.get_one(outfit_id)

    assert result.is_success == True
    assert result.message == "Outfit successfully retrieved 👍"


def test_edit_outfit_failed_empty_name():
    result = outfit_controller.update(outfit_id, {
        "name": "",
        "description": "This is Description",
        "picture": get_default_outfit_blob(),
    })

    assert result.is_success == False
    assert result.message == "Name is required 📛"


def test_edit_outfit_failed_name_too_long():
    result = outfit_controller.update(outfit_id, {
        "name": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a bibendum nibh finibus sit amet. Nunc in tortor sit amet velit fringilla dignissim eget in dui. Ut ut neque elit. Nunc interdum, lacus vel ultrices malesuada, lacus quam volutpat dui, ac gravida sem lectus ac velit. Nullam suscipit nisl vitae urna egestas maximus. Nullam interdum nulla fringilla, ",
        "description": "This is Description",
        "picture": get_default_outfit_blob(),
    })

    assert result.is_success == False
    assert result.message == "Name maximum 40 characters 📛"


def test_edit_outfit_failed_description_too_long():
    result = outfit_controller.update(outfit_id, {
        "name": "This is Name",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ligula nisl, vestibulum et dignissim et, tincidunt et felis. Phasellus finibus suscipit odio, a bibendum nibh finibus sit amet. Nunc in tortor sit amet velit fringilla dignissim eget in dui. Ut ut neque elit. Nunc interdum, lacus vel ultrices malesuada, lacus quam volutpat dui, ac gravida sem lectus ac velit. Nullam suscipit nisl vitae urna egestas maximus. Nullam interdum nulla fringilla, ",
        "picture": get_default_outfit_blob(),
    })

    assert result.is_success == False
    assert result.message == "Description maximum 255 characters 📛"


def test_edit_outfit_failed_picture_too_big():
    result = outfit_controller.update(outfit_id, {
        "name": "This is Name",
        "description": "This is Description",
        "picture": bytes(3 * 1024 * 1024),  # 3 MB
    })

    assert result.is_success == False
    assert result.message == "Picture is over 2 MB 📛"


def test_edit_outfit_success():
    result = outfit_controller.update(outfit_id, {
        "name": "This is Edited Name",
        "description": "This is Edited Description",
        "picture": get_default_outfit_blob(),
    })

    assert result.is_success == True
    assert result.message == "Outfit successfully updated 👍"


def test_add_outfit_category_empty_name():
    result = outfit_category_controller.create({
        "name": "",
    })

    assert result.is_success == False
    assert result.message == "Category is required 📛"


def test_add_outfit_category_false_name_format():
    # No Underscore
    result = outfit_category_controller.create({
        "name": "This is False Name",
    })

    assert result.is_success == False
    assert result.message == "Wrong Format in Database 📛"

    # Too Many Underscore
    result = outfit_category_controller.create({
        "name": "First_Second_Third",
    })

    assert result.is_success == False
    assert result.message == "Wrong Format in Database 📛"

    # First String Is Not Color or Category
    result = outfit_category_controller.create({
        "name": "random_category",
    })

    assert result.is_success == False
    assert result.message == "Wrong Format in Database 📛"


def test_add_outfit_category_name_too_long():
    result = outfit_category_controller.create({
        "name": "category_Lorem ipsum dolor sit amet, consectetur tincidunt.",
    })

    assert result.is_success == False
    assert result.message == "Category maximum 30 characters 📛"


def test_add_outfit_category_success():
    global categ_id

    result = outfit_category_controller.create({
        "name": "category_test",
    })

    assert result.is_success == True
    assert result.message == "Outfit Category successfully added 👍"

    categ_id = outfit_category_controller.get_category_by_index(result.data).data.id


def test_get_outfit_category_success():
    global categ_id

    result = outfit_category_controller.get_category(categ_id)

    assert result.is_success == True
    assert result.message == "Category successfully retrieved 👍"


def test_add_outfit_relationship_success():
    result = outfit_controller.create_relationship({
        "outfit_id": outfit_controller.get_one(outfit_id).data.index,
        "category_id": outfit_category_controller.get_category(categ_id).data.index,
    })

    assert result.is_success == True
    assert result.message == "Outfit-Category relationship successfully added 👍"


def test_delete_outfit_relationship_success():
    result = outfit_controller.delete_relationship({
        "outfit_id": outfit_controller.get_one(outfit_id).data.index,
        "category_id": outfit_category_controller.get_category(categ_id).data.index,
    })

    assert result.is_success == True
    assert result.message == "Outfit-Category relationship successfully deleted 👍"


def test_delete_outfit_category_success():
    result = outfit_category_controller.delete(categ_id)

    assert result.is_success == True
    assert result.message == "Outfit Category successfully deleted 👍"


def test_delete_outfit_success():
    result = outfit_controller.delete(outfit_id)

    assert result.is_success == True
    assert result.message == "Outfit successfully deleted 👍"


# def test_remove_db():
#     os.remove("testing.db")
