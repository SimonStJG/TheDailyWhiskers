import json
from pathlib import Path

from thedailywhiskers.dailywhiskers import get_cat_pictures, CatPicture


def test_get_cat_pictures():
    with (Path(__file__).parent / "sample.json").open("r") as f:
        top_cats = json.load(f)

    assert list(get_cat_pictures(top_cats)) == [
        CatPicture(
            url="https://preview.redd.it/mb9i7wiwe1m51.jpg?width=216&crop=smart&auto=webp&s=8ede94d966718839c28e05617e7919de378c8c2b",
            reddit_url="https://www.reddit.com/r/cats/comments/ip817t/this_is_booker_booker_is_a_very_special_cat/",
        ),
        CatPicture(
            url="https://preview.redd.it/m959oft2y0m51.jpg?width=640&crop=smart&auto=webp&s=3f53339038dd3a3ffa97c130660f82a37f31b3ba",
            reddit_url="https://www.reddit.com/r/cats/comments/ip6jji/my_boy_turned_7_today/",
        ),
        CatPicture(
            url="https://preview.redd.it/5fqc3w33czl51.jpg?width=216&crop=smart&auto=webp&s=64bc745e77108269f9e2e9e42f723c08f7da5792",
            reddit_url="https://www.reddit.com/r/cats/comments/ip0vwe/my_boyfriend_got_me_the_cutest_bday_gift_reddit/",
        ),
        CatPicture(
            url="https://preview.redd.it/k4cg80ef43m51.jpg?width=216&crop=smart&auto=webp&s=8b865405f8f93b4fbff5a60197eca1352e29454d",
            reddit_url="https://www.reddit.com/r/cats/comments/ipc981/this_kitten_is_affecting_me_on_a_molecular_level/",
        ),
        CatPicture(
            url="https://preview.redd.it/j14t68dy40m51.jpg?width=216&crop=smart&auto=webp&s=d738b9841d9a97136eb8369b1fb3e33c440af39d",
            reddit_url="https://www.reddit.com/r/cats/comments/ip3vxp/am_i_dead/",
        ),
        CatPicture(
            url="https://preview.redd.it/4ibm6o4h71m51.jpg?width=216&crop=smart&auto=webp&s=b39059b863be65590f861acb19c0270ac2d25017",
            reddit_url="https://www.reddit.com/r/cats/comments/ip7di8/my_little_photogenic_boy/",
        ),
        CatPicture(
            url="https://preview.redd.it/thu7jogqp0m51.jpg?width=216&crop=smart&auto=webp&s=f585f813bb1f9b97096e5824a6e82d0974966b66",
            reddit_url="https://www.reddit.com/r/cats/comments/ip5smf/kitten_at_the_animal_shelter_i_volunteer_at/",
        ),
        CatPicture(
            url="https://preview.redd.it/qqcnuzzyf1m51.jpg?width=216&crop=smart&auto=webp&s=8374bb76402e9b862b937930a38623aa53b82928",
            reddit_url="https://www.reddit.com/r/cats/comments/ip846c/we_found_three_kittens_and_a_skinny_nursing_mom/",
        ),
        CatPicture(
            url="https://preview.redd.it/fg1af30bkzl51.jpg?width=216&crop=smart&auto=webp&s=648659a3942ea48af10139d64f071c5314b5807d",
            reddit_url="https://www.reddit.com/r/cats/comments/ip1shc/when_you_let_a_stranger_pet_your_cat/",
        ),
        CatPicture(
            url="https://preview.redd.it/5ynwpbbsm3m51.jpg?width=216&crop=smart&auto=webp&s=c3907e4b849957dc48ea3ed4f9248f101ddd1df1",
            reddit_url="https://www.reddit.com/r/cats/comments/ipdd1v/this_is_navi_she_has_a_lot_of_ear_fluff/",
        ),
        CatPicture(
            url="https://preview.redd.it/50422sqq4zl51.jpg?width=216&crop=smart&auto=webp&s=34a627374c85e297cd0f4a5c2f5042f51edb0506",
            reddit_url="https://www.reddit.com/r/cats/comments/ip03gl/found_an_orphaned_kitten_near_a_busy_intersection/",
        ),
        CatPicture(
            url="https://preview.redd.it/3g44f6vevzl51.jpg?width=216&crop=smart&auto=webp&s=3938177b0c2cee6fcca194b31add2438f9b1b2bb",
            reddit_url="https://www.reddit.com/r/cats/comments/ip2y5g/my_handsome_man_is_missing_heres_a_cute_pic_of/",
        ),
        CatPicture(
            url="https://preview.redd.it/yrys9lx74yl51.png?width=216&crop=smart&auto=webp&s=166eb6a94c03e6d801ae631e9312fb4a027e2780",
            reddit_url="https://www.reddit.com/r/cats/comments/iow4kh/a_small_boi_i_drew/",
        ),
        CatPicture(
            url="https://preview.redd.it/2f4ar98nf1m51.jpg?width=640&crop=smart&auto=webp&s=b76d64a5823214f2b9e65ffc2684f5ddae583b52",
            reddit_url="https://www.reddit.com/r/cats/comments/ip82ut/two_days_and_1700_later_my_murder_gremlin_is_home/",
        ),
        CatPicture(
            url="https://preview.redd.it/koc7nrs8u3m51.jpg?width=640&crop=smart&auto=webp&s=e62bcc98cb1ad51f809cdfddaa767f39eb2f305a",
            reddit_url="https://www.reddit.com/r/cats/comments/ipduc7/today_is_my_cat_chloes_birthday_today_she_turns_4/",
        ),
        CatPicture(
            url="https://preview.redd.it/o3oim3nvm0m51.jpg?width=216&crop=smart&auto=webp&s=8c801618e977112acaab4765312dc36813d4ec14",
            reddit_url="https://www.reddit.com/r/cats/comments/ip5jep/these_two_spend_all_day_fighting_then_give_me_10/",
        ),
    ]
